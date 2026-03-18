"""
Write thesis chapters from markdown files to a single Google Doc with formatting.

Usage:
    python3 scripts/write_thesis_to_gdoc.py \
        --credentials /path/to/service-account.json \
        --share-with your-email@gmail.com \
        --doc-id DOCUMENT_ID

Two-pass approach to minimize API calls:
  Pass 1: Build full plain text + record formatting ranges
  Pass 2: Insert text in chunks, then apply formatting in batches
"""

import argparse
import os
import re
import sys
import time
from dataclasses import dataclass, field
from enum import Enum, auto

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# ---------------------------------------------------------------------------
# Markdown Parser
# ---------------------------------------------------------------------------

class BlockType(Enum):
    HEADING = auto()
    PARAGRAPH = auto()
    TABLE = auto()
    CODE_BLOCK = auto()
    ORDERED_LIST = auto()
    UNORDERED_LIST = auto()
    HORIZONTAL_RULE = auto()
    MATH_BLOCK = auto()


@dataclass
class InlineSpan:
    text: str
    bold: bool = False
    italic: bool = False
    code: bool = False


@dataclass
class Block:
    type: BlockType
    level: int = 0
    raw_text: str = ""
    spans: list = field(default_factory=list)
    rows: list = field(default_factory=list)
    items: list = field(default_factory=list)
    language: str = ""


def parse_inline(text: str) -> list[InlineSpan]:
    spans = []
    i = 0
    n = len(text)

    while i < n:
        if text[i] == '`' and not (i + 1 < n and text[i + 1] == '`'):
            end = text.find('`', i + 1)
            if end != -1:
                spans.append(InlineSpan(text=text[i + 1:end], code=True))
                i = end + 1
                continue

        if i + 2 < n and text[i:i + 3] in ('***', '___'):
            marker = text[i:i + 3]
            end = text.find(marker, i + 3)
            if end != -1:
                spans.append(InlineSpan(text=text[i + 3:end], bold=True, italic=True))
                i = end + 3
                continue

        if i + 1 < n and text[i:i + 2] in ('**', '__'):
            marker = text[i:i + 2]
            end = text.find(marker, i + 2)
            if end != -1:
                spans.append(InlineSpan(text=text[i + 2:end], bold=True))
                i = end + 2
                continue

        if text[i] in ('*', '_'):
            marker = text[i]
            if not (i + 1 < n and text[i + 1] == marker):
                end = text.find(marker, i + 1)
                if end != -1 and end > i + 1:
                    spans.append(InlineSpan(text=text[i + 1:end], italic=True))
                    i = end + 1
                    continue

        if text[i] == '$' and not (i + 1 < n and text[i + 1] == '$'):
            end = text.find('$', i + 1)
            if end != -1:
                spans.append(InlineSpan(text=text[i + 1:end], italic=True, code=True))
                i = end + 1
                continue

        plain_end = i + 1
        while plain_end < n and text[plain_end] not in ('*', '_', '`', '$'):
            plain_end += 1
        spans.append(InlineSpan(text=text[i:plain_end]))
        i = plain_end

    return spans if spans else [InlineSpan(text="")]


