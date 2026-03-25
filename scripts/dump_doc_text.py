#!/usr/bin/env python3
"""
Dump all text content from the Google Doc with paragraph indices,
to find insertion points for missing figures.
"""

from google.oauth2 import service_account
from googleapiclient.discovery import build

DOC_ID = '1cJlWFX9QCEsqYo7mp6cpCWAba3Xc433-IRu8nlR63o0'
SERVICE_ACCOUNT_FILE = '/Users/avada/WebstormProjects/Thesis/infra-inkwell-465003-f2-369235afe5ac.json'
SCOPES = ['https://www.googleapis.com/auth/documents', 'https://www.googleapis.com/auth/drive']

creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
service = build('docs', 'v1', credentials=creds)
doc = service.documents().get(documentId=DOC_ID).execute()
content = doc.get('body', {}).get('content', [])

# Search for key terms related to the 7 figures
search_terms = [
    'Figure 1.1', 'Figure 1.2', 'Figure 1.3', 'Figure 1.4',
    'Figure 2.1', 'Figure 2.2', 'Figure 2.3',
    'Table 1.1',  # Figure 1.1 goes after Table 1.1
    '1.2.3', '1.5.1', '1.5.2', '1.8',
    '2.2.2', '2.2.3', '2.2.5', '2.4',
    'The Gap in Existing Platforms',
    'Closed-Loop', 'closed-loop',
    'Five-Layer', 'five-layer', 'Architecture Overview',
    'Thesis Structure',
    'Literature Landscape', 'literature landscape',
    'Knowledge Tracing', 'knowledge tracing',
    'Spaced Repetition', 'spaced repetition',
    'Research Gap',
]

print(f"Document: {doc.get('title')}")
print(f"Total elements: {len(content)}")
print()

for element in content:
    start_idx = element.get('startIndex', 0)
    end_idx = element.get('endIndex', 0)

    if 'paragraph' in element:
        para = element['paragraph']
        text = ''
        has_image = False
        for elem in para.get('elements', []):
            if 'textRun' in elem:
                text += elem['textRun']['content']
            if 'inlineObjectElement' in elem:
                has_image = True

        text_stripped = text.strip()

        # Check if any search term is in the text
        matched = False
        for term in search_terms:
            if term.lower() in text_stripped.lower():
                matched = True
                break

        if matched or has_image:
            prefix = "[IMG]" if has_image else "     "
            print(f"{prefix} [{start_idx:6d}-{end_idx:6d}] {text_stripped[:150]}")

    elif 'table' in element:
        print(f"[TBL] [{start_idx:6d}-{end_idx:6d}] <TABLE>")
