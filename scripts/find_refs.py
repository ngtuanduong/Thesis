"""Find all headings in the Google Doc to locate References."""
import warnings
warnings.filterwarnings("ignore")
from google.oauth2 import service_account
from googleapiclient.discovery import build

KEY_FILE = "C:/Users/duong/WebstormProjects/Thesis/infra-inkwell-465003-f2-369235afe5ac.json"
DOC_ID = "1O4wJNovNTFjD5DORC-WOJ2AftbcjfyoQ6HuzRSlYFfA"
SCOPES = ['https://www.googleapis.com/auth/documents', 'https://www.googleapis.com/auth/drive']

creds = service_account.Credentials.from_service_account_file(KEY_FILE, scopes=SCOPES)
service = build('docs', 'v1', credentials=creds)
doc = service.documents().get(documentId=DOC_ID).execute()
body = doc['body']['content']

total_size = body[-1]['endIndex']
print(f"Document total size: {total_size}")
print()

# Search all elements near the end of the doc for "Reference"
for elem in body:
    if 'paragraph' not in elem:
        continue
    start_idx = elem.get('startIndex', 0)
    if start_idx < total_size - 5000:
        continue
    text = ''
    for el in elem['paragraph'].get('elements', []):
        if 'textRun' in el:
            text += el['textRun']['content']
    style = elem['paragraph'].get('paragraphStyle', {}).get('namedStyleType', '')
    if text.strip():
        print(f"  [{start_idx}] style={style}: {text.strip()[:100]}")

print()
print("--- Also checking for 'reference' anywhere ---")
for elem in body:
    if 'paragraph' not in elem:
        continue
    text = ''
    for el in elem['paragraph'].get('elements', []):
        if 'textRun' in el:
            text += el['textRun']['content']
    if 'reference' in text.lower() or 'bibliograph' in text.lower():
        style = elem['paragraph'].get('paragraphStyle', {}).get('namedStyleType', '')
        start_idx = elem.get('startIndex', 0)
        print(f"  [{start_idx}] style={style}: {text.strip()[:120]}")
