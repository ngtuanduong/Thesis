#!/usr/bin/env python3
"""
Fix formatting for the Chapter 3 content that was inserted.
Uses correct Google Docs API field names: spaceAbove/spaceBelow (not spaceBefore/spaceAfter).
Also retry the failed hyperparameter table image with smaller dimensions.
"""

import time
import re
from google.oauth2 import service_account
from googleapiclient.discovery import build

DOC_ID = '1cJlWFX9QCEsqYo7mp6cpCWAba3Xc433-IRu8nlR63o0'
SERVICE_ACCOUNT_FILE = 'infra-inkwell-465003-f2-369235afe5ac.json'
SCOPES = ['https://www.googleapis.com/auth/documents', 'https://www.googleapis.com/auth/drive']

creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
service = build('docs', 'v1', credentials=creds)

# ─── Read current document state ─────────────────────────────────────────
doc = service.documents().get(documentId=DOC_ID).execute()
content = doc.get('body', {}).get('content', [])

# Build a map of all paragraphs with their text and indices
paragraphs = []
for element in content:
    if 'paragraph' in element:
        para = element['paragraph']
        text = ''
        for elem in para.get('elements', []):
            if 'textRun' in elem:
                text += elem['textRun']['content']
        paragraphs.append({
            'text': text.strip(),
            'start': element.get('startIndex', 0),
            'end': element.get('endIndex', 0),
            'style': para.get('paragraphStyle', {}).get('namedStyleType', 'NORMAL_TEXT'),
        })

# Find the range of our inserted content (from "3.1.4" to before "Reference:")
insert_start = None
insert_end = None
for p in paragraphs:
    if p['text'].startswith('3.1.4 Requirements Traceability') and insert_start is None:
        insert_start = p['start']
    if 'Reference' in p['text'] and '[1]' in p['text']:
        insert_end = p['start']
        break

if insert_end is None:
    # Fallback: use document end
    insert_end = paragraphs[-1]['end']
    print("WARNING: Could not find References section, using document end")

if insert_start is None:
    print("ERROR: Could not find 3.1.4 heading")
    exit(1)

print(f"Chapter 3 inserted content range: {insert_start} to {insert_end}")

# Classify each paragraph in the range
format_requests = []
our_paragraphs = [p for p in paragraphs if p['start'] >= insert_start and p['start'] < insert_end]
print(f"Found {len(our_paragraphs)} paragraphs to format")

# Heading patterns
h2_patterns = [
    '3.2 System Overview',
    '3.3 Proposed Five-Layer',
    '3.4 Data Flow Design',
    '3.5 Database Schema',
    '3.6 API Design',
    '3.7 Caching Strategy',
]

h3_patterns = [
    '3.1.4 Requirements',
    '3.2.1 Four-Component',
    '3.2.2 Design Principles',
    '3.3.1 Architecture Overview',
    '3.3.2 Layer 1',
    '3.3.3 Layer 2',
    '3.3.4 Layer 3',
    '3.3.5 Layer 4',
    '3.3.6 Layer 5',
    '3.3.7 Knowledge Graph',
    '3.3.8 Hyperparameter',
    '3.4.1 Recommendation Flow',
    '3.4.2 Submission Processing',
    '3.4.3 Error Handling',
    '3.4.4 Cold Start',
    '3.5.1 Adaptive Tables',
    '3.5.2 Schema Relationships',
    '3.5.3 Migration Strategy',
    '3.6.1 AI Service Endpoints',
    '3.6.2 NestJS Gateway',
    '3.6.3 Endpoints with Adaptive',
]

bold_patterns = [
    'Purpose.', 'Model.', 'Input.', 'Output.', 'Mastery threshold.',
    'Interaction with other layers.', 'Structure.', 'Role in the architecture.',
    'Reward Signal.', 'Level 1 (Concept Selection).', 'Level 2 (Problem Selection).',
    'Security.', 'ID strategy.',
    'React + TypeScript Frontend', 'NestJS API Gateway', 'FastAPI AI Service',
    'PostgreSQL (pgvector)',
    'FR1', 'FR2', 'FR3', 'FR4', 'FR5', 'FR6', 'FR7', 'FR8', 'FR9', 'FR10', 'FR11',
    'NFR1-NFR5',
    'Transactional boundaries.', 'Retry mechanism.', 'Empty eligible set.',
    'ZPD exhaustion.', 'Concurrent submissions.', 'AI service unavailability.',
    'New Student Cold Start.', 'New Problem Cold Start.',
    'Concepts table.', 'Knowledge graph edges table.', 'Problem concepts table.',
    'Knowledge states table.', 'Elo ratings table.', 'MAB states table.',
    'FSRS cards table.',
    'Phase 1: Knowledge Graph', 'Phase 2: Adaptive state', 'Phase 3: Evaluation',
    'Phase 1: Synchronous', 'Phase 2: Asynchronous',
    'Knowledge Graph Management:', 'Adaptive Recommendations (Proxy):',
    'Analytics:', 'Invalidation strategy.', 'Fallback behavior.',
    'GET /adaptive/', 'POST /adaptive/', 'POST /api/submissions.',
    'GET /api/dashboard.',
]

