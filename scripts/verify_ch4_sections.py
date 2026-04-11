#!/usr/bin/env python3
"""
Verify all Chapter 4 sections and images are present in the Google Doc.
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

# Extract ALL paragraphs between Chapter 4 start and the next chapter/references
ch4_start = None
ch4_end = None
ch4_elements = []

for element in content:
    if 'paragraph' not in element:
        # Still track non-paragraph elements in ch4 range
        if ch4_start is not None and ch4_end is None:
            ch4_elements.append(element)
        continue

    para = element['paragraph']
    text = ''
    has_image = False
    for el in para.get('elements', []):
        if 'textRun' in el:
            text += el['textRun']['content']
        if 'inlineObjectElement' in el:
            has_image = True

    text_upper = text.strip().upper()
    style = para.get('paragraphStyle', {}).get('namedStyleType', '')

    if ch4_start is None:
        if 'CHAPTER 4' in text_upper and ('IMPLEMENTATION' in text_upper or text_upper.startswith('CHAPTER 4')):
            ch4_start = element.get('startIndex', 0)
            ch4_elements.append(element)
    elif ch4_end is None:
        # Check for Chapter 5 or References or Chapter 3 heading (which comes after ch4 in this doc)
        if text_upper.startswith('CHAPTER 5') or text_upper == 'REFERENCES' or text_upper == 'BIBLIOGRAPHY':
            ch4_end = element.get('startIndex', 0)
            break
        # Also check for Chapter 2 or Chapter 3 heading that might come after Ch4 in a reshuffled doc
        if ('CHAPTER 2' in text_upper or 'CHAPTER 3' in text_upper) and ('HEADING' in style):
            ch4_end = element.get('startIndex', 0)
            break
        ch4_elements.append(element)

if ch4_end is None:
    # Find document end
    ch4_end = content[-1].get('endIndex', 0)

print(f"Chapter 4 range: [{ch4_start} - {ch4_end}]")
print(f"Chapter 4 elements: {len(ch4_elements)}")
print()

# Now list all headings and images within Chapter 4
print("=== ALL HEADINGS IN CHAPTER 4 ===")
heading_count = 0
for element in ch4_elements:
    if 'paragraph' not in element:
        continue
    para = element['paragraph']
    style = para.get('paragraphStyle', {}).get('namedStyleType', '')
    if 'HEADING' not in style:
        continue

    text = ''
    for el in para.get('elements', []):
        if 'textRun' in el:
            text += el['textRun']['content']

    idx = element.get('startIndex', 0)
    heading_count += 1
    print(f"  [{idx:6d}] {style:12s} | {text.strip()[:100]}")

print(f"\nTotal headings: {heading_count}")

print("\n=== ALL IMAGES IN CHAPTER 4 ===")
image_count = 0
for element in ch4_elements:
    if 'paragraph' not in element:
        continue
    para = element['paragraph']
    has_image = False
    for el in para.get('elements', []):
        if 'inlineObjectElement' in el:
            has_image = True

    if not has_image:
        continue

    text = ''
    for el in para.get('elements', []):
        if 'textRun' in el:
            text += el['textRun']['content']

    idx = element.get('startIndex', 0)
    image_count += 1
    print(f"  [{idx:6d}] {text.strip()[:100] if text.strip() else '[image only]'}")

print(f"\nTotal images: {image_count}")

# Check for captions
print("\n=== CAPTIONS (Table 4.x / Figure 4.x) ===")
for element in ch4_elements:
    if 'paragraph' not in element:
        continue
    para = element['paragraph']
    text = ''
    for el in para.get('elements', []):
        if 'textRun' in el:
            text += el['textRun']['content']

    text_stripped = text.strip()
    if ('Table 4.' in text_stripped or 'Figure 4.' in text_stripped) and len(text_stripped) < 200:
        idx = element.get('startIndex', 0)
        print(f"  [{idx:6d}] {text_stripped[:120]}")

# Check expected sections
print("\n=== SECTION CHECKLIST ===")
expected_sections = [
    "4.1", "4.2", "4.3", "4.4", "4.5", "4.6", "4.7", "4.8", "4.9"
]
expected_visuals = [
    "Table 4.1", "Table 4.2", "Figure 4.1", "Figure 4.2", "Figure 4.3", "Figure 4.4", "Figure 4.5"
]

all_text = ""
for element in ch4_elements:
    if 'paragraph' not in element:
        continue
    para = element['paragraph']
    for el in para.get('elements', []):
        if 'textRun' in el:
            all_text += el['textRun']['content']

for sec in expected_sections:
    found = sec in all_text
    print(f"  Section {sec}: {'FOUND' if found else 'MISSING'}")

for vis in expected_visuals:
    found = vis in all_text
    print(f"  {vis}: {'FOUND' if found else 'MISSING'}")
