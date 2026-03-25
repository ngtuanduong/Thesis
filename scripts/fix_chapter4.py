"""
Fix Chapter 4 in Google Docs.
1. Delete existing Chapter 4 content
2. Re-insert from markdown source with proper headings/formatting
3. Insert all 7 images (2 tables + 5 figures) with captions

Figure captions and placement (not in markdown, must be added manually):
- Figure 4.1: After section 4.3.2 (Submission Pipeline Sequence Diagram)
- Figure 4.2: After section 4.3.1 text about BKT (BKT Hidden Markov Model)
- Figure 4.3: After section 4.5.3 (MAB Decision Flow)
- Figure 4.4: After section 4.6.1 text about FSRS (FSRS Card Lifecycle)
- Figure 4.5: After section 4.6.1 retrievability curve text (Retrievability Curve)
"""
import warnings
warnings.filterwarnings("ignore")

import re
import time
from google.oauth2 import service_account
from googleapiclient.discovery import build

KEY_FILE = "C:/Users/duong/WebstormProjects/Thesis/infra-inkwell-465003-f2-369235afe5ac.json"
DOC_ID = "1O4wJNovNTFjD5DORC-WOJ2AftbcjfyoQ6HuzRSlYFfA"
SCOPES = ['https://www.googleapis.com/auth/documents', 'https://www.googleapis.com/auth/drive']

VISUALS = {
    "Table 4.1": "https://files.catbox.moe/7nj9z8.png",
    "Table 4.2": "https://files.catbox.moe/0005w3.png",
    "Figure 4.1": "https://files.catbox.moe/vq16l2.png",
    "Figure 4.2": "https://files.catbox.moe/0pk8fv.png",
    "Figure 4.3": "https://files.catbox.moe/vbzbwp.png",
    "Figure 4.4": "https://files.catbox.moe/3yojqt.png",
    "Figure 4.5": "https://files.catbox.moe/4g1sh7.png",
}

IMAGE_SIZES = {
    "Table 4.1": (468, 170),
    "Table 4.2": (420, 165),
    "Figure 4.1": (468, 358),
    "Figure 4.2": (400, 280),
    "Figure 4.3": (468, 433),
    "Figure 4.4": (450, 316),
    "Figure 4.5": (430, 300),
}

# Figure captions - these are NOT in the markdown and must be inserted separately
FIGURE_CAPTIONS = {
    "Figure 4.1": "Figure 4.1. Submission processing pipeline: sequence diagram showing how a code submission triggers updates across all four adaptive layers.",
    "Figure 4.2": "Figure 4.2. BKT as a Hidden Markov Model: the two hidden states (Learned, Not Learned) and the four transition/emission parameters.",
    "Figure 4.3": "Figure 4.3. Hierarchical MAB decision flow: Level 1 selects a concept using Thompson Sampling with prerequisite and FSRS constraints; Level 2 selects a problem within the ZPD.",
    "Figure 4.4": "Figure 4.4. FSRS card lifecycle: state transitions showing how difficulty, stability, and retrievability evolve through successive reviews.",
    "Figure 4.5": "Figure 4.5. FSRS retrievability decay curve: the power-law relationship between elapsed time and recall probability for different stability values.",
}

# Where to insert each figure caption+image (identified by the text that precedes it)
# The caption+image will be inserted AFTER the paragraph containing this text
FIGURE_PLACEMENT = {
    "Figure 4.1": "event-driven wiring ensures mastery estimates are current",
    "Figure 4.2": "to prevent any numerical boundary problems",
    "Figure 4.3": "forcing every outcome into a binary mold",
    "Figure 4.4": "stability never rises after a failure",
    "Figure 4.5": "the due date after each review is simply the current time plus",
}


def get_service():
    creds = service_account.Credentials.from_service_account_file(KEY_FILE, scopes=SCOPES)
    return build('docs', 'v1', credentials=creds)