def parse_markdown(content: str) -> list[Block]:
    lines = content.split('\n')
    blocks = []
    i = 0

    while i < len(lines):
        line = lines[i]

        if not line.strip():
            i += 1
            continue

        heading_match = re.match(r'^(#{1,6})\s+(.+)$', line)
        if heading_match:
            level = len(heading_match.group(1))
            text = heading_match.group(2).strip()
            blocks.append(Block(type=BlockType.HEADING, level=level, raw_text=text, spans=parse_inline(text)))
            i += 1
            continue

        if re.match(r'^(-{3,}|\*{3,}|_{3,})$', line.strip()):
            blocks.append(Block(type=BlockType.HORIZONTAL_RULE))
            i += 1
            continue

        if line.strip().startswith('$$'):
            stripped = line.strip()
            # Single-line math: $$...$$
            if stripped.endswith('$$') and len(stripped) > 4:
                math_text = stripped[2:-2].strip()
                blocks.append(Block(type=BlockType.MATH_BLOCK, raw_text=math_text, spans=[InlineSpan(text=math_text, italic=True)]))
                i += 1
                continue
            # Multi-line math block
            math_lines = [stripped[2:]]  # remove opening $$
            i += 1
            while i < len(lines) and '$$' not in lines[i]:
                math_lines.append(lines[i])
                i += 1
            if i < len(lines):
                closing_line = lines[i].strip()
                if closing_line.endswith('$$'):
                    math_lines.append(closing_line[:-2])
                i += 1
            math_text = '\n'.join(l for l in math_lines if l.strip())
            blocks.append(Block(type=BlockType.MATH_BLOCK, raw_text=math_text, spans=[InlineSpan(text=math_text, italic=True)]))
            continue

        if line.strip().startswith('```'):
            lang = line.strip()[3:].strip()
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('```'):
                code_lines.append(lines[i])
                i += 1
            if i < len(lines):
                i += 1
            blocks.append(Block(type=BlockType.CODE_BLOCK, raw_text='\n'.join(code_lines), language=lang))
            continue

        if line.strip().startswith('|'):
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                table_lines.append(lines[i])
                i += 1
            rows = []
            for tl in table_lines:
                cells = [c.strip() for c in tl.strip().strip('|').split('|')]
                if all(re.match(r'^:?-+:?$', c) for c in cells):
                    continue
                rows.append(cells)
            if rows:
                blocks.append(Block(type=BlockType.TABLE, rows=rows))
            continue

        if re.match(r'^(\s*[-*+]\s)', line):
            items = []
            while i < len(lines) and re.match(r'^(\s*[-*+]\s)', lines[i]):
                item_text = re.sub(r'^\s*[-*+]\s+', '', lines[i])
                items.append(parse_inline(item_text))
                i += 1
            blocks.append(Block(type=BlockType.UNORDERED_LIST, items=items))
            continue

        if re.match(r'^(\s*\d+[.)]\s)', line):
            items = []
            while i < len(lines) and re.match(r'^(\s*\d+[.)]\s)', lines[i]):
                item_text = re.sub(r'^\s*\d+[.)]\s+', '', lines[i])
                items.append(parse_inline(item_text))
                i += 1
            blocks.append(Block(type=BlockType.ORDERED_LIST, items=items))
            continue

        para_lines = []
        while i < len(lines):
            l = lines[i]
            if not l.strip():
                break
            if re.match(r'^#{1,6}\s', l):
                break
            if l.strip().startswith('```'):
                break
            if l.strip().startswith('|') and '|' in l[1:]:
                break
            if re.match(r'^(-{3,}|\*{3,}|_{3,})$', l.strip()):
                break
            if l.strip().startswith('$$'):
                break
            para_lines.append(l)
            i += 1
        if para_lines:
            text = ' '.join(para_lines)
            blocks.append(Block(type=BlockType.PARAGRAPH, raw_text=text, spans=parse_inline(text)))

    return blocks


# ---------------------------------------------------------------------------
# Formatting range tracking
# ---------------------------------------------------------------------------

@dataclass
class FormatRange:
    start: int
    end: int
    bold: bool = False
    italic: bool = False
    font_family: str = None
    font_size: float = None
    fg_color: dict = None
    bg_color: dict = None


@dataclass
class ParagraphFormat:
    start: int
    end: int
    named_style: str = None
    alignment: str = None
    indent_pt: float = None
    bullet_preset: str = None


# ---------------------------------------------------------------------------
# Two-pass document builder
# ---------------------------------------------------------------------------

