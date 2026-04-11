"""
Republish Chapter 4 (Implementation) to Google Docs with humanized text.
1. Find Chapter 4 start/end in the document
2. Delete existing Chapter 4 content
3. Re-insert humanized content with proper formatting
4. Re-insert images
"""
import warnings
warnings.filterwarnings("ignore")

import re
import time
from google.oauth2 import service_account
from googleapiclient.discovery import build

KEY_FILE = "/Users/avada/WebstormProjects/Thesis/infra-inkwell-465003-f2-369235afe5ac.json"
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


def get_service():
    creds = service_account.Credentials.from_service_account_file(KEY_FILE, scopes=SCOPES)
    return build('docs', 'v1', credentials=creds)


def find_chapter4_range(service):
    """Find the start and end indices of Chapter 4 in the doc."""
    doc = service.documents().get(documentId=DOC_ID).execute()
    body = doc['body']['content']

    ch4_start = None
    ch4_end = None

    for elem in body:
        if 'paragraph' not in elem:
            continue
        para = elem['paragraph']
        text = ''
        for el in para.get('elements', []):
            if 'textRun' in el:
                text += el['textRun']['content']

        text_clean = text.strip().upper()

        # Find Chapter 4 heading
        if ch4_start is None:
            if 'CHAPTER 4' in text_clean and ('IMPLEMENTATION' in text_clean or text_clean.startswith('CHAPTER 4')):
                ch4_start = elem['startIndex']
                print(f"  Found Chapter 4 start at index {ch4_start}: {text.strip()[:60]}")

        # Find Chapter 5 heading (or References or end of doc) - this marks end of Ch4
        elif ch4_end is None:
            if ('CHAPTER 5' in text_clean) or ('REFERENCES' == text_clean) or ('BIBLIOGRAPHY' == text_clean):
                ch4_end = elem['startIndex']
                print(f"  Found Chapter 4 end at index {ch4_end}: {text.strip()[:60]}")
                break

    if ch4_start is None:
        print("  ERROR: Could not find Chapter 4!")
        return None, None

    if ch4_end is None:
        # Chapter 4 goes to end of doc
        ch4_end = body[-1]['endIndex'] - 1
        print(f"  Chapter 4 extends to doc end: {ch4_end}")

    return ch4_start, ch4_end


def delete_chapter4(service, start, end):
    """Delete existing Chapter 4 content from the doc."""
    # We need to also delete the page break before chapter 4 heading
    # Go back 1-2 chars to catch the page break
    actual_start = max(1, start - 1)

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
        print("  Delete successful")
        return actual_start
    except Exception as e:
        print(f"  Delete failed: {e}")
        # Try without the page break
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
        print("  Delete successful (without page break)")
        return start