def find_chapter4_range(service):
    """Find Chapter 4 boundaries."""
    doc = service.documents().get(documentId=DOC_ID).execute()
    body = doc['body']['content']

    ch4_start = None
    ch4_end = None
    found_ch4_summary = False

    for elem in body:
        if 'paragraph' not in elem:
            continue
        text = ''
        for el in elem['paragraph'].get('elements', []):
            if 'textRun' in el:
                text += el['textRun']['content']
        text_upper = text.strip().upper()
        style = elem['paragraph'].get('paragraphStyle', {}).get('namedStyleType', '')

        if ch4_start is None:
            if 'CHAPTER 4' in text_upper and ('IMPLEMENTATION' in text_upper or text_upper.startswith('CHAPTER 4')):
                ch4_start = elem['startIndex']
                print(f"  Found Ch4 start at {ch4_start}: {text.strip()[:60]}")

        elif ch4_end is None:
            # Track when we pass Chapter Summary heading
            if text.strip() == 'Chapter Summary' and 'HEADING' in style:
                found_ch4_summary = True
                continue

            # After Ch4 summary, look for the transition paragraph
            if found_ch4_summary:
                if text.strip().startswith('Chapter 5 turns to') or text.strip().startswith('Chapter 5:'):
                    ch4_end = elem['endIndex']
                    print(f"  Found Ch4 end (after summary) at {ch4_end}: {text.strip()[:60]}")
                    break

            # Also check for any next chapter heading or References
            if ('CHAPTER 5' in text_upper or 'CHAPTER 2' in text_upper or
                text_upper == 'REFERENCES' or text_upper == 'BIBLIOGRAPHY'):
                if 'HEADING' in style:
                    ch4_end = elem['startIndex']
                    print(f"  Found Ch4 end (next heading) at {ch4_end}: {text.strip()[:60]}")
                    break

    if ch4_start and ch4_end is None:
        # Last resort: scan for the paragraph that ends Ch4's content
        for elem in body:
            if 'paragraph' not in elem:
                continue
            if elem.get('startIndex', 0) <= ch4_start:
                continue
            text = ''
            for el in elem['paragraph'].get('elements', []):
                if 'textRun' in el:
                    text += el['textRun']['content']

            text_stripped = text.strip()
            # Chapter 4 ends with transition to Chapter 5
            if 'Chapter 5 turns to' in text_stripped:
                ch4_end = elem['endIndex']
                print(f"  Found Ch4 end (last resort) at {ch4_end}: {text_stripped[:60]}")
                break

    if ch4_start and ch4_end is None:
        # Absolute fallback: find the next HEADING_2 after ch4 content
        # that is NOT a 4.x heading
        past_ch4_start = False
        for elem in body:
            if 'paragraph' not in elem:
                continue
            if elem.get('startIndex', 0) == ch4_start:
                past_ch4_start = True
                continue
            if not past_ch4_start:
                continue
            text = ''
            for el in elem['paragraph'].get('elements', []):
                if 'textRun' in el:
                    text += el['textRun']['content']
            style = elem['paragraph'].get('paragraphStyle', {}).get('namedStyleType', '')
            text_stripped = text.strip()
            # Look for Chapter 1/2/3 headings that come after Ch4 in the doc
            if 'HEADING' in style and ('Chapter 1' in text_stripped or 'Chapter 2' in text_stripped or 'Chapter 3' in text_stripped):
                ch4_end = elem['startIndex']
                print(f"  Found Ch4 end (fallback heading) at {ch4_end}: {text_stripped[:60]}")
                break

    return ch4_start, ch4_end


def delete_range(service, start, end):
    """Delete content range."""
    actual_start = max(1, start - 1)  # Catch page break before heading
    print(f"  Deleting range [{actual_start}, {end}] ({end - actual_start} chars)")
    try:
        service.documents().batchUpdate(
            documentId=DOC_ID,
            body={'requests': [{
                'deleteContentRange': {
                    'range': {
                        'startIndex': actual_start,
                        'endIndex': end,
                    }
                }
            }]}
        ).execute()
        print("  Delete OK")
        return actual_start
    except Exception as e:
        print(f"  Delete failed with -1 offset: {e}")
        service.documents().batchUpdate(
            documentId=DOC_ID,
            body={'requests': [{
                'deleteContentRange': {
                    'range': {
                        'startIndex': start,
                        'endIndex': end,
                    }
                }
            }]}
        ).execute()
        print("  Delete OK (no offset)")
        return start


