#!/usr/bin/env python3
"""
Find where Figure 4.x captions exist and check for section 4.5/4.6 headings.
Also check the detailed structure around missing areas.
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

# Dump everything from index 48000 to 66000 (sections 4.4 through 4.7)
# This covers the area where 4.5 and 4.6 should be, and figure captions
print("=== DETAILED DUMP: Index 48000-66500 (Sections 4.4 through 4.7) ===")
for element in content:
    start_idx = element.get('startIndex', 0)
    end_idx = element.get('endIndex', 0)

    if end_idx < 48000 or start_idx > 66500:
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

        # Show headings, image paragraphs, and lines containing Figure/Table references
        is_heading = 'HEADING' in style
        has_figure_ref = 'Figure 4.' in text_stripped or 'Table 4.' in text_stripped
        is_short = len(text_stripped) < 100  # captions are short

        if is_heading or has_image or has_figure_ref or is_short:
            prefix = "[IMG]" if has_image else f"[{style[:10]:10s}]"
            print(f"{prefix} [{start_idx:6d}-{end_idx:6d}] {text_stripped[:150]}")

    elif 'table' in element:
        print(f"[TABLE    ] [{start_idx:6d}-{end_idx:6d}] <TABLE>")

# Also dump area around Figure 4.1 caption (should be after submission pipeline section)
# Check for "Figure 4." text anywhere in ch4
print("\n\n=== ALL PARAGRAPHS CONTAINING 'Figure 4.' IN ENTIRE DOC ===")
for element in content:
    if 'paragraph' not in element:
        continue
    para = element['paragraph']
    text = ''
    for el in para.get('elements', []):
        if 'textRun' in el:
            text += el['textRun']['content']

    if 'Figure 4.' in text:
        idx = element.get('startIndex', 0)
        style = para.get('paragraphStyle', {}).get('namedStyleType', '')
        print(f"  [{idx:6d}] {style:12s} | {text.strip()[:150]}")

# Check inline objects in the document
print("\n\n=== INLINE OBJECTS IN DOCUMENT (between ch4 indices) ===")
inline_objects = doc.get('inlineObjects', {})
print(f"Total inline objects in doc: {len(inline_objects)}")
for obj_id, obj_data in inline_objects.items():
    props = obj_data.get('inlineObjectProperties', {}).get('embeddedObject', {})
    title = props.get('title', '')
    desc = props.get('description', '')
    uri = props.get('imageProperties', {}).get('contentUri', '') if 'imageProperties' in props else ''
    source_uri = props.get('imageProperties', {}).get('sourceUri', '') if 'imageProperties' in props else ''
    w = props.get('size', {}).get('width', {}).get('magnitude', 0)
    h = props.get('size', {}).get('height', {}).get('magnitude', 0)
    print(f"  {obj_id[:20]:20s} | {w:.0f}x{h:.0f}pt | src={source_uri[:60] if source_uri else 'N/A'}")