caption_patterns = [
    'Figure 3.', 'Table 3.',
]

equation_patterns = [
    'E(A) = 1 /',
    "R_A' = R_A",  # Use the actual character
    "R_B' = R_B",
    'K_A = K_base',
    'R_student +',
    'r = w_1',
    'R(t) = (1 +',
]

for p in our_paragraphs:
    text = p['text']
    start = p['start']
    end = p['end']

    if not text:
        continue

    # Determine paragraph type
    para_type = 'body'

    for pattern in h2_patterns:
        if text.startswith(pattern):
            para_type = 'h2'
            break

    if para_type == 'body':
        for pattern in h3_patterns:
            if text.startswith(pattern):
                para_type = 'h3'
                break

    if para_type == 'body':
        for pattern in caption_patterns:
            if text.startswith(pattern):
                para_type = 'caption'
                break

    if para_type == 'body':
        for pattern in equation_patterns:
            if text.startswith(pattern):
                para_type = 'equation'
                break

    if para_type == 'body':
        for pattern in bold_patterns:
            if text.startswith(pattern):
                para_type = 'bold_label'
                break

    if para_type == 'body' and text.startswith('Chapter Summary.'):
        para_type = 'bold_label'

    # Build format requests
    if para_type == 'h2':
        format_requests.append({
            'updateParagraphStyle': {
                'range': {'startIndex': start, 'endIndex': end},
                'paragraphStyle': {
                    'namedStyleType': 'HEADING_2',
                    'spaceAbove': {'magnitude': 18, 'unit': 'PT'},
                    'spaceBelow': {'magnitude': 8, 'unit': 'PT'},
                    'keepWithNext': True,
                },
                'fields': 'namedStyleType,spaceAbove,spaceBelow,keepWithNext',
            }
        })
        format_requests.append({
            'updateTextStyle': {
                'range': {'startIndex': start, 'endIndex': end - 1},
                'textStyle': {
                    'bold': True,
                    'italic': False,
                    'weightedFontFamily': {'fontFamily': 'Times New Roman'},
                    'fontSize': {'magnitude': 13, 'unit': 'PT'},
                },
                'fields': 'bold,italic,weightedFontFamily,fontSize',
            }
        })

    elif para_type == 'h3':
        format_requests.append({
            'updateParagraphStyle': {
                'range': {'startIndex': start, 'endIndex': end},
                'paragraphStyle': {
                    'namedStyleType': 'HEADING_3',
                    'spaceAbove': {'magnitude': 14, 'unit': 'PT'},
                    'spaceBelow': {'magnitude': 6, 'unit': 'PT'},
                    'keepWithNext': True,
                },
                'fields': 'namedStyleType,spaceAbove,spaceBelow,keepWithNext',
            }
        })
        format_requests.append({
            'updateTextStyle': {
                'range': {'startIndex': start, 'endIndex': end - 1},
                'textStyle': {
                    'bold': True,
                    'italic': True,
                    'weightedFontFamily': {'fontFamily': 'Times New Roman'},
                    'fontSize': {'magnitude': 12, 'unit': 'PT'},
                },
                'fields': 'bold,italic,weightedFontFamily,fontSize',
            }
        })

    elif para_type == 'body':
        format_requests.append({
            'updateParagraphStyle': {
                'range': {'startIndex': start, 'endIndex': end},
                'paragraphStyle': {
                    'namedStyleType': 'NORMAL_TEXT',
                    'lineSpacing': 150,
                    'spaceBelow': {'magnitude': 6, 'unit': 'PT'},
                    'indentFirstLine': {'magnitude': 36, 'unit': 'PT'},
                    'alignment': 'JUSTIFIED',
                },
                'fields': 'namedStyleType,lineSpacing,spaceBelow,indentFirstLine,alignment',
            }
        })
        format_requests.append({
            'updateTextStyle': {
                'range': {'startIndex': start, 'endIndex': end - 1},
                'textStyle': {
                    'weightedFontFamily': {'fontFamily': 'Times New Roman'},
                    'fontSize': {'magnitude': 12, 'unit': 'PT'},
                    'bold': False,
                    'italic': False,
                },
                'fields': 'weightedFontFamily,fontSize,bold,italic',
            }
        })

    elif para_type == 'bold_label':
        format_requests.append({
            'updateParagraphStyle': {
                'range': {'startIndex': start, 'endIndex': end},
                'paragraphStyle': {
                    'namedStyleType': 'NORMAL_TEXT',
                    'lineSpacing': 150,
                    'spaceBelow': {'magnitude': 4, 'unit': 'PT'},
                    'spaceAbove': {'magnitude': 8, 'unit': 'PT'},
                },
                'fields': 'namedStyleType,lineSpacing,spaceBelow,spaceAbove',
            }
        })
        format_requests.append({
            'updateTextStyle': {
                'range': {'startIndex': start, 'endIndex': end - 1},
                'textStyle': {
                    'bold': True,
                    'italic': False,
                    'weightedFontFamily': {'fontFamily': 'Times New Roman'},
                    'fontSize': {'magnitude': 12, 'unit': 'PT'},
                },
                'fields': 'bold,italic,weightedFontFamily,fontSize',
            }
        })

    elif para_type == 'caption':
        format_requests.append({
            'updateParagraphStyle': {
                'range': {'startIndex': start, 'endIndex': end},
                'paragraphStyle': {
                    'namedStyleType': 'NORMAL_TEXT',
                    'alignment': 'CENTER',
                    'spaceBelow': {'magnitude': 12, 'unit': 'PT'},
                    'spaceAbove': {'magnitude': 6, 'unit': 'PT'},
                },
                'fields': 'namedStyleType,alignment,spaceBelow,spaceAbove',
            }
        })
        format_requests.append({
            'updateTextStyle': {
                'range': {'startIndex': start, 'endIndex': end - 1},
                'textStyle': {
                    'italic': True,
                    'bold': False,
                    'weightedFontFamily': {'fontFamily': 'Times New Roman'},
                    'fontSize': {'magnitude': 12, 'unit': 'PT'},
                },
                'fields': 'italic,bold,weightedFontFamily,fontSize',
            }
        })

    elif para_type == 'equation':
        format_requests.append({
            'updateParagraphStyle': {
                'range': {'startIndex': start, 'endIndex': end},
                'paragraphStyle': {
                    'namedStyleType': 'NORMAL_TEXT',
                    'alignment': 'CENTER',
                    'spaceBelow': {'magnitude': 8, 'unit': 'PT'},
                    'spaceAbove': {'magnitude': 8, 'unit': 'PT'},
                    'indentFirstLine': {'magnitude': 0, 'unit': 'PT'},
                },
                'fields': 'namedStyleType,alignment,spaceBelow,spaceAbove,indentFirstLine',
            }
        })
        format_requests.append({
            'updateTextStyle': {
                'range': {'startIndex': start, 'endIndex': end - 1},
                'textStyle': {
                    'italic': True,
                    'bold': False,
                    'weightedFontFamily': {'fontFamily': 'Cambria Math'},
                    'fontSize': {'magnitude': 12, 'unit': 'PT'},
                },
                'fields': 'italic,bold,weightedFontFamily,fontSize',
            }
        })

