"""
Publish Chapter 4 (Implementation) to Google Docs.
Appends after existing content with proper formatting.
"""
import warnings
warnings.filterwarnings("ignore")

import json
import re
import time
from google.oauth2 import service_account
from googleapiclient.discovery import build

KEY_FILE = "/Users/avada/WebstormProjects/Thesis/infra-inkwell-465003-f2-369235afe5ac.json"
DOC_ID = "1O4wJNovNTFjD5DORC-WOJ2AftbcjfyoQ6HuzRSlYFfA"
SCOPES = ['https://www.googleapis.com/auth/documents', 'https://www.googleapis.com/auth/drive']

# Visual URLs from catbox
VISUALS = {
    "Table 4.1": "https://files.catbox.moe/7nj9z8.png",
    "Table 4.2": "https://files.catbox.moe/0005w3.png",
    "Figure 4.1": "https://files.catbox.moe/vq16l2.png",
    "Figure 4.2": "https://files.catbox.moe/0pk8fv.png",
    "Figure 4.3": "https://files.catbox.moe/vbzbwp.png",
    "Figure 4.4": "https://files.catbox.moe/3yojqt.png",
    "Figure 4.5": "https://files.catbox.moe/4g1sh7.png",
}

# Image dimensions (width in PT, ~468pt = 6.5 inches)
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


def get_doc_end(service):
    doc = service.documents().get(documentId=DOC_ID).execute()
    content = doc['body']['content']
    return content[-1]['endIndex']


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

        # Code block toggle
        if line.startswith('```'):
            if in_code:
                # End code block
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

        # Chapter heading
        if line.startswith('# ') and not line.startswith('## '):
            blocks.append(('h1', line[2:].strip()))
            i += 1
            continue

        # Section heading (##)
        if line.startswith('## ') and not line.startswith('### '):
            blocks.append(('h2', line[3:].strip()))
            i += 1
            continue

        # Subsection heading (###)
        if line.startswith('### ') and not line.startswith('#### '):
            blocks.append(('h3', line[4:].strip()))
            i += 1
            continue

        # Sub-subsection heading (####)
        if line.startswith('#### '):
            blocks.append(('h4', line[5:].strip()))
            i += 1
            continue

        # Table caption lines (italic)
        if line.startswith('*Table ') and line.endswith('*'):
            blocks.append(('caption', line.strip('*').strip()))
            i += 1
            continue

        # Markdown table
        if '|' in line and line.strip().startswith('|'):
            table_lines = []
            while i < len(lines) and '|' in lines[i] and lines[i].strip().startswith('|'):
                if not lines[i].strip().replace('|', '').replace('-', '').replace(':', '').strip() == '':
                    table_lines.append(lines[i])
                i += 1
            if table_lines:
                blocks.append(('table', table_lines))
            continue

        # Math display ($$)
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

        # Empty line
        if not line.strip():
            i += 1
            continue

        # Regular paragraph (collect multi-line)
        para_lines = [line]
        i += 1
        while i < len(lines) and lines[i].strip() and not lines[i].startswith('#') and not lines[i].startswith('```') and not lines[i].startswith('*Table ') and not (lines[i].strip().startswith('|') and '|' in lines[i]) and not lines[i].startswith('$$'):
            para_lines.append(lines[i])
            i += 1
        para = ' '.join(para_lines)
        blocks.append(('para', para))

    return blocks


