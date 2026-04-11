#!/usr/bin/env python3
"""
Detailed check of sections 4.4-4.7 to understand missing headings and figure placement.
"""
import warnings
warnings.filterwarnings("ignore")

from google.oauth2 import service_account
from googleapiclient.discovery import build

DOC_ID = "1O4wJNovNTFjD5DORC-WOJ2AftbcjfyoQ6HuzRSlYFfA"
KEY_FILE = "C:/Users/duong/WebstormProjects/Thesis/infra-inkwell-465003-f2-369235afe5ac.json"
SCOPES = ['https://www.googleapis.com/auth/documents', 'https://www.googleapis.com/auth/drive']

creds = service_account.Credentials.from_service_account_file(KEY_FILE, scopes=SCOPES)
service = build('docs', 'v1', credentials=creds)
doc = service.documents().get(documentId=DOC_ID).execute()
content = doc.get('body', {}).get('content', [])

# Dump ALL paragraphs from index 48000 to 72500 with full text
print("=== FULL PARAGRAPH DUMP: Index 48000-72500 ===")
for element in content:
    start_idx = element.get('startIndex', 0)
    end_idx = element.get('endIndex', 0)

    if end_idx < 48000 or start_idx > 72500:
        continue

    if 'paragraph' in element:
        para = element['paragraph']
        text = ''
        has_image = False
        for el in para.get('elements', []):
            if 'textRun' in el:
                text += el['textRun']['content']
            if 'inlineObjectElement' in el:
                has_image = True

        style = para.get('paragraphStyle', {}).get('namedStyleType', '')
        text_stripped = text.strip()

        # Show everything: headings, short paragraphs, important markers
        if text_stripped:
            prefix = "[IMG]" if has_image else f"[{style[:10]:10s}]"
            truncated = text_stripped[:200]
            print(f"{prefix} [{start_idx:6d}-{end_idx:6d}] {truncated}")