def parse_chapter():
    """Parse chapter4-implementation.md into structured blocks."""
    with open("/Users/avada/WebstormProjects/Thesis/documents/thesis-chapters/chapter4-implementation.md") as f:
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
            math_lines = [line.strip().lstrip('$')]
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
        'insertText': {
            'location': {'index': idx},
            'text': '\n'
        }
    })
    idx += 1
    insert_requests.append({
        'insertPageBreak': {
            'location': {'index': idx}
        }
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
            for j, req in enumerate(batch):
                try:
                    service.documents().batchUpdate(
                        documentId=DOC_ID,
                        body={'requests': [req]}
                    ).execute()
                except Exception as e2:
                    print(f"    Request {i+j} failed: {e2}")
        time.sleep(2)


def insert_images(service):
    """Insert images by finding caption text and inserting after it."""
    print(f"\nInserting {len(VISUALS)} images...")

    for vis_key in reversed(list(VISUALS.keys())):
        url = VISUALS[vis_key]
        width, height = IMAGE_SIZES.get(vis_key, (468, 300))

        doc = service.documents().get(documentId=DOC_ID).execute()
        body_content = doc['body']['content']

        caption_text = vis_key
        insert_idx = None

        for elem in body_content:
            if 'paragraph' in elem:
                para_text = ''
                for el in elem['paragraph'].get('elements', []):
                    if 'textRun' in el:
                        para_text += el['textRun']['content']

                if caption_text in para_text and ("Table 4." in para_text or "Figure 4." in para_text):
                    insert_idx = elem['endIndex'] - 1
                    break

        if insert_idx is None:
            print(f"  Could not find caption for {vis_key}, skipping")
            continue

        try:
            service.documents().batchUpdate(
                documentId=DOC_ID,
                body={'requests': [{
                    'insertText': {
                        'location': {'index': insert_idx},
                        'text': '\n'
                    }
                }]}
            ).execute()
            time.sleep(1)

            doc = service.documents().get(documentId=DOC_ID).execute()
            body_content = doc['body']['content']

            for elem in body_content:
                if 'paragraph' in elem:
                    para_text = ''
                    for el in elem['paragraph'].get('elements', []):
                        if 'textRun' in el:
                            para_text += el['textRun']['content']
                    if caption_text in para_text:
                        insert_idx = elem['endIndex']
                        break

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
            print(f"  Inserted {vis_key}: {width}x{height}pt")
            time.sleep(2)

        except Exception as e:
            print(f"  Failed to insert {vis_key}: {e}")
            time.sleep(2)


def main():
    print("=== Chapter 4 REPUBLISH (Humanized) ===\n")

    service = get_service()

    # Step 1: Find Chapter 4 boundaries
    print("Step 1: Finding Chapter 4 in document...")
    ch4_start, ch4_end = find_chapter4_range(service)
    if ch4_start is None:
        print("FATAL: Cannot find Chapter 4 in document!")
        return

    print(f"  Chapter 4 spans indices [{ch4_start}, {ch4_end}] = {ch4_end - ch4_start} chars")

    # Step 2: Delete existing Chapter 4
    print("\nStep 2: Deleting existing Chapter 4 content...")
    insert_point = delete_chapter4(service, ch4_start, ch4_end)
    time.sleep(3)

    # Step 3: Parse humanized chapter
    print("\nStep 3: Parsing humanized chapter4-implementation.md...")
    blocks = parse_chapter()
    type_counts = {}
    for bt, _ in blocks:
        type_counts[bt] = type_counts.get(bt, 0) + 1
    print(f"  Parsed {len(blocks)} blocks:")
    for t, c in sorted(type_counts.items()):
        print(f"    {t}: {c}")

    # Step 4: Build requests
    print("\nStep 4: Building API requests...")
    insert_reqs, format_reqs, final_idx = build_requests(blocks, insert_point)
    print(f"  Insert requests: {len(insert_reqs)}")
    print(f"  Format requests: {len(format_reqs)}")

    # Step 5: Insert text
    print("\nStep 5: Inserting humanized text...")
    execute_batch(service, insert_reqs, "INSERT")
    time.sleep(3)

    # Step 6: Apply formatting
    print("\nStep 6: Applying formatting...")
    execute_batch(service, format_reqs, "FORMAT")
    time.sleep(3)

    # Step 7: Insert images
    print("\nStep 7: Inserting images...")
    insert_images(service)

    # Step 8: Verify
    print("\nStep 8: Verification...")
    doc = service.documents().get(documentId=DOC_ID).execute()
    body = doc['body']['content']
    total_chars = body[-1]['endIndex']
    print(f"  Document total size: {total_chars} chars")

    ch4_found = False
    for elem in body:
        if 'paragraph' in elem:
            text = ''
            for el in elem['paragraph'].get('elements', []):
                if 'textRun' in el:
                    text += el['textRun']['content']
            if 'CHAPTER 4' in text.upper() and 'IMPLEMENTATION' in text.upper():
                ch4_found = True
                break
    print(f"  Chapter 4 heading found: {ch4_found}")
    print("\n=== DONE ===")


if __name__ == '__main__':
    main()
