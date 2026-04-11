#!/usr/bin/env python3
"""
Verify the current state of the Google Doc.
Check which chapters exist and where Chapter 4 content is (or is not).
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

print(f"Document title: {doc.get('title')}")
print(f"Total elements: {len(content)}")
last_elem = content[-1]
doc_end = last_elem.get('endIndex', 0)
print(f"Document end index: {doc_end}")
print()

# Search for chapter headings, section headings, figure/table captions related to Ch4
search_terms = [
    'CHAPTER 1', 'CHAPTER 2', 'CHAPTER 3', 'CHAPTER 4', 'CHAPTER 5',
    'REFERENCES', 'BIBLIOGRAPHY',
    '4.1 ', '4.2 ', '4.3 ', '4.4 ', '4.5 ', '4.6 ', '4.7 ', '4.8 ', '4.9 ',
    'Table 4.', 'Figure 4.',
    'Technology Stack', 'Knowledge Graph', 'Knowledge Tracing',
    'Difficulty Calibration', 'Problem Selection', 'Spaced Repetition',
    'Recommendation Pipeline', 'Frontend', 'Deployment',
]

print("=== KEY PARAGRAPHS ===")
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
        style = para.get('paragraphStyle', {}).get('namedStyleType', '')

        matched = False
        for term in search_terms:
            if term.lower() in text_stripped.lower():
                matched = True
                break

        if matched or has_image:
            prefix = "[IMG]" if has_image else f"[{style[:10]:10s}]"
            print(f"{prefix} [{start_idx:6d}-{end_idx:6d}] {text_stripped[:150]}")

# Print the last 20 paragraphs to see what's at the end
print()
print("=== LAST 20 TEXT PARAGRAPHS ===")
text_paras = []
for element in content:
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
        if text_stripped or has_image:
            text_paras.append((element.get('startIndex', 0), element.get('endIndex', 0), text_stripped[:120], has_image))

for start, end, txt, img in text_paras[-20:]:
    prefix = "[IMG]" if img else "     "
    print(f"{prefix} [{start:6d}-{end:6d}] {txt}")