def build_requests(blocks, start_index):
    """Build Google Docs API requests from parsed blocks."""
    insert_requests = []
    format_requests = []
    image_insertions = []  # (index, visual_key, caption)

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
    idx += 1  # page break takes 1 char

    for block_type, content in blocks:
        if block_type == 'h1':
            # Chapter heading
            text = content.upper() + '\n'
            insert_requests.append({
                'insertText': {
                    'location': {'index': idx},
                    'text': text
                }
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
                'insertText': {
                    'location': {'index': idx},
                    'text': text
                }
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
                'insertText': {
                    'location': {'index': idx},
                    'text': text
                }
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
            # Clean up markdown inline formatting for plain text
            clean = content
            # Remove markdown bold/italic markers for now (we'll add formatting later)
            # Keep the text content
            text = clean + '\n'
            insert_requests.append({
                'insertText': {
                    'location': {'index': idx},
                    'text': text
                }
            })
            start = idx
            end = idx + len(text) - 1

            # Body paragraph formatting
            format_requests.append({
                'updateParagraphStyle': {
                    'range': {'startIndex': start, 'endIndex': end},
                    'paragraphStyle': {
                        'namedStyleType': 'NORMAL_TEXT',
                        'lineSpacing': 150,
                        'spaceAfter': {'magnitude': 6, 'unit': 'PT'},
                        'alignment': 'JUSTIFIED',
                        'indentFirstLine': {'magnitude': 36, 'unit': 'PT'},
                    },
                    'fields': 'namedStyleType,lineSpacing,spaceAfter,alignment,indentFirstLine',
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

            # Handle bold text within paragraph
            bold_pattern = re.compile(r'\*\*(.+?)\*\*')
            for match in bold_pattern.finditer(text):
                b_start = start + match.start()
                b_end = start + match.end()
                format_requests.append({
                    'updateTextStyle': {
                        'range': {'startIndex': b_start, 'endIndex': b_end},
                        'textStyle': {'bold': True},
                        'fields': 'bold',
                    }
                })

            # Handle inline code
            code_pattern = re.compile(r'`([^`]+)`')
            for match in code_pattern.finditer(text):
                c_start = start + match.start()
                c_end = start + match.end()
                format_requests.append({
                    'updateTextStyle': {
                        'range': {'startIndex': c_start, 'endIndex': c_end},
                        'textStyle': {
                            'weightedFontFamily': {'fontFamily': 'Courier New'},
                            'fontSize': {'magnitude': 10, 'unit': 'PT'},
                        },
                        'fields': 'weightedFontFamily,fontSize',
                    }
                })

            # Handle $math$ inline
            math_pattern = re.compile(r'\$([^$]+)\$')
            for match in math_pattern.finditer(text):
                m_start = start + match.start()
                m_end = start + match.end()
                format_requests.append({
                    'updateTextStyle': {
                        'range': {'startIndex': m_start, 'endIndex': m_end},
                        'textStyle': {
                            'weightedFontFamily': {'fontFamily': 'Cambria Math'},
                            'italic': True,
                        },
                        'fields': 'weightedFontFamily,italic',
                    }
                })

            # Check if this paragraph should have an image after it
            for vis_key in VISUALS:
                if vis_key in content and vis_key.startswith("Table"):
                    # Insert image after this caption-like paragraph
                    image_insertions.append((idx + len(text), vis_key))
                    break

            idx += len(text)

        elif block_type == 'caption':
            text = content + '\n'
            insert_requests.append({
                'insertText': {
                    'location': {'index': idx},
                    'text': text
                }
            })
            start = idx
            end = idx + len(text) - 1
            format_requests.append({
                'updateParagraphStyle': {
                    'range': {'startIndex': start, 'endIndex': end},
                    'paragraphStyle': {
                        'namedStyleType': 'NORMAL_TEXT',
                        'alignment': 'CENTER',
                        'spaceAfter': {'magnitude': 6, 'unit': 'PT'},
                        'indentFirstLine': {'magnitude': 0, 'unit': 'PT'},
                    },
                    'fields': 'namedStyleType,alignment,spaceAfter,indentFirstLine',
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

            # Insert visual image after caption
            for vis_key in VISUALS:
                if vis_key in content:
                    image_insertions.append((idx + len(text), vis_key))
                    break

            idx += len(text)

        elif block_type == 'code':
            text = content + '\n'
            insert_requests.append({
                'insertText': {
                    'location': {'index': idx},
                    'text': text
                }
            })
            start = idx
            end = idx + len(text) - 1
            format_requests.append({
                'updateParagraphStyle': {
                    'range': {'startIndex': start, 'endIndex': end},
                    'paragraphStyle': {
                        'namedStyleType': 'NORMAL_TEXT',
                        'lineSpacing': 115,
                        'spaceAfter': {'magnitude': 6, 'unit': 'PT'},
                        'spaceBefore': {'magnitude': 6, 'unit': 'PT'},
                        'indentFirstLine': {'magnitude': 0, 'unit': 'PT'},
                        'indentStart': {'magnitude': 36, 'unit': 'PT'},
                    },
                    'fields': 'namedStyleType,lineSpacing,spaceAfter,spaceBefore,indentFirstLine,indentStart',
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
                'insertText': {
                    'location': {'index': idx},
                    'text': text
                }
            })
            start = idx
            end = idx + len(text) - 1
            format_requests.append({
                'updateParagraphStyle': {
                    'range': {'startIndex': start, 'endIndex': end},
                    'paragraphStyle': {
                        'alignment': 'CENTER',
                        'spaceAfter': {'magnitude': 6, 'unit': 'PT'},
                        'spaceBefore': {'magnitude': 6, 'unit': 'PT'},
                        'indentFirstLine': {'magnitude': 0, 'unit': 'PT'},
                    },
                    'fields': 'alignment,spaceAfter,spaceBefore,indentFirstLine',
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
            # Convert markdown table to plain text (aligned)
            rows = []
            for tl in content:
                cells = [c.strip() for c in tl.split('|')[1:-1]]
                rows.append(cells)
            if rows:
                # Insert as formatted text (native GDoc tables are complex)
                for row in rows:
                    row_text = '  |  '.join(row) + '\n'
                    insert_requests.append({
                        'insertText': {
                            'location': {'index': idx},
                            'text': row_text
                        }
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

    return insert_requests, format_requests, image_insertions, idx


def execute_batch(service, requests, label=""):
    """Execute requests in batches of 40 with delay."""
    batch_size = 40
    total = len(requests)
    for i in range(0, total, batch_size):
        batch = requests[i:i+batch_size]
        try:
            service.documents().batchUpdate(
                documentId=DOC_ID,
                body={'requests': batch}
            ).execute()
            print(f"  {label} batch {i//batch_size + 1}/{(total+batch_size-1)//batch_size}: {len(batch)} requests OK")
        except Exception as e:
            print(f"  {label} batch {i//batch_size + 1} FAILED: {e}")
            # Try individual requests
            for j, req in enumerate(batch):
                try:
                    service.documents().batchUpdate(
                        documentId=DOC_ID,
                        body={'requests': [req]}
                    ).execute()
                except Exception as e2:
                    print(f"    Request {i+j} failed: {e2}")
        time.sleep(2)


def insert_images(service, image_insertions):
    """Insert images from last to first to avoid index shifting."""
    # We need to re-read the doc to get current indices after text insertion
    # Instead, insert images one at a time with doc re-read
    if not image_insertions:
        return

    print(f"\nInserting {len(image_insertions)} images...")

    # Since we inserted text, we need to find the caption text in the doc
    # and insert images after it. Process from last to first.
    doc = service.documents().get(documentId=DOC_ID).execute()
    body_content = doc['body']['content']

    for vis_key in reversed(list(VISUALS.keys())):
        url = VISUALS[vis_key]
        width, height = IMAGE_SIZES.get(vis_key, (468, 300))

        # Find the caption text in the document
        caption_text = vis_key  # e.g., "Table 4.1" or "Figure 4.1"
        insert_idx = None

        for elem in body_content:
            if 'paragraph' in elem:
                para_text = ''
                for el in elem['paragraph'].get('elements', []):
                    if 'textRun' in el:
                        para_text += el['textRun']['content']

                if caption_text in para_text and ("Table 4." in para_text or "Figure 4." in para_text):
                    # For captions that start with "Table 4.x." or contain figure references
                    # Insert image after this paragraph
                    insert_idx = elem['endIndex'] - 1
                    break

        if insert_idx is None:
            print(f"  Could not find insertion point for {vis_key}, skipping")
            continue

        try:
            # Insert a newline first, then the image
            service.documents().batchUpdate(
                documentId=DOC_ID,
                body={'requests': [
                    {
                        'insertText': {
                            'location': {'index': insert_idx},
                            'text': '\n'
                        }
                    }
                ]}
            ).execute()
            time.sleep(1)

            # Re-read doc to get updated index
            doc = service.documents().get(documentId=DOC_ID).execute()
            body_content = doc['body']['content']

            # Find the new index after the newline
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
                body={'requests': [
                    {
                        'insertInlineImage': {
                            'location': {'index': insert_idx},
                            'uri': url,
                            'objectSize': {
                                'width': {'magnitude': width, 'unit': 'PT'},
                                'height': {'magnitude': height, 'unit': 'PT'},
                            }
                        }
                    }
                ]}
            ).execute()
            print(f"  Inserted {vis_key}: {url} ({width}x{height}pt)")

            # Center the image paragraph
            doc = service.documents().get(documentId=DOC_ID).execute()
            body_content = doc['body']['content']

            time.sleep(2)

        except Exception as e:
            print(f"  Failed to insert {vis_key}: {e}")
            # Re-read doc for next iteration
            doc = service.documents().get(documentId=DOC_ID).execute()
            body_content = doc['body']['content']
            time.sleep(2)


def main():
    print("=== Chapter 4 Publishing Pipeline ===\n")

    # Step 1: Parse chapter
    print("Step 1: Parsing chapter4-implementation.md...")
    blocks = parse_chapter()
    print(f"  Parsed {len(blocks)} blocks:")
    type_counts = {}
    for bt, _ in blocks:
        type_counts[bt] = type_counts.get(bt, 0) + 1
    for t, c in sorted(type_counts.items()):
        print(f"    {t}: {c}")

    # Step 2: Connect to Google Docs
    print("\nStep 2: Connecting to Google Docs API...")
    service = get_service()
    end_index = get_doc_end(service)
    print(f"  Document end index: {end_index}")

    # Step 3: Build requests
    print("\nStep 3: Building API requests...")
    insert_reqs, format_reqs, image_inserts, final_idx = build_requests(blocks, end_index - 1)
    print(f"  Insert requests: {len(insert_reqs)}")
    print(f"  Format requests: {len(format_reqs)}")
    print(f"  Image insertions: {len(image_inserts)}")
    total_chars = final_idx - (end_index - 1)
    print(f"  Total characters to insert: ~{total_chars}")

    # Step 4: Insert text
    print("\nStep 4: Inserting text...")
    execute_batch(service, insert_reqs, "INSERT")

    # Step 5: Apply formatting
    print("\nStep 5: Applying formatting...")
    execute_batch(service, format_reqs, "FORMAT")

    # Step 6: Insert images
    print("\nStep 6: Inserting images...")
    insert_images(service, image_inserts)

    # Step 7: Verify
    print("\nStep 7: Verifying...")
    new_end = get_doc_end(service)
    print(f"  Document end index: {end_index} -> {new_end}")
    print(f"  Characters added: {new_end - end_index}")

    print("\n=== Chapter 4 publishing complete ===")


if __name__ == '__main__':
    main()
