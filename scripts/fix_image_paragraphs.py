#!/usr/bin/env python3
"""
Fix images that ended up inside caption paragraphs.
For each image that shares a paragraph with caption text,
insert a newline after the image to push the caption to its own paragraph.
"""

import time
from google.oauth2 import service_account
from googleapiclient.discovery import build

DOC_ID = '1cJlWFX9QCEsqYo7mp6cpCWAba3Xc433-IRu8nlR63o0'
SERVICE_ACCOUNT_FILE = '/Users/avada/WebstormProjects/Thesis/infra-inkwell-465003-f2-369235afe5ac.json'
SCOPES = ['https://www.googleapis.com/auth/documents', 'https://www.googleapis.com/auth/drive']

creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
service = build('docs', 'v1', credentials=creds)


def get_doc():
    return service.documents().get(documentId=DOC_ID).execute()


def batch_update(requests):
    return service.documents().batchUpdate(
        documentId=DOC_ID,
        body={'requests': requests}
    ).execute()


def fix_images():
    """Find images that share a paragraph with text and insert a newline to separate them."""
    doc = get_doc()
    content = doc.get('body', {}).get('content', [])

    # Find paragraphs that have both an inline image and text
    fixes_needed = []
    for element in content:
        if 'paragraph' not in element:
            continue
        para = element['paragraph']
        has_image = False
        has_text = False
        image_end = None

        for elem in para.get('elements', []):
            if 'inlineObjectElement' in elem:
                has_image = True
                image_end = elem.get('endIndex', 0)
            if 'textRun' in elem:
                text = elem['textRun']['content'].strip()
                if text:
                    has_text = True

        if has_image and has_text and image_end is not None:
            # Need to insert a newline after the image
            fixes_needed.append(image_end)

    print(f"Found {len(fixes_needed)} images sharing paragraphs with text")

    if not fixes_needed:
        print("No fixes needed!")
        return

    # Process from last to first to avoid index shifting
    fixes_needed.sort(reverse=True)

    for idx, insert_at in enumerate(fixes_needed):
        print(f"  Fix {idx+1}/{len(fixes_needed)}: Inserting newline at index {insert_at}")
        try:
            batch_update([{
                'insertText': {
                    'location': {'index': insert_at},
                    'text': '\n',
                }
            }])
        except Exception as e:
            print(f"    ERROR: {str(e)[:200]}")
        time.sleep(1)

    print("Done fixing image paragraphs!")

    # Now apply centered paragraph style to the image paragraphs
    print("\nApplying centered alignment to image paragraphs...")
    doc = get_doc()
    content = doc.get('body', {}).get('content', [])

    format_requests = []
    for element in content:
        if 'paragraph' not in element:
            continue
        para = element['paragraph']
        for elem in para.get('elements', []):
            if 'inlineObjectElement' in elem:
                start = element.get('startIndex', 0)
                end = element.get('endIndex', 0)
                format_requests.append({
                    'updateParagraphStyle': {
                        'range': {'startIndex': start, 'endIndex': end},
                        'paragraphStyle': {
                            'alignment': 'CENTER',
                            'spaceAbove': {'magnitude': 12, 'unit': 'PT'},
                            'spaceBelow': {'magnitude': 6, 'unit': 'PT'},
                        },
                        'fields': 'alignment,spaceAbove,spaceBelow',
                    }
                })

    if format_requests:
        # Skip the cover page logo (first image)
        print(f"  Centering {len(format_requests)} image paragraphs...")
        try:
            batch_update(format_requests)
            print("  Done!")
        except Exception as e:
            print(f"  ERROR: {str(e)[:200]}")


if __name__ == '__main__':
    fix_images()
