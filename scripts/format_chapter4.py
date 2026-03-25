"""
Apply formatting to Chapter 4 in Google Docs.
Reads the document to find headings, paragraphs, code blocks, etc.
and applies proper formatting.
"""
import warnings
warnings.filterwarnings("ignore")

import re
import time
from google.oauth2 import service_account
from googleapiclient.discovery import build

KEY_FILE = "/Users/avada/WebstormProjects/Thesis/infra-inkwell-465003-f2-369235afe5ac.json"
DOC_ID = "1O4wJNovNTFjD5DORC-WOJ2AftbcjfyoQ6HuzRSlYFfA"
SCOPES = ['https://www.googleapis.com/auth/documents']

CH4_START = 153522  # Where Chapter 4 starts

# Visual URLs
VISUALS = {
    "Table 4.1": ("https://files.catbox.moe/7nj9z8.png", 468, 170),
    "Table 4.2": ("https://files.catbox.moe/0005w3.png", 420, 165),
    "Figure 4.1": ("https://files.catbox.moe/vq16l2.png", 468, 358),
    "Figure 4.2": ("https://files.catbox.moe/0pk8fv.png", 400, 280),
    "Figure 4.3": ("https://files.catbox.moe/vbzbwp.png", 468, 433),
    "Figure 4.4": ("https://files.catbox.moe/3yojqt.png", 450, 316),
    "Figure 4.5": ("https://files.catbox.moe/4g1sh7.png", 430, 300),
}


def get_service():
    creds = service_account.Credentials.from_service_account_file(KEY_FILE, scopes=SCOPES)
    return build('docs', 'v1', credentials=creds)


def safe_batch(service, requests, label=""):
    """Execute batch with retry on rate limit."""
    max_retries = 3
    for attempt in range(max_retries):
        try:
            service.documents().batchUpdate(
                documentId=DOC_ID,
                body={'requests': requests}
            ).execute()
            return True
        except Exception as e:
            err_str = str(e)
            if '429' in err_str or 'RATE_LIMIT' in err_str:
                wait = 30 * (attempt + 1)
                print(f"    Rate limited, waiting {wait}s...")
                time.sleep(wait)
            else:
                print(f"    Error in {label}: {err_str[:200]}")
                return False
    return False


def get_paragraphs(service):
    """Get all paragraphs in Chapter 4 region."""
    doc = service.documents().get(documentId=DOC_ID).execute()
    content = doc['body']['content']

    paragraphs = []
    for elem in content:
        start = elem.get('startIndex', 0)
        end = elem.get('endIndex', 0)
        if start < CH4_START:
            continue

        if 'paragraph' in elem:
            text = ''
            for el in elem['paragraph'].get('elements', []):
                if 'textRun' in el:
                    text += el['textRun']['content']

            paragraphs.append({
                'start': start,
                'end': end,
                'text': text,
                'style': elem['paragraph'].get('paragraphStyle', {}),
            })

    return paragraphs


def classify_paragraph(text):
    """Classify paragraph type from its text content."""
    stripped = text.strip()
    if not stripped:
        return 'empty'
    if stripped.startswith('CHAPTER 4'):
        return 'h1'
    # H2: "4.X Something" pattern at start (no sub-sub)
    if re.match(r'^4\.\d+\s+\w', stripped) and not re.match(r'^4\.\d+\.\d+', stripped):
        return 'h2'
    # H3: "4.X.Y Something" pattern
    if re.match(r'^4\.\d+\.\d+\s+\w', stripped):
        return 'h3'
    # Code: starts with common code patterns
    if stripped.startswith('def ') or stripped.startswith('class ') or stripped.startswith('async def'):
        return 'code_start'
    if stripped.startswith('import ') or stripped.startswith('from '):
        return 'code_start'
    # Check for code-like content (indented, has syntax)
    if any(stripped.startswith(p) for p in ['p_l', 'p_g', 'p_s', 'if ', 'else:', 'for ', 'return ', 'await ', '#']):
        return 'code'
    # Captions
    if stripped.startswith('Table 4.') and '.' in stripped[8:]:
        return 'caption'
    # Math display
    if '$$' in stripped or (stripped.startswith('E(') or stripped.startswith('R(') or stripped.startswith('R\'') or stripped.startswith('S\'')):
        return 'math'
    # SQL-like
    if stripped.startswith('concepts (') or stripped.startswith('knowledge_graph_edges (') or stripped.startswith('problem_concepts ('):
        return 'code'
    # Table-like rows (contains |)
    if '  |  ' in stripped:
        return 'table_row'

    return 'para'