class DocumentBuilder:
    """Builds plain text + formatting metadata, then writes to Google Docs."""

    HEADING_STYLES = {
        1: 'HEADING_1', 2: 'HEADING_2', 3: 'HEADING_3',
        4: 'HEADING_4', 5: 'HEADING_5', 6: 'HEADING_6',
    }

    def __init__(self):
        self.text_parts: list[str] = []  # plain text segments (non-table)
        self.format_ranges: list[FormatRange] = []
        self.para_formats: list[ParagraphFormat] = []
        self.tables: list[dict] = []  # {insert_offset, rows}
        self.pos = 0  # virtual cursor

    def _append(self, text: str) -> tuple[int, int]:
        start = self.pos
        self.text_parts.append(text)
        self.pos += len(text)
        return start, self.pos

    def add_spans(self, spans: list[InlineSpan], newline=True):
        block_start = self.pos
        for span in spans:
            s = self.pos
            self._append(span.text)
            e = self.pos
            if span.bold or span.italic or span.code:
                self.format_ranges.append(FormatRange(
                    start=s, end=e,
                    bold=span.bold, italic=span.italic,
                    font_family='Consolas' if span.code else None,
                    bg_color={'red': 0.95, 'green': 0.95, 'blue': 0.95} if span.code else None,
                ))
        if newline:
            self._append('\n')
        return block_start, self.pos

    def add_heading(self, block: Block):
        start, end = self.add_spans(block.spans)
        style = self.HEADING_STYLES.get(block.level, 'HEADING_3')
        self.para_formats.append(ParagraphFormat(start=start, end=end, named_style=style))

    def add_paragraph(self, block: Block):
        self.add_spans(block.spans)

    def add_code_block(self, block: Block):
        start, _ = self._append(block.raw_text + '\n')
        end = self.pos
        self.format_ranges.append(FormatRange(
            start=start, end=end,
            font_family='Consolas', font_size=9,
            bg_color={'red': 0.95, 'green': 0.95, 'blue': 0.95},
        ))
        self.para_formats.append(ParagraphFormat(start=start, end=end, indent_pt=18.0))

    def add_math_block(self, block: Block):
        start, _ = self._append(block.raw_text + '\n')
        end = self.pos
        self.format_ranges.append(FormatRange(
            start=start, end=end, italic=True, font_family='Cambria Math',
        ))
        self.para_formats.append(ParagraphFormat(start=start, end=end, alignment='CENTER'))

    def add_table(self, block: Block):
        """Record a table to be inserted separately (tables need special API calls)."""
        # Insert a placeholder marker in text
        marker = f'\n'  # just a newline where the table will go
        start = self.pos
        self._append(marker)
        self.tables.append({
            'text_offset': start,
            'rows': block.rows,
        })

    def add_list(self, block: Block, ordered=False):
        start = self.pos
        for item_spans in block.items:
            for span in item_spans:
                s = self.pos
                self._append(span.text)
                e = self.pos
                if span.bold or span.italic or span.code:
                    self.format_ranges.append(FormatRange(
                        start=s, end=e,
                        bold=span.bold, italic=span.italic,
                        font_family='Consolas' if span.code else None,
                    ))
            self._append('\n')
        end = self.pos
        preset = 'NUMBERED_DECIMAL_ALPHA_ROMAN' if ordered else 'BULLET_DISC_CIRCLE_SQUARE'
        self.para_formats.append(ParagraphFormat(start=start, end=end, bullet_preset=preset))

    def add_horizontal_rule(self):
        text = '─' * 50 + '\n'
        start, _ = self._append(text)
        end = self.pos
        self.format_ranges.append(FormatRange(
            start=start, end=end,
            fg_color={'red': 0.7, 'green': 0.7, 'blue': 0.7}, font_size=6,
        ))
        self.para_formats.append(ParagraphFormat(start=start, end=end, alignment='CENTER'))

    def add_cover_page(self, content: str):
        lines = content.strip().split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                self._append('\n')
                continue
            start = self.pos
            self._append(line + '\n')
            end = self.pos
            self.para_formats.append(ParagraphFormat(start=start, end=end, alignment='CENTER'))
            if 'GRADUATION THESIS' in line or 'ADAPTIVE LEARNING' in line:
                self.format_ranges.append(FormatRange(start=start, end=end - 1, bold=True, font_size=16))
            elif 'MINISTRY' in line or 'HANOI UNIVERSITY' in line or 'FACULTY' in line:
                self.format_ranges.append(FormatRange(start=start, end=end - 1, bold=True, font_size=13))

    def add_page_break_marker(self):
        """We'll handle page breaks separately since they're special."""
        # Use a Unicode marker we can find later
        self._append('\f\n')  # form feed as page break marker

    def add_block(self, block: Block):
        if block.type == BlockType.HEADING:
            self.add_heading(block)
        elif block.type == BlockType.PARAGRAPH:
            self.add_paragraph(block)
        elif block.type == BlockType.CODE_BLOCK:
            self.add_code_block(block)
        elif block.type == BlockType.MATH_BLOCK:
            self.add_math_block(block)
        elif block.type == BlockType.TABLE:
            self.add_table(block)
        elif block.type == BlockType.UNORDERED_LIST:
            self.add_list(block, ordered=False)
        elif block.type == BlockType.ORDERED_LIST:
            self.add_list(block, ordered=True)
        elif block.type == BlockType.HORIZONTAL_RULE:
            self.add_horizontal_rule()

    def get_full_text(self) -> str:
        return ''.join(self.text_parts)


# ---------------------------------------------------------------------------
# Google Docs Writer with batching and retry
# ---------------------------------------------------------------------------

