#!/usr/bin/env python3
"""
Find all visual caption positions in the document (Table X.Y, Figure X.Y captions)
to determine where images need to be inserted for chapters that don't have them yet.
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

print("All Table/Figure captions found in the document:\n")

for element in content:
    if 'paragraph' not in element:
        continue
    para = element['paragraph']
    text = ''
    for elem in para.get('elements', []):
        if 'textRun' in elem:
            text += elem['textRun']['content']
    text = text.strip()
    if text and ('Table ' in text or 'Figure ' in text):
        # Check if this looks like a caption (starts with Table/Figure and has a period)
        if (text.startswith('Table ') or text.startswith('Figure ')) and '.' in text[:15]:
            start = element.get('startIndex', 0)
            end = element.get('endIndex', 0)
            print(f"  [{start:6d} - {end:6d}] {text[:100]}")

# Also find chapter headings to understand document structure
print("\n\nChapter headings found:\n")
for element in content:
    if 'paragraph' not in element:
        continue
    para = element['paragraph']
    style = para.get('paragraphStyle', {}).get('namedStyleType', '')
    if style in ('HEADING_1', 'HEADING_2'):
        text = ''
        for elem in para.get('elements', []):
            if 'textRun' in elem:
                text += elem['textRun']['content']
        text = text.strip()
        if text:
            start = element.get('startIndex', 0)
            print(f"  [{start:6d}] [{style}] {text[:100]}")