def build_format_requests(paragraphs):
    """Build formatting requests for all Chapter 4 paragraphs."""
    requests = []

    # First: set all of Chapter 4 to Times New Roman 12pt as base
    last_end = max(p['end'] for p in paragraphs) if paragraphs else CH4_START + 1
    requests.append({
        'updateTextStyle': {
            'range': {'startIndex': CH4_START, 'endIndex': last_end - 1},
            'textStyle': {
                'weightedFontFamily': {'fontFamily': 'Times New Roman'},
                'fontSize': {'magnitude': 12, 'unit': 'PT'},
            },
            'fields': 'weightedFontFamily,fontSize',
        }
    })

    # Default paragraph style for all
    requests.append({
        'updateParagraphStyle': {
            'range': {'startIndex': CH4_START, 'endIndex': last_end - 1},
            'paragraphStyle': {
                'lineSpacing': 150,
                'alignment': 'JUSTIFIED',
                'indentFirstLine': {'magnitude': 36, 'unit': 'PT'},
            },
            'fields': 'lineSpacing,alignment,indentFirstLine',
        }
    })

    in_code_block = False

    for p in paragraphs:
        text = p['text']
        start = p['start']
        end = p['end'] - 1  # exclude trailing newline from range
        ptype = classify_paragraph(text)

        if end <= start:
            continue

        if ptype == 'h1':
            requests.append({
                'updateParagraphStyle': {
                    'range': {'startIndex': start, 'endIndex': end},
                    'paragraphStyle': {
                        'namedStyleType': 'HEADING_1',
                        'alignment': 'CENTER',
                        'indentFirstLine': {'magnitude': 0, 'unit': 'PT'},
                    },
                    'fields': 'namedStyleType,alignment,indentFirstLine',
                }
            })
            requests.append({
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
            in_code_block = False

        elif ptype == 'h2':
            requests.append({
                'updateParagraphStyle': {
                    'range': {'startIndex': start, 'endIndex': end},
                    'paragraphStyle': {
                        'namedStyleType': 'HEADING_2',
                        'indentFirstLine': {'magnitude': 0, 'unit': 'PT'},
                    },
                    'fields': 'namedStyleType,indentFirstLine',
                }
            })
            requests.append({
                'updateTextStyle': {
                    'range': {'startIndex': start, 'endIndex': end},
                    'textStyle': {
                        'weightedFontFamily': {'fontFamily': 'Times New Roman'},
                        'fontSize': {'magnitude': 13, 'unit': 'PT'},
                        'bold': True,
                        'italic': False,
                    },
                    'fields': 'weightedFontFamily,fontSize,bold,italic',
                }
            })
            in_code_block = False

        elif ptype == 'h3':
            requests.append({
                'updateParagraphStyle': {
                    'range': {'startIndex': start, 'endIndex': end},
                    'paragraphStyle': {
                        'namedStyleType': 'HEADING_3',
                        'indentFirstLine': {'magnitude': 0, 'unit': 'PT'},
                    },
                    'fields': 'namedStyleType,indentFirstLine',
                }
            })
            requests.append({
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
            in_code_block = False

        elif ptype in ('code', 'code_start'):
            in_code_block = True
            requests.append({
                'updateParagraphStyle': {
                    'range': {'startIndex': start, 'endIndex': end},
                    'paragraphStyle': {
                        'namedStyleType': 'NORMAL_TEXT',
                        'lineSpacing': 115,
                        'indentFirstLine': {'magnitude': 0, 'unit': 'PT'},
                        'indentStart': {'magnitude': 36, 'unit': 'PT'},
                        'alignment': 'START',
                    },
                    'fields': 'namedStyleType,lineSpacing,indentFirstLine,indentStart,alignment',
                }
            })
            requests.append({
                'updateTextStyle': {
                    'range': {'startIndex': start, 'endIndex': end},
                    'textStyle': {
                        'weightedFontFamily': {'fontFamily': 'Courier New'},
                        'fontSize': {'magnitude': 9, 'unit': 'PT'},
                        'bold': False,
                        'italic': False,
                    },
                    'fields': 'weightedFontFamily,fontSize,bold,italic',
                }
            })

        elif ptype == 'caption':
            in_code_block = False
            requests.append({
                'updateParagraphStyle': {
                    'range': {'startIndex': start, 'endIndex': end},
                    'paragraphStyle': {
                        'alignment': 'CENTER',
                        'indentFirstLine': {'magnitude': 0, 'unit': 'PT'},
                    },
                    'fields': 'alignment,indentFirstLine',
                }
            })
            requests.append({
                'updateTextStyle': {
                    'range': {'startIndex': start, 'endIndex': end},
                    'textStyle': {
                        'italic': True,
                        'bold': False,
                    },
                    'fields': 'italic,bold',
                }
            })

        elif ptype == 'math':
            in_code_block = False
            requests.append({
                'updateParagraphStyle': {
                    'range': {'startIndex': start, 'endIndex': end},
                    'paragraphStyle': {
                        'alignment': 'CENTER',
                        'indentFirstLine': {'magnitude': 0, 'unit': 'PT'},
                    },
                    'fields': 'alignment,indentFirstLine',
                }
            })
            requests.append({
                'updateTextStyle': {
                    'range': {'startIndex': start, 'endIndex': end},
                    'textStyle': {
                        'weightedFontFamily': {'fontFamily': 'Cambria Math'},
                        'italic': True,
                    },
                    'fields': 'weightedFontFamily,italic',
                }
            })

        elif ptype == 'table_row':
            in_code_block = False
            requests.append({
                'updateParagraphStyle': {
                    'range': {'startIndex': start, 'endIndex': end},
                    'paragraphStyle': {
                        'lineSpacing': 115,
                        'indentFirstLine': {'magnitude': 0, 'unit': 'PT'},
                        'alignment': 'START',
                    },
                    'fields': 'lineSpacing,indentFirstLine,alignment',
                }
            })
            requests.append({
                'updateTextStyle': {
                    'range': {'startIndex': start, 'endIndex': end},
                    'textStyle': {
                        'fontSize': {'magnitude': 11, 'unit': 'PT'},
                    },
                    'fields': 'fontSize',
                }
            })

        else:
            # Regular paragraph
            if in_code_block:
                # This might actually be code continuation
                stripped = text.strip()
                if stripped and (stripped[0] in ' \t#{}()[]' or
                    any(stripped.startswith(k) for k in ['p_', 'state', 'student', 'problem', 'target', 'query', 'result', 'mapping', 'concept', 'card', 'review', 'updates', 'params', 'recent', 'trend', 'total', 'weight', 'residual', 'k =', 'k_', 'hard_', 'easy_', 's_new', 'd_new', 'r =', 'n_', 'sample', 'best_', 'reward', 'learning', 'difficulty', 'efficiency', 'DEFAULT', 'ELO_', 'K_', 'W =', 'W[', '0.'])):
                    requests.append({
                        'updateParagraphStyle': {
                            'range': {'startIndex': start, 'endIndex': end},
                            'paragraphStyle': {
                                'lineSpacing': 115,
                                'indentFirstLine': {'magnitude': 0, 'unit': 'PT'},
                                'indentStart': {'magnitude': 36, 'unit': 'PT'},
                                'alignment': 'START',
                            },
                            'fields': 'lineSpacing,indentFirstLine,indentStart,alignment',
                        }
                    })
                    requests.append({
                        'updateTextStyle': {
                            'range': {'startIndex': start, 'endIndex': end},
                            'textStyle': {
                                'weightedFontFamily': {'fontFamily': 'Courier New'},
                                'fontSize': {'magnitude': 9, 'unit': 'PT'},
                            },
                            'fields': 'weightedFontFamily,fontSize',
                        }
                    })
                    continue
                else:
                    in_code_block = False

            # Apply bold formatting for **text** patterns
            for match in re.finditer(r'\*\*(.+?)\*\*', text):
                b_start = start + match.start()
                b_end = start + match.end()
                if b_end <= p['end']:
                    requests.append({
                        'updateTextStyle': {
                            'range': {'startIndex': b_start, 'endIndex': b_end},
                            'textStyle': {'bold': True},
                            'fields': 'bold',
                        }
                    })

            # Apply inline code formatting
            for match in re.finditer(r'`([^`]+)`', text):
                c_start = start + match.start()
                c_end = start + match.end()
                if c_end <= p['end']:
                    requests.append({
                        'updateTextStyle': {
                            'range': {'startIndex': c_start, 'endIndex': c_end},
                            'textStyle': {
                                'weightedFontFamily': {'fontFamily': 'Courier New'},
                                'fontSize': {'magnitude': 10, 'unit': 'PT'},
                            },
                            'fields': 'weightedFontFamily,fontSize',
                        }
                    })

            # Apply math formatting for $...$
            for match in re.finditer(r'\$([^$]+)\$', text):
                m_start = start + match.start()
                m_end = start + match.end()
                if m_end <= p['end']:
                    requests.append({
                        'updateTextStyle': {
                            'range': {'startIndex': m_start, 'endIndex': m_end},
                            'textStyle': {
                                'weightedFontFamily': {'fontFamily': 'Cambria Math'},
                                'italic': True,
                            },
                            'fields': 'weightedFontFamily,italic',
                        }
                    })

    return requests


def insert_images(service):
    """Insert visual images into the document."""
    print("\nInserting images...")
    doc = service.documents().get(documentId=DOC_ID).execute()
    content = doc['body']['content']

    # Build a map of caption text -> end index
    caption_locations = {}
    for elem in content:
        if 'paragraph' not in elem:
            continue
        start = elem.get('startIndex', 0)
        if start < CH4_START:
            continue

        text = ''
        for el in elem['paragraph'].get('elements', []):
            if 'textRun' in el:
                text += el['textRun']['content']

        for vis_key in VISUALS:
            if vis_key + '.' in text:
                caption_locations[vis_key] = elem['endIndex']

    print(f"  Found caption locations for: {list(caption_locations.keys())}")

    # Insert from last to first to avoid index shifts
    sorted_keys = sorted(caption_locations.keys(), key=lambda k: caption_locations[k], reverse=True)

    for vis_key in sorted_keys:
        url, width, height = VISUALS[vis_key]
        insert_idx = caption_locations[vis_key] - 1

        try:
            # Insert newline + image
            reqs = [
                {
                    'insertText': {
                        'location': {'index': insert_idx},
                        'text': '\n'
                    }
                },
                {
                    'insertInlineImage': {
                        'location': {'index': insert_idx + 1},
                        'uri': url,
                        'objectSize': {
                            'width': {'magnitude': width, 'unit': 'PT'},
                            'height': {'magnitude': height, 'unit': 'PT'},
                        }
                    }
                }
            ]
            safe_batch(service, reqs, f"image-{vis_key}")
            print(f"  Inserted {vis_key}")

            # Center the image paragraph
            time.sleep(2)
            doc = service.documents().get(documentId=DOC_ID).execute()
            content = doc['body']['content']

            # Find the image paragraph and center it
            for elem in content:
                if 'paragraph' in elem and elem.get('startIndex', 0) >= CH4_START:
                    for el in elem['paragraph'].get('elements', []):
                        if 'inlineObjectElement' in el:
                            img_start = elem['startIndex']
                            img_end = elem['endIndex']
                            safe_batch(service, [{
                                'updateParagraphStyle': {
                                    'range': {'startIndex': img_start, 'endIndex': img_end - 1},
                                    'paragraphStyle': {
                                        'alignment': 'CENTER',
                                        'indentFirstLine': {'magnitude': 0, 'unit': 'PT'},
                                    },
                                    'fields': 'alignment,indentFirstLine',
                                }
                            }], f"center-{vis_key}")
                            break

            # Update caption_locations for remaining items (shifted by ~2 chars)
            # Actually since we're going from last to first, no shift needed for remaining

            time.sleep(3)

        except Exception as e:
            print(f"  Failed to insert {vis_key}: {e}")
            time.sleep(5)


def main():
    print("=== Chapter 4 Formatting ===\n")

    service = get_service()

    # Step 1: Get all paragraphs
    print("Step 1: Reading Chapter 4 paragraphs...")
    paragraphs = get_paragraphs(service)
    print(f"  Found {len(paragraphs)} paragraphs in Chapter 4 region")

    # Classify
    types = {}
    for p in paragraphs:
        t = classify_paragraph(p['text'])
        types[t] = types.get(t, 0) + 1
    for t, c in sorted(types.items()):
        print(f"    {t}: {c}")

    # Step 2: Build formatting requests
    print("\nStep 2: Building formatting requests...")
    fmt_reqs = build_format_requests(paragraphs)
    print(f"  Total format requests: {len(fmt_reqs)}")

    # Step 3: Apply formatting in batches
    print("\nStep 3: Applying formatting...")
    batch_size = 30
    total = len(fmt_reqs)
    success_count = 0
    for i in range(0, total, batch_size):
        batch = fmt_reqs[i:i+batch_size]
        ok = safe_batch(service, batch, f"FMT-{i//batch_size+1}")
        if ok:
            success_count += len(batch)
            print(f"  Batch {i//batch_size+1}/{(total+batch_size-1)//batch_size}: {len(batch)} requests OK")
        else:
            print(f"  Batch {i//batch_size+1} had errors, retrying individually...")
            for req in batch:
                if safe_batch(service, [req], "single"):
                    success_count += 1
                time.sleep(1)
        time.sleep(3)

    print(f"\n  Applied {success_count}/{total} formatting requests")

    # Step 4: Insert images
    insert_images(service)

    print("\n=== Formatting complete ===")


if __name__ == '__main__':
    main()