def parse_chapter():
    """Parse chapter4-implementation.md into structured blocks."""
    with open("C:/Users/duong/WebstormProjects/Thesis/documents/thesis-chapters/chapter4-implementation.md") as f:
        text = f.read()

    blocks = []
    lines = text.split('\n')
    i = 0
    in_code = False
    code_buf = []

    while i < len(lines):
        line = lines[i]

        if line.startswith('```'):
            if in_code:
                blocks.append(('code', '\n'.join(code_buf)))
                code_buf = []
                in_code = False
            else:
                in_code = True
            i += 1
            continue

        if in_code:
            code_buf.append(line)
            i += 1
            continue

        if line.startswith('# ') and not line.startswith('## '):
            blocks.append(('h1', line[2:].strip()))
            i += 1
            continue

        if line.startswith('## ') and not line.startswith('### '):
            blocks.append(('h2', line[3:].strip()))
            i += 1
            continue

        if line.startswith('### ') and not line.startswith('#### '):
            blocks.append(('h3', line[4:].strip()))
            i += 1
            continue

        if line.startswith('#### '):
            blocks.append(('h4', line[5:].strip()))
            i += 1
            continue

        if line.startswith('*Table ') and line.endswith('*'):
            blocks.append(('caption', line.strip('*').strip()))
            i += 1
            continue

        if line.startswith('*Figure ') and line.endswith('*'):
            blocks.append(('caption', line.strip('*').strip()))
            i += 1
            continue

        if '|' in line and line.strip().startswith('|'):
            table_lines = []
            while i < len(lines) and '|' in lines[i] and lines[i].strip().startswith('|'):
                if not lines[i].strip().replace('|', '').replace('-', '').replace(':', '').strip() == '':
                    table_lines.append(lines[i])
                i += 1
            if table_lines:
                blocks.append(('table', table_lines))
            continue

        if line.strip().startswith('$$'):
            stripped = line.strip()
            # Single-line math: $$...$$
            if stripped.endswith('$$') and len(stripped) > 4:
                # Remove leading and trailing $$
                math_content = stripped[2:-2].strip()
                blocks.append(('math', math_content))
                i += 1
                continue
            # Multi-line math: starts with $$ on one line, ends with $$ on another
            math_lines = [stripped.lstrip('$')]
            i += 1
            while i < len(lines) and not lines[i].strip().endswith('$$'):
                math_lines.append(lines[i].strip())
                i += 1
            if i < len(lines):
                math_lines.append(lines[i].strip().rstrip('$'))
            blocks.append(('math', ' '.join(l for l in math_lines if l)))
            i += 1
            continue

        if not line.strip():
            i += 1
            continue

        para_lines = [line]
        i += 1
        while (i < len(lines) and lines[i].strip()
               and not lines[i].startswith('#')
               and not lines[i].startswith('```')
               and not lines[i].startswith('*Table ')
               and not lines[i].startswith('*Figure ')
               and not (lines[i].strip().startswith('|') and '|' in lines[i])
               and not lines[i].startswith('$$')):
            para_lines.append(lines[i])
            i += 1
        para = ' '.join(para_lines)
        blocks.append(('para', para))

    return blocks


