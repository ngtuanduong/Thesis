#!/usr/bin/env python3
"""
Search for any text mentioning Figure 1.x, Figure 2.x in the document
to find where these visuals should go.
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

search_terms = ['Figure 1.', 'Figure 2.', 'Table 2.1']

print("Searching for Figure 1.x, Figure 2.x, Table 2.1 references:\n")

for element in content:
    if 'paragraph' not in element:
        continue
    para = element['paragraph']
    text = ''
    for elem in para.get('elements', []):
        if 'textRun' in elem:
            text += elem['textRun']['content']
    text_stripped = text.strip()
    for term in search_terms:
        if term in text_stripped:
            start = element.get('startIndex', 0)
            print(f"  [{start:6d}] {text_stripped[:120]}")
            break
