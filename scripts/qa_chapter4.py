#!/usr/bin/env python3
"""
QA verification for Chapter 4 in Google Docs.
Checks: all headings, all images, all figure captions, section completeness.
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

print("=" * 60)
print("CHAPTER 4 QA REPORT")
print("=" * 60)

# 1. Find Chapter 4 range
ch4_start = None
ch4_end = None
ch4_elements = []
found_summary = False

for element in content:
    if 'paragraph' not in element:
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
        if 'CHAPTER 4' in text_upper and 'HEADING' in style:
            ch4_start = element.get('startIndex', 0)
            ch4_elements.append(element)
    elif ch4_end is None:
        if 'Chapter 5 turns to' in text.strip():
            ch4_end = element.get('endIndex', 0)
            ch4_elements.append(element)
        elif ('CHAPTER 2' in text_upper or 'CHAPTER 3' in text_upper or 'CHAPTER 5' in text_upper) and 'HEADING' in style:
            ch4_end = element.get('startIndex', 0)
        else:
            ch4_elements.append(element)

if ch4_end is None:
    ch4_end = content[-1].get('endIndex', 0)

print(f"\n1. CHAPTER 4 RANGE")
print(f"   Start: {ch4_start}")
print(f"   End:   {ch4_end}")
print(f"   Size:  {ch4_end - ch4_start} chars")
print(f"   Elements: {len(ch4_elements)}")

# 2. Check all expected headings
print(f"\n2. HEADING CHECK")
expected_headings = {
    "CHAPTER 4": "H1",
    "4.1 Technology Stack": "H2",
    "4.2 Knowledge Graph Construction": "H2",
    "4.2.1 Concept Taxonomy": "H3",
    "4.2.2 Prerequisite Relationships": "H3",
    "4.2.3 Problem-to-Concept Mapping": "H3",
    "4.2.4 Future Direction": "H3",
    "4.3 Layer 1": "H2",
    "4.3.1 BKT Implementation": "H3",
    "4.3.2 Multi-Concept Update": "H3",
    "4.4 Layer 2": "H2",
    "4.4.1 Dual Elo Implementation": "H3",
    "4.4.2 ZPD Filtering": "H3",
    "4.5 Layer 3": "H2",
    "4.5.1 Thompson Sampling": "H3",
    "4.5.2 Reward Function": "H3",
    "4.5.3 Hierarchical Selection": "H3",
    "4.6 Layer 4": "H2",
    "4.6.1 FSRS-5 Algorithm": "H3",
    "4.6.2 Rating Mapping": "H3",
    "4.6.3 Review Queue": "H3",
    "4.7 Layer 5": "H2",
    "4.8 Frontend Implementation": "H2",
    "4.8.1 Student Dashboard": "H3",
    "4.8.2 Adaptive Recommendation": "H3",
    "4.8.3 Review Queue Page": "H3",
    "4.8.4 Technology Choices": "H3",
    "4.9 Deployment": "H2",
    "4.9.1 Docker Compose": "H3",
    "4.9.2 Environment Configuration": "H3",
    "4.9.3 Monitoring": "H3",
    "Chapter Summary": "H2",
}

found_headings = {}
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
    text_stripped = text.strip()
    found_headings[text_stripped] = style

all_found = True
for expected, expected_level in expected_headings.items():
    found = False
    for fh in found_headings:
        if expected.lower() in fh.lower():
            found = True
            break
    status = "OK" if found else "MISSING"
    if not found:
        all_found = False
    print(f"   [{status:7s}] {expected_level} | {expected}")

print(f"\n   Headings: {'ALL PRESENT' if all_found else 'SOME MISSING'}")

# 3. Check images
print(f"\n3. IMAGE CHECK")
ch4_images = 0
ch4_image_sources = []
inline_objects = doc.get('inlineObjects', {})

for element in ch4_elements:
    if 'paragraph' not in element:
        continue
    para = element['paragraph']
    for el in para.get('elements', []):
        if 'inlineObjectElement' in el:
            obj_id = el['inlineObjectElement'].get('inlineObjectId', '')
            ch4_images += 1
            if obj_id in inline_objects:
                props = inline_objects[obj_id].get('inlineObjectProperties', {}).get('embeddedObject', {})
                src = props.get('imageProperties', {}).get('sourceUri', '') if 'imageProperties' in props else ''
                ch4_image_sources.append(src)

expected_images = {
    "Table 4.1": "7nj9z8.png",
    "Table 4.2": "0005w3.png",
    "Figure 4.1": "vq16l2.png",
    "Figure 4.2": "0pk8fv.png",
    "Figure 4.3": "vbzbwp.png",
    "Figure 4.4": "3yojqt.png",
    "Figure 4.5": "4g1sh7.png",
}

print(f"   Total images in Ch4 range: {ch4_images}")
all_images_found = True
for name, filename in expected_images.items():
    found = any(filename in src for src in ch4_image_sources)
    status = "OK" if found else "MISSING"
    if not found:
        all_images_found = False
    print(f"   [{status:7s}] {name} ({filename})")

print(f"\n   Images: {'ALL PRESENT' if all_images_found else 'SOME MISSING'}")

# 4. Check figure captions
print(f"\n4. FIGURE CAPTION CHECK")
expected_captions = [
    "Figure 4.1",
    "Figure 4.2",
    "Figure 4.3",
    "Figure 4.4",
    "Figure 4.5",
    "Table 4.1",
    "Table 4.2",
]

all_text = ""
for element in ch4_elements:
    if 'paragraph' not in element:
        continue
    for el in element['paragraph'].get('elements', []):
        if 'textRun' in el:
            all_text += el['textRun']['content']

all_captions_found = True
for cap in expected_captions:
    found = cap in all_text
    status = "OK" if found else "MISSING"
    if not found:
        all_captions_found = False
    print(f"   [{status:7s}] {cap}")

print(f"\n   Captions: {'ALL PRESENT' if all_captions_found else 'SOME MISSING'}")

# 5. Check section text content (key phrases from each section)
print(f"\n5. SECTION CONTENT CHECK")
section_markers = {
    "4.1": "React 18",
    "4.2.1": "concept taxonomy",
    "4.2.2": "directed acyclic graph",
    "4.2.3": "problem_concepts",
    "4.2.4": "Automated Concept Extraction",
    "4.3.1": "bkt_update",
    "4.3.2": "get_or_create_state",
    "4.4.1": "expected_score",
    "4.4.2": "Zone of Proximal Development",
    "4.5.1": "thompson_select",
    "4.5.2": "learning_gain",
    "4.5.3": "FSRS conflict resolution",
    "4.6.1": "retrievability",
    "4.6.2": "submission_to_fsrs_rating",
    "4.6.3": "get_review_queue",
    "4.7": "Socratic hints",
    "4.8.1": "radar chart",
    "4.8.2": "recommendation card",
    "4.8.3": "FSRS scheduler",
    "4.8.4": "Recharts",
    "4.9.1": "Docker Compose",
    "4.9.2": "Three environment profiles",
    "4.9.3": "structured JSON",
}

all_content_found = True
for sec, marker in section_markers.items():
    found = marker.lower() in all_text.lower()
    status = "OK" if found else "MISSING"
    if not found:
        all_content_found = False
    print(f"   [{status:7s}] Section {sec}: '{marker}'")

print(f"\n   Section content: {'ALL PRESENT' if all_content_found else 'SOME MISSING'}")

# 6. Overall summary
print(f"\n{'=' * 60}")
print(f"OVERALL QA RESULT")
print(f"{'=' * 60}")
passed = all([all_found, all_images_found, all_captions_found, all_content_found])
print(f"   Headings:  {'PASS' if all_found else 'FAIL'}")
print(f"   Images:    {'PASS' if all_images_found else 'FAIL'}")
print(f"   Captions:  {'PASS' if all_captions_found else 'FAIL'}")
print(f"   Content:   {'PASS' if all_content_found else 'FAIL'}")
print(f"   ---------")
print(f"   OVERALL:   {'PASS' if passed else 'FAIL'}")
