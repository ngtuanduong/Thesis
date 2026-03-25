"""
Publish Chapter 5 to Google Docs - insert ABOVE the References section.
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
CH5_FILE = "C:/Users/duong/WebstormProjects/Thesis/documents/thesis-chapters/chapter5-evaluation.md"

VISUALS = {
    "Table 5.1": "https://files.catbox.moe/2llwwm.png",
    "Table 5.2": "https://files.catbox.moe/wjmwg9.png",
    "Table 5.3": "https://files.catbox.moe/ukyi05.png",
    "Figure 5.1": "https://files.catbox.moe/xaopkb.png",
}

IMAGE_SIZES = {
    "Table 5.1": (468, 158),    # 920x311 -> scale to 468pt width
    "Table 5.2": (468, 170),    # 920x333
    "Table 5.3": (468, 332),    # 941x666
    "Figure 5.1": (468, 184),   # 818x322
}


def get_service():
    creds = service_account.Credentials.from_service_account_file(KEY_FILE, scopes=SCOPES)
    return build('docs', 'v1', credentials=creds)


def find_references_index(service):
    """Find the start index of the References section."""
    doc = service.documents().get(documentId=DOC_ID).execute()
    body = doc['body']['content']

    for elem in body:
        if 'paragraph' not in elem:
            continue
        text = ''
        for el in elem['paragraph'].get('elements', []):
            if 'textRun' in el:
                text += el['textRun']['content']
        text_upper = text.strip().upper()
        style = elem['paragraph'].get('paragraphStyle', {}).get('namedStyleType', '')

        if ('REFERENCE' in text_upper or 'BIBLIOGRAPHY' in text_upper) and 'HEADING' in style:
            idx = elem['startIndex']
            print(f"  Found References heading at index {idx}: '{text.strip()[:80]}'")
            return idx

    # Fallback: search for "Reference" in heading-styled paragraphs
    for elem in body:
        if 'paragraph' not in elem:
            continue
        text = ''
        for el in elem['paragraph'].get('elements', []):
            if 'textRun' in el:
                text += el['textRun']['content']
        if 'reference' in text.strip().lower()[:20] and 'HEADING' in elem['paragraph'].get('paragraphStyle', {}).get('namedStyleType', ''):
            idx = elem['startIndex']
            print(f"  Found References (fallback) at index {idx}: '{text.strip()[:80]}'")
            return idx

    print("  WARNING: Could not find References section!")
    return None


def parse_chapter():
    """Parse chapter5-evaluation.md into structured blocks."""
    with open(CH5_FILE, encoding='utf-8') as f:
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
                math_content = stripped[2:-2].strip()
                blocks.append(('math', math_content))
                i += 1
                continue
            # Multi-line math
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
    """Build Google Docs API requests from parsed blocks."""
    insert_requests = []
    format_requests = []
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

            # Bold text **...**
            for match in re.finditer(r'\*\*(.+?)\*\*', text):
                format_requests.append({
                    'updateTextStyle': {
                        'range': {'startIndex': start + match.start(), 'endIndex': start + match.end()},
                        'textStyle': {'bold': True},
                        'fields': 'bold',
                    }
                })

            # Inline code `...`
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

            # Inline math $...$
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

    return insert_requests, format_requests, idx


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


def insert_images(service):
    """Insert images after their caption paragraphs, in reverse order."""
    print("\nInserting images...")

    # Process in reverse to avoid index drift
    visual_keys = ["Table 5.3", "Table 5.2", "Figure 5.1", "Table 5.1"]

    for vis_key in visual_keys:
        url = VISUALS[vis_key]
        width, height = IMAGE_SIZES[vis_key]

        print(f"\n  Processing {vis_key}...")

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
            # Match caption text
            if vis_key in text and len(text.strip()) < 200:
                insert_idx = elem['endIndex']
                print(f"    Found caption at idx {insert_idx}: {text.strip()[:80]}")
                break

        if insert_idx is None:
            print(f"    WARN: Could not find caption for {vis_key}")
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
            print(f"    Inserted {vis_key} image ({width}x{height}pt)")
            time.sleep(2)
        except Exception as e:
            print(f"    FAILED {vis_key}: {e}")
            time.sleep(2)


def main():
    print("=== Chapter 5: Publish to Google Docs (ABOVE References) ===\n")

    service = get_service()

    # Step 1: Find References section
    print("Step 1: Finding References section...")
    ref_index = find_references_index(service)
    if ref_index is None:
        print("FATAL: Could not find References section!")
        return
    print(f"  Will insert Chapter 5 before index {ref_index}")

    # Step 2: Parse chapter source
    print("\nStep 2: Parsing chapter5-evaluation.md...")
    blocks = parse_chapter()
    type_counts = {}
    for bt, _ in blocks:
        type_counts[bt] = type_counts.get(bt, 0) + 1
    print(f"  Parsed {len(blocks)} blocks:")
    for t, c in sorted(type_counts.items()):
        print(f"    {t}: {c}")

    # Step 3: Build requests
    print("\nStep 3: Building API requests...")
    insert_reqs, format_reqs, final_idx = build_requests(blocks, ref_index)
    print(f"  Insert requests: {len(insert_reqs)}")
    print(f"  Format requests: {len(format_reqs)}")
    total_chars = final_idx - ref_index
    print(f"  Total chars to insert: ~{total_chars}")

    # Step 4: Insert text
    print("\nStep 4: Inserting text...")
    execute_batch(service, insert_reqs, "INSERT")
    time.sleep(3)

    # Step 5: Apply formatting
    print("\nStep 5: Applying formatting...")
    execute_batch(service, format_reqs, "FORMAT")
    time.sleep(3)

    # Step 6: Insert images
    print("\nStep 6: Inserting images...")
    insert_images(service)

    # Step 7: Verify
    print("\n\nStep 7: Verification...")
    doc = service.documents().get(documentId=DOC_ID).execute()
    body = doc['body']['content']
    total_size = body[-1]['endIndex']
    print(f"  Document total size: {total_size} chars")

    ch5_found = False
    headings_found = []
    images_found = 0
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

            if 'CHAPTER 5' in text_stripped.upper() and 'HEADING' in style:
                ch5_found = True
            if 'HEADING' in style and ('5.' in text_stripped[:4] or text_stripped.startswith('Chapter Summary')):
                headings_found.append(text_stripped[:50])
            if has_img:
                images_found += 1

    print(f"  Chapter 5 heading: {'FOUND' if ch5_found else 'MISSING'}")
    print(f"  Section headings found: {len(headings_found)}")
    for h in headings_found:
        print(f"    - {h}")
    print(f"  Total inline images in document: {images_found}")

    print("\n=== DONE ===")


if __name__ == '__main__':
    main()