def build_requests(blocks, start_index):
    """Build Google Docs API requests from parsed blocks.
    Also injects figure captions at the right places.
    """
    insert_requests = []
    format_requests = []
    figure_insert_points = {}  # figure_key -> index where to insert caption+image

    idx = start_index

    # Page break before chapter
    insert_requests.append({
        'insertText': {'location': {'index': idx}, 'text': '\n'}
    })
    idx += 1
    insert_requests.append({
        'insertPageBreak': {'location': {'index': idx}}
    })
    idx += 1

    for block_type, content in blocks:
        if block_type == 'h1':
            text = content.upper() + '\n'
            insert_requests.append({
                'insertText': {'location': {'index': idx}, 'text': text}
            })
            start = idx
            end = idx + len(text) - 1
            format_requests.append({
                'updateParagraphStyle': {
                    'range': {'startIndex': start, 'endIndex': end},
                    'paragraphStyle': {
                        'namedStyleType': 'HEADING_1',
                        'alignment': 'CENTER',
                        'spaceAbove': {'magnitude': 24, 'unit': 'PT'},
                        'spaceBelow': {'magnitude': 12, 'unit': 'PT'},
                    },
                    'fields': 'namedStyleType,alignment,spaceAbove,spaceBelow',
                }
            })
            format_requests.append({
                'updateTextStyle': {
                    'range': {'startIndex': start, 'endIndex': end},
                    'textStyle': {
                        'weightedFontFamily': {'fontFamily': 'Times New Roman'},
                        'fontSize': {'magnitude': 14, 'unit': 'PT'},
                        'bold': True,
                    },
                    'fields': 'weightedFontFamily,fontSize,bold',
                }
            })
            idx += len(text)

        elif block_type == 'h2':
            text = content + '\n'
            insert_requests.append({
                'insertText': {'location': {'index': idx}, 'text': text}
            })
            start = idx
            end = idx + len(text) - 1
            format_requests.append({
                'updateParagraphStyle': {
                    'range': {'startIndex': start, 'endIndex': end},
                    'paragraphStyle': {
                        'namedStyleType': 'HEADING_2',
                        'spaceAbove': {'magnitude': 18, 'unit': 'PT'},
                        'spaceBelow': {'magnitude': 8, 'unit': 'PT'},
                    },
                    'fields': 'namedStyleType,spaceAbove,spaceBelow',
                }
            })
            format_requests.append({
                'updateTextStyle': {
                    'range': {'startIndex': start, 'endIndex': end},
                    'textStyle': {
                        'weightedFontFamily': {'fontFamily': 'Times New Roman'},
                        'fontSize': {'magnitude': 13, 'unit': 'PT'},
                        'bold': True,
                    },
                    'fields': 'weightedFontFamily,fontSize,bold',
                }
            })
            idx += len(text)

        elif block_type in ('h3', 'h4'):
            text = content + '\n'
            insert_requests.append({
                'insertText': {'location': {'index': idx}, 'text': text}
            })
            start = idx
            end = idx + len(text) - 1
            format_requests.append({
                'updateParagraphStyle': {
                    'range': {'startIndex': start, 'endIndex': end},
                    'paragraphStyle': {
                        'namedStyleType': 'HEADING_3',
                        'spaceAbove': {'magnitude': 12, 'unit': 'PT'},
                        'spaceBelow': {'magnitude': 6, 'unit': 'PT'},
                    },
                    'fields': 'namedStyleType,spaceAbove,spaceBelow',
                }
            })
            format_requests.append({
                'updateTextStyle': {
                    'range': {'startIndex': start, 'endIndex': end},
                    'textStyle': {
                        'weightedFontFamily': {'fontFamily': 'Times New Roman'},
                        'fontSize': {'magnitude': 12, 'unit': 'PT'},
                        'bold': True,
                        'italic': True,
                    },
                    'fields': 'weightedFontFamily,fontSize,bold,italic',
                }
            })
            idx += len(text)

        elif block_type == 'para':
            text = content + '\n'
            insert_requests.append({
                'insertText': {'location': {'index': idx}, 'text': text}
            })
            start = idx
            end = idx + len(text) - 1

            format_requests.append({
                'updateParagraphStyle': {
                    'range': {'startIndex': start, 'endIndex': end},
                    'paragraphStyle': {
                        'namedStyleType': 'NORMAL_TEXT',
                        'lineSpacing': 150,
                        'spaceBelow': {'magnitude': 6, 'unit': 'PT'},
                        'alignment': 'JUSTIFIED',
                        'indentFirstLine': {'magnitude': 36, 'unit': 'PT'},
                    },
                    'fields': 'namedStyleType,lineSpacing,spaceBelow,alignment,indentFirstLine',
                }
            })
            format_requests.append({
                'updateTextStyle': {
                    'range': {'startIndex': start, 'endIndex': end},
                    'textStyle': {
                        'weightedFontFamily': {'fontFamily': 'Times New Roman'},
                        'fontSize': {'magnitude': 12, 'unit': 'PT'},
                    },
                    'fields': 'weightedFontFamily,fontSize',
                }
            })

            # Bold text
            for match in re.finditer(r'\*\*(.+?)\*\*', text):
                format_requests.append({
                    'updateTextStyle': {
                        'range': {'startIndex': start + match.start(), 'endIndex': start + match.end()},
                        'textStyle': {'bold': True},
                        'fields': 'bold',
                    }
                })

            # Inline code
            for match in re.finditer(r'`([^`]+)`', text):
                format_requests.append({
                    'updateTextStyle': {
                        'range': {'startIndex': start + match.start(), 'endIndex': start + match.end()},
                        'textStyle': {
                            'weightedFontFamily': {'fontFamily': 'Courier New'},
                            'fontSize': {'magnitude': 10, 'unit': 'PT'},
                        },
                        'fields': 'weightedFontFamily,fontSize',
                    }
                })

            # Inline math
            for match in re.finditer(r'\$([^$]+)\$', text):
                format_requests.append({
                    'updateTextStyle': {
                        'range': {'startIndex': start + match.start(), 'endIndex': start + match.end()},
                        'textStyle': {
                            'weightedFontFamily': {'fontFamily': 'Cambria Math'},
                            'italic': True,
                        },
                        'fields': 'weightedFontFamily,italic',
                    }
                })

            # Check if this paragraph is a figure insertion point
            for fig_key, marker_text in FIGURE_PLACEMENT.items():
                if marker_text in content:
                    figure_insert_points[fig_key] = idx + len(text)

            idx += len(text)

        elif block_type == 'caption':
            text = content + '\n'
            insert_requests.append({
                'insertText': {'location': {'index': idx}, 'text': text}
            })
            start = idx
            end = idx + len(text) - 1
            format_requests.append({
                'updateParagraphStyle': {
                    'range': {'startIndex': start, 'endIndex': end},
                    'paragraphStyle': {
                        'namedStyleType': 'NORMAL_TEXT',
                        'alignment': 'CENTER',
                        'spaceBelow': {'magnitude': 6, 'unit': 'PT'},
                        'indentFirstLine': {'magnitude': 0, 'unit': 'PT'},
                    },
                    'fields': 'namedStyleType,alignment,spaceBelow,indentFirstLine',
                }
            })
            format_requests.append({
                'updateTextStyle': {
                    'range': {'startIndex': start, 'endIndex': end},
                    'textStyle': {
                        'weightedFontFamily': {'fontFamily': 'Times New Roman'},
                        'fontSize': {'magnitude': 12, 'unit': 'PT'},
                        'italic': True,
                    },
                    'fields': 'weightedFontFamily,fontSize,italic',
                }
            })
            idx += len(text)

        elif block_type == 'code':
            text = content + '\n'
            insert_requests.append({
                'insertText': {'location': {'index': idx}, 'text': text}
            })
            start = idx
            end = idx + len(text) - 1
            format_requests.append({
                'updateParagraphStyle': {
                    'range': {'startIndex': start, 'endIndex': end},
                    'paragraphStyle': {
                        'namedStyleType': 'NORMAL_TEXT',
                        'lineSpacing': 115,
                        'spaceBelow': {'magnitude': 6, 'unit': 'PT'},
                        'spaceAbove': {'magnitude': 6, 'unit': 'PT'},
                        'indentFirstLine': {'magnitude': 0, 'unit': 'PT'},
                        'indentStart': {'magnitude': 36, 'unit': 'PT'},
                    },
                    'fields': 'namedStyleType,lineSpacing,spaceBelow,spaceAbove,indentFirstLine,indentStart',
                }
            })
            format_requests.append({
                'updateTextStyle': {
                    'range': {'startIndex': start, 'endIndex': end},
                    'textStyle': {
                        'weightedFontFamily': {'fontFamily': 'Courier New'},
                        'fontSize': {'magnitude': 9, 'unit': 'PT'},
                    },
                    'fields': 'weightedFontFamily,fontSize',
                }
            })
            idx += len(text)

        elif block_type == 'math':
            text = content + '\n'
            insert_requests.append({
                'insertText': {'location': {'index': idx}, 'text': text}
            })
            start = idx
            end = idx + len(text) - 1
            format_requests.append({
                'updateParagraphStyle': {
                    'range': {'startIndex': start, 'endIndex': end},
                    'paragraphStyle': {
                        'alignment': 'CENTER',
                        'spaceBelow': {'magnitude': 6, 'unit': 'PT'},
                        'spaceAbove': {'magnitude': 6, 'unit': 'PT'},
                        'indentFirstLine': {'magnitude': 0, 'unit': 'PT'},
                    },
                    'fields': 'alignment,spaceBelow,spaceAbove,indentFirstLine',
                }
            })
            format_requests.append({
                'updateTextStyle': {
                    'range': {'startIndex': start, 'endIndex': end},
                    'textStyle': {
                        'weightedFontFamily': {'fontFamily': 'Cambria Math'},
                        'fontSize': {'magnitude': 12, 'unit': 'PT'},
                        'italic': True,
                    },
                    'fields': 'weightedFontFamily,fontSize,italic',
                }
            })
            idx += len(text)

        elif block_type == 'table':
            for tl in content:
                cells = [c.strip() for c in tl.split('|')[1:-1]]
                row_text = '  |  '.join(cells) + '\n'
                insert_requests.append({
                    'insertText': {'location': {'index': idx}, 'text': row_text}
                })
                start = idx
                end = idx + len(row_text) - 1
                format_requests.append({
                    'updateTextStyle': {
                        'range': {'startIndex': start, 'endIndex': end},
                        'textStyle': {
                            'weightedFontFamily': {'fontFamily': 'Times New Roman'},
                            'fontSize': {'magnitude': 11, 'unit': 'PT'},
                        },
                        'fields': 'weightedFontFamily,fontSize',
                    }
                })
                format_requests.append({
                    'updateParagraphStyle': {
                        'range': {'startIndex': start, 'endIndex': end},
                        'paragraphStyle': {
                            'lineSpacing': 115,
                            'indentFirstLine': {'magnitude': 0, 'unit': 'PT'},
                        },
                        'fields': 'lineSpacing,indentFirstLine',
                    }
                })
                idx += len(row_text)

    # Now inject figure captions into the text stream
    # We need to add caption text blocks at the identified insertion points
    # Since we're building sequentially, we need to add them as additional blocks
    # Actually, we've already tracked the figure_insert_points during the build.
    # But since we built everything sequentially, the indices are "as built" positions.
    # We'll insert figures separately AFTER text insertion, using caption text search.

    return insert_requests, format_requests, figure_insert_points, idx


