#!/usr/bin/env python3
"""
Discover all inline images in the thesis Google Doc and print their positions,
nearby text, and inline object details.
"""

import json
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
inline_objects = doc.get('inlineObjects', {})

print(f"Document title: {doc.get('title', 'Unknown')}")
print(f"Total inline objects: {len(inline_objects)}")
print()

# Walk through all content elements
image_count = 0
for i, element in enumerate(content):
    if 'paragraph' not in element:
        continue

    para = element['paragraph']
    para_start = element.get('startIndex', 0)
    para_end = element.get('endIndex', 0)

    for elem in para.get('elements', []):
        if 'inlineObjectElement' in elem:
            image_count += 1
            obj_id = elem['inlineObjectElement'].get('inlineObjectId', '')
            elem_start = elem.get('startIndex', 0)
            elem_end = elem.get('endIndex', 0)

            # Get image details from inlineObjects
            img_props = inline_objects.get(obj_id, {})
            embedded = img_props.get('inlineObjectProperties', {}).get('embeddedObject', {})
            source_uri = embedded.get('imageProperties', {}).get('sourceUri', 'N/A')
            content_uri = embedded.get('imageProperties', {}).get('contentUri', 'N/A')
            size = embedded.get('size', {})
            width = size.get('width', {})
            height = size.get('height', {})

            # Get text from surrounding paragraphs
            context_before = ''
            context_after = ''

            # Look at paragraphs before
            for j in range(max(0, i-3), i):
                el = content[j]
                if 'paragraph' in el:
                    text = ''
                    for e in el['paragraph'].get('elements', []):
                        if 'textRun' in e:
                            text += e['textRun']['content']
                    if text.strip():
                        context_before = text.strip()

            # Look at paragraphs after
            for j in range(i+1, min(i+4, len(content))):
                el = content[j]
                if 'paragraph' in el:
                    text = ''
                    for e in el['paragraph'].get('elements', []):
                        if 'textRun' in e:
                            text += e['textRun']['content']
                    if text.strip():
                        context_after = text.strip()
                        break

            # Also check text in same paragraph
            same_para_text = ''
            for e in para.get('elements', []):
                if 'textRun' in e:
                    same_para_text += e['textRun']['content']

            print(f"IMAGE #{image_count}")
            print(f"  Object ID: {obj_id}")
            print(f"  Index: {elem_start} - {elem_end}")
            print(f"  Source URI: {source_uri[:100]}")
            print(f"  Size: {width.get('magnitude', '?')} x {height.get('magnitude', '?')} {width.get('unit', '?')}")
            print(f"  Same paragraph text: '{same_para_text.strip()[:80]}'")
            print(f"  Context before: '{context_before[:80]}'")
            print(f"  Context after:  '{context_after[:80]}'")
            print()

print(f"Total images found: {image_count}")