def retry_api_call(func, max_retries=5):
    """Retry API calls with exponential backoff on 429 errors."""
    for attempt in range(max_retries):
        try:
            return func()
        except HttpError as e:
            if e.resp.status == 429:
                wait = min(2 ** attempt * 10, 60)
                print(f"  Rate limited, waiting {wait}s... (attempt {attempt + 1}/{max_retries})")
                time.sleep(wait)
            else:
                raise
    raise Exception(f"Failed after {max_retries} retries")


class GoogleDocsWriter:
    MAX_BATCH = 50  # max requests per batchUpdate to stay safe

    def __init__(self, credentials_path: str):
        creds = service_account.Credentials.from_service_account_file(
            credentials_path,
            scopes=[
                'https://www.googleapis.com/auth/documents',
                'https://www.googleapis.com/auth/drive',
            ]
        )
        self.docs_service = build('docs', 'v1', credentials=creds)
        self.drive_service = build('drive', 'v3', credentials=creds)

    def _batch_update(self, doc_id: str, requests: list):
        if not requests:
            return
        # Split into chunks
        for i in range(0, len(requests), self.MAX_BATCH):
            chunk = requests[i:i + self.MAX_BATCH]
            retry_api_call(lambda c=chunk: self.docs_service.documents().batchUpdate(
                documentId=doc_id, body={'requests': c}
            ).execute())
            if i + self.MAX_BATCH < len(requests):
                time.sleep(2)  # small delay between chunks

    def write_document(self, doc_id: str, builder: DocumentBuilder):
        """Write the built content to the Google Doc."""
        full_text = builder.get_full_text()

        # --- Step 1: Clear existing content ---
        print("Clearing existing content...")
        doc = retry_api_call(lambda: self.docs_service.documents().get(documentId=doc_id).execute())
        body = doc['body']['content']
        end_index = body[-1]['endIndex'] - 1 if body else 1
        if end_index > 1:
            self._batch_update(doc_id, [{
                'deleteContentRange': {
                    'range': {'startIndex': 1, 'endIndex': end_index}
                }
            }])

        # --- Step 2: Insert all plain text at once ---
        # Remove form feed markers, we'll handle page breaks differently
        clean_text = full_text.replace('\f', '')
        print(f"Inserting text ({len(clean_text)} chars)...")

        # Insert in chunks of 50k chars to avoid payload limits
        CHUNK_SIZE = 50000
        insert_pos = 1
        for ci in range(0, len(clean_text), CHUNK_SIZE):
            chunk = clean_text[ci:ci + CHUNK_SIZE]
            retry_api_call(lambda c=chunk, p=insert_pos: self.docs_service.documents().batchUpdate(
                documentId=doc_id, body={'requests': [{
                    'insertText': {
                        'location': {'index': p},
                        'text': c,
                    }
                }]}
            ).execute())
            insert_pos += len(chunk)
            if ci + CHUNK_SIZE < len(clean_text):
                time.sleep(2)

        # Offset for all formatting: text starts at index 1
        base_offset = 1
        # Adjust for removed \f characters
        ff_positions = [m.start() for m in re.finditer('\f', full_text)]

        def adjusted_pos(virtual_pos):
            """Convert virtual position to actual doc position, accounting for removed \f."""
            removed = sum(1 for fp in ff_positions if fp < virtual_pos)
            return base_offset + virtual_pos - removed

        # --- Step 3: Apply text formatting ---
        print("Applying text formatting...")
        fmt_requests = []
        for fr in builder.format_ranges:
            start = adjusted_pos(fr.start)
            end = adjusted_pos(fr.end)
            if start >= end:
                continue

            style = {}
            fields = []
            if fr.bold:
                style['bold'] = True
                fields.append('bold')
            if fr.italic:
                style['italic'] = True
                fields.append('italic')
            if fr.font_family:
                style['weightedFontFamily'] = {'fontFamily': fr.font_family}
                fields.append('weightedFontFamily')
            if fr.font_size:
                style['fontSize'] = {'magnitude': fr.font_size, 'unit': 'PT'}
                fields.append('fontSize')
            if fr.fg_color:
                style['foregroundColor'] = {'color': {'rgbColor': fr.fg_color}}
                fields.append('foregroundColor')
            if fr.bg_color:
                style['backgroundColor'] = {'color': {'rgbColor': fr.bg_color}}
                fields.append('backgroundColor')

            if fields:
                fmt_requests.append({
                    'updateTextStyle': {
                        'range': {'startIndex': start, 'endIndex': end},
                        'textStyle': style,
                        'fields': ','.join(fields),
                    }
                })

        self._batch_update(doc_id, fmt_requests)

        # --- Step 4: Apply paragraph formatting ---
        print("Applying paragraph formatting...")
        para_requests = []
        bullet_requests = []

        for pf in builder.para_formats:
            start = adjusted_pos(pf.start)
            end = adjusted_pos(pf.end)
            if start >= end:
                continue

            if pf.named_style:
                para_requests.append({
                    'updateParagraphStyle': {
                        'range': {'startIndex': start, 'endIndex': end},
                        'paragraphStyle': {'namedStyleType': pf.named_style},
                        'fields': 'namedStyleType',
                    }
                })
            if pf.alignment:
                para_requests.append({
                    'updateParagraphStyle': {
                        'range': {'startIndex': start, 'endIndex': end},
                        'paragraphStyle': {'alignment': pf.alignment},
                        'fields': 'alignment',
                    }
                })
            if pf.indent_pt:
                para_requests.append({
                    'updateParagraphStyle': {
                        'range': {'startIndex': start, 'endIndex': end},
                        'paragraphStyle': {
                            'indentFirstLine': {'magnitude': pf.indent_pt, 'unit': 'PT'},
                            'indentStart': {'magnitude': pf.indent_pt, 'unit': 'PT'},
                        },
                        'fields': 'indentFirstLine,indentStart',
                    }
                })
            if pf.bullet_preset:
                bullet_requests.append({
                    'createParagraphBullets': {
                        'range': {'startIndex': start, 'endIndex': end},
                        'bulletPreset': pf.bullet_preset,
                    }
                })

        self._batch_update(doc_id, para_requests)
        if bullet_requests:
            self._batch_update(doc_id, bullet_requests)

        # --- Step 5: Insert tables ---
        if builder.tables:
            print(f"Inserting {len(builder.tables)} tables...")
            # Process tables from last to first to avoid index shifting
            sorted_tables = sorted(builder.tables, key=lambda t: t['text_offset'], reverse=True)
            for table_info in sorted_tables:
                self._insert_table(doc_id, table_info, ff_positions, base_offset)
                time.sleep(2)

        # --- Step 6: Table of Contents ---
        # Google Docs API doesn't support insertTableOfContents.
        # The user can add it manually: Insert > Table of Contents in Google Docs.
        print("Note: Add Table of Contents manually in Google Docs (Insert > Table of Contents)")
        print("Done!")

    def _insert_table(self, doc_id: str, table_info: dict, ff_positions: list, base_offset: int):
        """Insert a table at the recorded position."""
        rows = table_info['rows']
        if not rows:
            return

        virtual_pos = table_info['text_offset']
        removed = sum(1 for fp in ff_positions if fp < virtual_pos)
        insert_at = base_offset + virtual_pos - removed

        n_rows = len(rows)
        n_cols = max(len(r) for r in rows)

        # Delete the placeholder newline
        try:
            self._batch_update(doc_id, [{
                'deleteContentRange': {
                    'range': {'startIndex': insert_at, 'endIndex': insert_at + 1}
                }
            }])
        except Exception:
            pass

        # Insert the table
        retry_api_call(lambda: self.docs_service.documents().batchUpdate(
            documentId=doc_id, body={'requests': [{
                'insertTable': {
                    'rows': n_rows,
                    'columns': n_cols,
                    'location': {'index': insert_at},
                }
            }]}
        ).execute())

        # Read document to get table cell indices
        doc = retry_api_call(lambda: self.docs_service.documents().get(documentId=doc_id).execute())
        body = doc['body']['content']

        # Find the table at or near insert_at
        table_element = None
        for element in body:
            if 'table' in element:
                if element['startIndex'] >= insert_at - 2:
                    table_element = element
                    break

        if not table_element:
            print("  Warning: Could not find inserted table")
            return

        table = table_element['table']

        # Fill cells from last to first
        cell_ops = []
        for row_idx in range(n_rows):
            for col_idx in range(n_cols):
                cell_text = rows[row_idx][col_idx] if col_idx < len(rows[row_idx]) else ''
                cell_text = cell_text.strip()
                if not cell_text:
                    continue
                try:
                    cell_content = table['tableRows'][row_idx]['tableCells'][col_idx]['content']
                    cell_start = cell_content[0]['startIndex']
                    cell_ops.append((cell_start, cell_text, row_idx == 0))
                except (IndexError, KeyError):
                    continue

        cell_ops.sort(key=lambda x: x[0], reverse=True)

        requests = []
        for cell_start, cell_text, is_header in cell_ops:
            requests.append({
                'insertText': {
                    'location': {'index': cell_start},
                    'text': cell_text,
                }
            })
            if is_header:
                requests.append({
                    'updateTextStyle': {
                        'range': {'startIndex': cell_start, 'endIndex': cell_start + len(cell_text)},
                        'textStyle': {'bold': True},
                        'fields': 'bold',
                    }
                })

        if requests:
            self._batch_update(doc_id, requests)

    def _insert_toc(self, doc_id: str):
        """Insert a TOC heading and table of contents at the start."""
        # Insert TOC heading
        toc_text = 'Table of Contents\n'
        retry_api_call(lambda: self.docs_service.documents().batchUpdate(
            documentId=doc_id, body={'requests': [
                {'insertText': {'location': {'index': 1}, 'text': toc_text}},
            ]}
        ).execute())

        self._batch_update(doc_id, [
            {
                'updateParagraphStyle': {
                    'range': {'startIndex': 1, 'endIndex': 1 + len(toc_text)},
                    'paragraphStyle': {'namedStyleType': 'HEADING_1'},
                    'fields': 'namedStyleType',
                }
            }
        ])

        # Insert the actual TOC
        toc_index = 1 + len(toc_text)
        retry_api_call(lambda: self.docs_service.documents().batchUpdate(
            documentId=doc_id, body={'requests': [{
                'insertTableOfContents': {
                    'location': {'index': toc_index},
                }
            }]}
        ).execute())


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description='Write thesis to Google Doc')
    parser.add_argument('--credentials', '-c', required=True, help='Service account JSON path')
    parser.add_argument('--share-with', '-s', help='Email to share with')
    parser.add_argument('--doc-id', '-d', required=True, help='Existing Google Doc ID')
    parser.add_argument('--chapters-dir',
                        default=os.path.join(os.path.dirname(__file__), '..', 'documents', 'thesis-chapters'),
                        help='Path to thesis chapters directory')
    args = parser.parse_args()

    chapters_dir = os.path.abspath(args.chapters_dir)
    if not os.path.isdir(chapters_dir):
        print(f"Error: chapters directory not found: {chapters_dir}")
        sys.exit(1)

    chapter_files = [
        ('0-cover-page.md', True),
        ('abstract.md', False),
        ('chapter1-introduction.md', False),
        ('chapter2-literature-review.md', False),
        ('chapter3-system-design.md', False),
    ]

    # --- Pass 1: Build content ---
    print("=== Pass 1: Parsing markdown ===")
    builder = DocumentBuilder()

    for idx, (filename, is_cover) in enumerate(chapter_files):
        path = os.path.join(chapters_dir, filename)
        if not os.path.isfile(path):
            print(f"  Warning: {filename} not found, skipping")
            continue

        print(f"  Parsing: {filename}")
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        if is_cover:
            builder.add_cover_page(content)
        else:
            blocks = parse_markdown(content)
            for block in blocks:
                builder.add_block(block)

        # Page break between chapters (not after last)
        if idx < len(chapter_files) - 1:
            builder.add_page_break_marker()

    full_text = builder.get_full_text()
    print(f"  Total: {len(full_text)} chars, {len(builder.format_ranges)} format ranges, "
          f"{len(builder.para_formats)} paragraph formats, {len(builder.tables)} tables")

    # --- Pass 2: Write to Google Docs ---
    print("\n=== Pass 2: Writing to Google Docs ===")
    writer = GoogleDocsWriter(args.credentials)
    writer.write_document(args.doc_id, builder)

    # Share if requested
    if args.share_with:
        try:
            writer.drive_service.permissions().create(
                fileId=args.doc_id,
                body={'type': 'user', 'role': 'writer', 'emailAddress': args.share_with},
                sendNotificationEmail=False,
            ).execute()
            print(f"Shared with: {args.share_with}")
        except HttpError as e:
            # May fail if already shared or if service account doesn't own the doc
            print(f"  Note: Could not share (you likely already have access): {e.reason}")

    print(f"\nYour thesis is ready at:")
    print(f"https://docs.google.com/document/d/{args.doc_id}/edit")


if __name__ == '__main__':
    main()