def execute_batch(service, requests, label=""):
    batch_size = 40
    total = len(requests)
    for i in range(0, total, batch_size):
        batch = requests[i:i+batch_size]
        try:
            service.documents().batchUpdate(
                documentId=DOC_ID,
                body={'requests': batch}
            ).execute()
            print(f"  {label} batch {i//batch_size + 1}/{(total+batch_size-1)//batch_size}: {len(batch)} OK")
        except Exception as e:
            print(f"  {label} batch {i//batch_size + 1} FAILED: {e}")
            # Try individual
            for j, req in enumerate(batch):
                try:
                    service.documents().batchUpdate(
                        documentId=DOC_ID,
                        body={'requests': [req]}
                    ).execute()
                except Exception as e2:
                    print(f"    Req {i+j} failed: {str(e2)[:100]}")
        time.sleep(2)


def insert_figure_captions_and_images(service):
    """
    After text is inserted, find the marker paragraphs and insert
    figure captions + images after them. Process in reverse order to
    avoid index shifting.
    """
    print("\nInserting figure captions and images...")

    # Process each figure: insert caption text, then image
    # Do it in reverse order (Figure 4.5 first) to avoid index drift
    fig_keys = ["Figure 4.5", "Figure 4.4", "Figure 4.3", "Figure 4.2", "Figure 4.1"]

    for fig_key in fig_keys:
        marker_text = FIGURE_PLACEMENT[fig_key]
        caption_text = FIGURE_CAPTIONS[fig_key]
        url = VISUALS[fig_key]
        width, height = IMAGE_SIZES[fig_key]

        print(f"\n  Processing {fig_key}...")

        # Re-read doc to get current indices
        doc = service.documents().get(documentId=DOC_ID).execute()
        body_content = doc['body']['content']

        # Find the marker paragraph
        insert_after_idx = None
        for elem in body_content:
            if 'paragraph' not in elem:
                continue
            text = ''
            for el in elem['paragraph'].get('elements', []):
                if 'textRun' in el:
                    text += el['textRun']['content']

            if marker_text in text:
                insert_after_idx = elem['endIndex'] - 1
                print(f"    Found marker at idx {insert_after_idx}: ...{text.strip()[-60:]}")
                break

        if insert_after_idx is None:
            print(f"    WARN: Could not find marker for {fig_key}: '{marker_text[:50]}'")
            continue

        # Insert caption text after marker paragraph
        try:
            caption_with_newline = '\n' + caption_text + '\n'
            service.documents().batchUpdate(
                documentId=DOC_ID,
                body={'requests': [{
                    'insertText': {
                        'location': {'index': insert_after_idx},
                        'text': caption_with_newline
                    }
                }]}
            ).execute()
            time.sleep(1)

            # Format caption: centered, italic, Times New Roman 12pt
            cap_start = insert_after_idx + 1  # after the \n
            cap_end = cap_start + len(caption_text)
            format_reqs = [
                {
                    'updateParagraphStyle': {
                        'range': {'startIndex': cap_start, 'endIndex': cap_end},
                        'paragraphStyle': {
                            'namedStyleType': 'NORMAL_TEXT',
                            'alignment': 'CENTER',
                            'spaceBelow': {'magnitude': 6, 'unit': 'PT'},
                            'indentFirstLine': {'magnitude': 0, 'unit': 'PT'},
                        },
                        'fields': 'namedStyleType,alignment,spaceBelow,indentFirstLine',
                    }
                },
                {
                    'updateTextStyle': {
                        'range': {'startIndex': cap_start, 'endIndex': cap_end},
                        'textStyle': {
                            'weightedFontFamily': {'fontFamily': 'Times New Roman'},
                            'fontSize': {'magnitude': 12, 'unit': 'PT'},
                            'italic': True,
                        },
                        'fields': 'weightedFontFamily,fontSize,italic',
                    }
                }
            ]
            service.documents().batchUpdate(
                documentId=DOC_ID,
                body={'requests': format_reqs}
            ).execute()
            time.sleep(1)

            # Now insert image after the caption
            # Re-read doc to find the caption we just inserted
            doc = service.documents().get(documentId=DOC_ID).execute()
            body_content = doc['body']['content']

            img_insert_idx = None
            for elem in body_content:
                if 'paragraph' not in elem:
                    continue
                text = ''
                for el in elem['paragraph'].get('elements', []):
                    if 'textRun' in el:
                        text += el['textRun']['content']
                if fig_key in text and len(text.strip()) < 250:
                    img_insert_idx = elem['endIndex']
                    break

            if img_insert_idx is None:
                print(f"    WARN: Could not find caption for image insertion")
                continue

            service.documents().batchUpdate(
                documentId=DOC_ID,
                body={'requests': [{
                    'insertInlineImage': {
                        'location': {'index': img_insert_idx},
                        'uri': url,
                        'objectSize': {
                            'width': {'magnitude': width, 'unit': 'PT'},
                            'height': {'magnitude': height, 'unit': 'PT'},
                        }
                    }
                }]}
            ).execute()
            print(f"    Inserted {fig_key} caption + image ({width}x{height}pt)")
            time.sleep(2)

        except Exception as e:
            print(f"    FAILED {fig_key}: {e}")
            time.sleep(2)