print(f"Total format requests: {len(format_requests)}")

# Apply formatting in batches
batch_size = 40
for i in range(0, len(format_requests), batch_size):
    batch = format_requests[i:i+batch_size]
    try:
        service.documents().batchUpdate(
            documentId=DOC_ID,
            body={'requests': batch}
        ).execute()
        print(f"  Format batch {i//batch_size + 1}/{(len(format_requests) + batch_size - 1)//batch_size} applied ({len(batch)} requests)")
    except Exception as e:
        print(f"  Format batch {i//batch_size + 1} FAILED: {str(e)[:200]}")
    time.sleep(2)

# ─── Retry the failed hyperparameter table image ─────────────────────────
print("\nRetrying hyperparameter table image with smaller dimensions...")

# Find the caption "Table 3.3. Hyperparameter summary" and insert image before it
for p in paragraphs:
    if p['text'].startswith('Table 3.3. Hyperparameter summary'):
        img_index = p['start']  # Insert before the caption
        try:
            service.documents().batchUpdate(
                documentId=DOC_ID,
                body={'requests': [{
                    'insertInlineImage': {
                        'location': {'index': img_index},
                        'uri': 'https://files.catbox.moe/ue4upp.png',
                        'objectSize': {
                            'width': {'magnitude': 400, 'unit': 'PT'},
                            'height': {'magnitude': 350, 'unit': 'PT'},
                        }
                    }
                }]}
            ).execute()
            print(f"  Hyperparameter table image inserted at index {img_index}")
        except Exception as e:
            print(f"  Image retry FAILED: {str(e)[:200]}")
        break

print("\n=== FORMATTING COMPLETE ===")
