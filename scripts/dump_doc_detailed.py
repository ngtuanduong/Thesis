#!/usr/bin/env python3
"""
Dump detailed text around specific index ranges to find exact insertion points.
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

# Ranges to examine in detail (start, end) - covers areas around the 7 figures
ranges = [
    # Figure 1.1 - after Table 1.1 (around index 14007-16000)
    (13900, 16300),
    # Figure 1.3 - after 1.5.1 Architecture Overview (around 22718-25900)
    (22700, 26000),
    # Figure 1.2 - after 1.5.2 Closed-Loop Workflow (around 25823-27000)
    (25800, 27500),
    # Figure 1.4 - after 1.8 Thesis Structure (around 32271-34700)
    (32200, 34800),
    # Figure 2.1 - beginning of Chapter 2 or near 2.4 (around 34675 or 78692)
    (34600, 36000),
    # Figure 2.2 - after 2.2.2 DKT discussion (around 49886-52500)
    (49800, 52600),
    # Figure 2.3 - end of 2.2.5 Spaced Repetition (around 62106-66000)
    (62000, 66500),
]

for r_start, r_end in ranges:
    print(f"\n{'='*80}")
    print(f"RANGE: {r_start} - {r_end}")
    print(f"{'='*80}")
    for element in content:
        el_start = element.get('startIndex', 0)
        el_end = element.get('endIndex', 0)

        if el_end < r_start or el_start > r_end:
            continue

        if 'paragraph' in element:
            para = element['paragraph']
            text = ''
            has_image = False
            for elem in para.get('elements', []):
                if 'textRun' in elem:
                    text += elem['textRun']['content']
                if 'inlineObjectElement' in elem:
                    has_image = True

            style = para.get('paragraphStyle', {}).get('namedStyleType', '')
            prefix = "[IMG]" if has_image else f"[{style[:8]:8s}]"
            print(f"{prefix} [{el_start:6d}-{el_end:6d}] {text.strip()[:150]}")

        elif 'table' in element:
            print(f"[TABLE  ] [{el_start:6d}-{el_end:6d}] <TABLE>")

        elif 'sectionBreak' in element:
            print(f"[SECBRK ] [{el_start:6d}-{el_end:6d}] <SECTION BREAK>")