def insert_table_images(service):
    """Insert Table 4.1 and Table 4.2 images after their captions."""
    print("\nInserting table images...")

    table_keys = ["Table 4.2", "Table 4.1"]  # Reverse order

    for tbl_key in table_keys:
        url = VISUALS[tbl_key]
        width, height = IMAGE_SIZES[tbl_key]

        print(f"\n  Processing {tbl_key}...")

        doc = service.documents().get(documentId=DOC_ID).execute()
        body_content = doc['body']['content']

        # Find the caption paragraph
        insert_idx = None
        for elem in body_content:
            if 'paragraph' not in elem:
                continue
            text = ''
            for el in elem['paragraph'].get('elements', []):
                if 'textRun' in el:
                    text += el['textRun']['content']
            if tbl_key in text and ("Technology Stack" in text or "BKT Parameters" in text or "Default BKT" in text):
                insert_idx = elem['endIndex']
                print(f"    Found caption at idx {insert_idx}: {text.strip()[:80]}")
                break

        if insert_idx is None:
            print(f"    WARN: Could not find caption for {tbl_key}")
            continue

        try:
            service.documents().batchUpdate(
                documentId=DOC_ID,
                body={'requests': [{
                    'insertInlineImage': {
                        'location': {'index': insert_idx},
                        'uri': url,
                        'objectSize': {
                            'width': {'magnitude': width, 'unit': 'PT'},
                            'height': {'magnitude': height, 'unit': 'PT'},
                        }
                    }
                }]}
            ).execute()
            print(f"    Inserted {tbl_key} image ({width}x{height}pt)")
            time.sleep(2)
        except Exception as e:
            print(f"    FAILED {tbl_key}: {e}")
            time.sleep(2)


def main():
    print("=== Chapter 4 FIX: Delete & Republish with All Figures ===\n")

    service = get_service()

    # Step 1: Find Chapter 4 boundaries
    print("Step 1: Finding Chapter 4 boundaries...")
    ch4_start, ch4_end = find_chapter4_range(service)
    if ch4_start is None:
        print("FATAL: Could not find Chapter 4!")
        return
    print(f"  Chapter 4: [{ch4_start}, {ch4_end}] = {ch4_end - ch4_start} chars")

    # Step 2: Delete existing Chapter 4
    print("\nStep 2: Deleting existing Chapter 4...")
    insert_point = delete_range(service, ch4_start, ch4_end)
    time.sleep(3)

    # Step 3: Parse chapter source
    print("\nStep 3: Parsing chapter4-implementation.md...")
    blocks = parse_chapter()
    type_counts = {}
    for bt, _ in blocks:
        type_counts[bt] = type_counts.get(bt, 0) + 1
    print(f"  Parsed {len(blocks)} blocks:")
    for t, c in sorted(type_counts.items()):
        print(f"    {t}: {c}")

    # Step 4: Build requests
    print("\nStep 4: Building API requests...")
    insert_reqs, format_reqs, fig_points, final_idx = build_requests(blocks, insert_point)
    print(f"  Insert requests: {len(insert_reqs)}")
    print(f"  Format requests: {len(format_reqs)}")
    print(f"  Figure insertion points found: {list(fig_points.keys())}")
    total_chars = final_idx - insert_point
    print(f"  Total chars to insert: ~{total_chars}")

    # Step 5: Insert text
    print("\nStep 5: Inserting text...")
    execute_batch(service, insert_reqs, "INSERT")
    time.sleep(3)

    # Step 6: Apply formatting
    print("\nStep 6: Applying formatting...")
    execute_batch(service, format_reqs, "FORMAT")
    time.sleep(3)

    # Step 7: Insert table images
    print("\nStep 7: Inserting table images...")
    insert_table_images(service)
    time.sleep(2)

    # Step 8: Insert figure captions and images
    print("\nStep 8: Inserting figure captions and images...")
    insert_figure_captions_and_images(service)

    # Step 9: Verify
    print("\n\nStep 9: Verification...")
    doc = service.documents().get(documentId=DOC_ID).execute()
    body = doc['body']['content']
    total_size = body[-1]['endIndex']
    print(f"  Document total size: {total_size} chars")

    # Check for chapter 4 heading
    ch4_found = False
    headings_found = []
    images_found = 0
    figure_captions_found = []
    for elem in body:
        if 'paragraph' in elem:
            text = ''
            has_img = False
            for el in elem['paragraph'].get('elements', []):
                if 'textRun' in el:
                    text += el['textRun']['content']
                if 'inlineObjectElement' in el:
                    has_img = True
            style = elem['paragraph'].get('paragraphStyle', {}).get('namedStyleType', '')
            text_stripped = text.strip()

            if 'CHAPTER 4' in text_stripped.upper() and 'HEADING' in style:
                ch4_found = True
            if 'HEADING' in style and ('4.' in text_stripped[:4] or text_stripped.startswith('Chapter Summary')):
                headings_found.append(text_stripped[:50])
            if has_img:
                images_found += 1
            if 'Figure 4.' in text_stripped and len(text_stripped) < 250:
                figure_captions_found.append(text_stripped[:80])

    print(f"  Chapter 4 heading: {'FOUND' if ch4_found else 'MISSING'}")
    print(f"  Section headings found: {len(headings_found)}")
    for h in headings_found:
        print(f"    - {h}")
    print(f"  Inline images in Ch4 area: {images_found}")
    print(f"  Figure captions found: {len(figure_captions_found)}")
    for fc in figure_captions_found:
        print(f"    - {fc}")

    print("\n=== DONE ===")


if __name__ == '__main__':
    main()
