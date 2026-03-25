#!/usr/bin/env python3
"""
Insert 7 missing figures into the thesis Google Doc.
Processes ONE figure at a time, re-reading the document after each insertion.

For each figure:
1. Find the anchor text (a paragraph near where the figure should go)
2. Insert a new paragraph with the caption (centered, italic)
3. Insert the image before the caption
4. Format the caption
"""

import time
import sys
from google.oauth2 import service_account
from googleapiclient.discovery import build

# ─── Configuration ───────────────────────────────────────────────────────────
DOC_ID = '1cJlWFX9QCEsqYo7mp6cpCWAba3Xc433-IRu8nlR63o0'
SERVICE_ACCOUNT_FILE = '/Users/avada/WebstormProjects/Thesis/infra-inkwell-465003-f2-369235afe5ac.json'
SCOPES = ['https://www.googleapis.com/auth/documents', 'https://www.googleapis.com/auth/drive']

creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
service = build('docs', 'v1', credentials=creds)


def get_doc():
    """Fetch the current document state."""
    return service.documents().get(documentId=DOC_ID).execute()


def batch_update(requests):
    """Execute a batchUpdate with given requests."""
    return service.documents().batchUpdate(
        documentId=DOC_ID,
        body={'requests': requests}
    ).execute()


def find_paragraph_end(doc, anchor_text):
    """
    Find the endIndex of the paragraph whose text contains anchor_text.
    Returns the endIndex (which is the start of the next paragraph's newline).
    """
    content = doc.get('body', {}).get('content', [])
    for element in content:
        if 'paragraph' not in element:
            continue
        text = ''
        for elem in element['paragraph'].get('elements', []):
            if 'textRun' in elem:
                text += elem['textRun']['content']
        if anchor_text in text.strip():
            return element.get('endIndex', 0)
    return None


def find_heading_start(doc, heading_text):
    """
    Find the startIndex of a heading paragraph containing heading_text.
    """
    content = doc.get('body', {}).get('content', [])
    for element in content:
        if 'paragraph' not in element:
            continue
        style = element['paragraph'].get('paragraphStyle', {}).get('namedStyleType', '')
        if 'HEADING' not in style:
            continue
        text = ''
        for elem in element['paragraph'].get('elements', []):
            if 'textRun' in elem:
                text += elem['textRun']['content']
        if heading_text in text.strip():
            return element.get('startIndex', 0)
    return None


def insert_figure(anchor_text, anchor_mode, caption_text, image_url, width=468, height=350):
    """
    Insert a figure (image + caption) at the specified location.

    anchor_mode:
      'after_paragraph' - insert after the paragraph containing anchor_text
      'before_heading' - insert before the heading containing anchor_text
    """
    doc = get_doc()

    if anchor_mode == 'after_paragraph':
        # Find end of the anchor paragraph
        end_idx = find_paragraph_end(doc, anchor_text)
        if end_idx is None:
            print(f"  ERROR: Could not find paragraph containing: '{anchor_text[:60]}...'")
            return False
        # Insert point is at end_idx - 1 (before the newline of the anchor paragraph)
        # Actually, we want to insert AFTER the paragraph, so at end_idx
        # But we need to insert a newline first, then the caption, then the image before it
        insert_at = end_idx - 1  # before the trailing newline of the last paragraph in the section

    elif anchor_mode == 'before_heading':
        start_idx = find_heading_start(doc, anchor_text)
        if start_idx is None:
            print(f"  ERROR: Could not find heading containing: '{anchor_text[:60]}...'")
            return False
        insert_at = start_idx - 1  # before the heading's paragraph
    else:
        print(f"  ERROR: Unknown anchor_mode: {anchor_mode}")
        return False

    print(f"  Found anchor. Insert point: {insert_at}")

    # Step 1: Insert caption text (newline + caption + newline)
    caption_with_newlines = f"\n{caption_text}\n"

    try:
        batch_update([{
            'insertText': {
                'location': {'index': insert_at},
                'text': caption_with_newlines,
            }
        }])
        print(f"  Inserted caption text at {insert_at}")
    except Exception as e:
        print(f"  ERROR inserting caption text: {str(e)[:300]}")
        return False

    time.sleep(1.5)

    # Step 2: Re-read doc, find the caption we just inserted, and format it
    doc = get_doc()
    content = doc.get('body', {}).get('content', [])

    caption_start = None
    caption_end = None
    for element in content:
        if 'paragraph' not in element:
            continue
        text = ''
        for elem in element['paragraph'].get('elements', []):
            if 'textRun' in elem:
                text += elem['textRun']['content']
        if caption_text in text.strip():
            caption_start = element.get('startIndex', 0)
            caption_end = element.get('endIndex', 0)
            break

    if caption_start is None:
        print(f"  ERROR: Could not find inserted caption text")
        return False

    print(f"  Caption found at [{caption_start}-{caption_end}]")

    # Format the caption: italic, centered, Times New Roman 12pt
    try:
        batch_update([
            {
                'updateTextStyle': {
                    'range': {'startIndex': caption_start, 'endIndex': caption_end - 1},
                    'textStyle': {
                        'italic': True,
                        'weightedFontFamily': {'fontFamily': 'Times New Roman'},
                        'fontSize': {'magnitude': 12, 'unit': 'PT'},
                    },
                    'fields': 'italic,weightedFontFamily,fontSize',
                }
            },
            {
                'updateParagraphStyle': {
                    'range': {'startIndex': caption_start, 'endIndex': caption_end - 1},
                    'paragraphStyle': {
                        'alignment': 'CENTER',
                        'indentFirstLine': {'magnitude': 0, 'unit': 'PT'},
                        'indentStart': {'magnitude': 0, 'unit': 'PT'},
                    },
                    'fields': 'alignment,indentFirstLine,indentStart',
                }
            }
        ])
        print(f"  Caption formatted (italic, centered)")
    except Exception as e:
        print(f"  ERROR formatting caption: {str(e)[:300]}")
        # Continue anyway - the text is there

    time.sleep(1.5)

    # Step 3: Re-read doc again, insert image before the caption
    doc = get_doc()
    content = doc.get('body', {}).get('content', [])

    # Find caption again for fresh index
    img_insert_idx = None
    for element in content:
        if 'paragraph' not in element:
            continue
        text = ''
        for elem in element['paragraph'].get('elements', []):
            if 'textRun' in elem:
                text += elem['textRun']['content']
        if caption_text in text.strip():
            img_insert_idx = element.get('startIndex', 0)
            break

    if img_insert_idx is None:
        print(f"  ERROR: Could not find caption for image insertion")
        return False

    print(f"  Inserting image at index {img_insert_idx}...")

    try:
        batch_update([{
            'insertInlineImage': {
                'location': {'index': img_insert_idx},
                'uri': image_url,
                'objectSize': {
                    'width': {'magnitude': width, 'unit': 'PT'},
                    'height': {'magnitude': height, 'unit': 'PT'},
                }
            }
        }])
        print(f"  SUCCESS: Image inserted!")
    except Exception as e:
        print(f"  ERROR inserting image: {str(e)[:300]}")
        return False

    time.sleep(1.5)

    # Step 4: Center the image paragraph
    doc = get_doc()
    content = doc.get('body', {}).get('content', [])

    # Find the image paragraph (paragraph containing inlineObjectElement right before caption)
    for element in content:
        if 'paragraph' not in element:
            continue
        for elem in element['paragraph'].get('elements', []):
            if 'inlineObjectElement' in elem:
                # Check if next paragraph is our caption
                el_start = element.get('startIndex', 0)
                el_end = element.get('endIndex', 0)
                # Look for caption right after
                for next_el in content:
                    if next_el.get('startIndex', 0) == el_end:
                        if 'paragraph' in next_el:
                            next_text = ''
                            for ne in next_el['paragraph'].get('elements', []):
                                if 'textRun' in ne:
                                    next_text += ne['textRun']['content']
                            if caption_text in next_text:
                                # This is the image paragraph
                                try:
                                    batch_update([{
                                        'updateParagraphStyle': {
                                            'range': {'startIndex': el_start, 'endIndex': el_end - 1},
                                            'paragraphStyle': {
                                                'alignment': 'CENTER',
                                                'indentFirstLine': {'magnitude': 0, 'unit': 'PT'},
                                                'indentStart': {'magnitude': 0, 'unit': 'PT'},
                                            },
                                            'fields': 'alignment,indentFirstLine,indentStart',
                                        }
                                    }])
                                    print(f"  Image paragraph centered")
                                except Exception as e:
                                    print(f"  Warning: Could not center image paragraph: {str(e)[:200]}")
                                break
                break

    return True


# ═══════════════════════════════════════════════════════════════════════════════
# Define the 7 figures with their anchor points
# ═══════════════════════════════════════════════════════════════════════════════

FIGURES = [
    {
        'name': 'Figure 1.1',
        'anchor_text': 'This thesis proposes a unified adaptive platform that incorporates all the components of the adaptive system.',
        'anchor_mode': 'after_paragraph',
        'caption': 'Figure 1.1. Research gap positioning: the thesis platform sits at the intersection of programming-specific design and adaptive learning, a space no existing platform fully occupies.',
        'url': 'https://files.catbox.moe/8w2yoy.png',
        'width': 468,
        'height': 350,
    },
    {
        'name': 'Figure 1.3',
        'anchor_text': 'The parameters used in each layer are explained in Chapter 4.',
        'anchor_mode': 'after_paragraph',
        'caption': 'Figure 1.3. Five-layer adaptive engine architecture overview.',
        'url': 'https://files.catbox.moe/ughnpo.png',
        'width': 468,
        'height': 350,
    },
    {
        'name': 'Figure 1.2',
        'anchor_text': 'This closed-loop approach to the adaptive engine means the learning cycle continuously adapts',
        'anchor_mode': 'after_paragraph',
        'caption': 'Figure 1.2. Closed-loop adaptive workflow showing continuous knowledge state updates.',
        'url': 'https://files.catbox.moe/7a37u4.png',
        'width': 468,
        'height': 350,
    },
    {
        'name': 'Figure 1.4',
        'anchor_text': 'Chapter 6: Conclusion presents a summary of key findings',
        'anchor_mode': 'after_paragraph',
        'caption': 'Figure 1.4. Thesis structure roadmap showing chapter flow, contributions, and research question mapping.',
        'url': 'https://files.catbox.moe/xj4fhd.png',
        'width': 468,
        'height': 400,
    },
    {
        'name': 'Figure 2.1',
        'anchor_text': 'Section 2.1 introduces the rel',  # intro paragraph of Ch2
        'anchor_mode': 'after_paragraph',
        'caption': 'Figure 2.1. Literature landscape map showing six research streams converging on the thesis.',
        'url': 'https://files.catbox.moe/d3k3b9.png',
        'width': 468,
        'height': 350,
    },
    {
        'name': 'Figure 2.2',
        'anchor_text': 'BKT is selected as the knowledge tracing engine for the proposed platform for several reasons',
        'anchor_mode': 'after_paragraph',
        'caption': 'Figure 2.2. Evolution of knowledge tracing: from BKT (1994) through DKT (2015) to DKT2 (2025).',
        'url': 'https://files.catbox.moe/226gnb.png',
        'width': 468,
        'height': 300,
    },
    {
        'name': 'Figure 2.3',
        'anchor_text': 'FSRS is applied as Layer 4 (Review Scheduler) in the proposed architecture',
        'anchor_mode': 'after_paragraph',
        'caption': 'Figure 2.3. Evolution of spaced repetition algorithms from Ebbinghaus to FSRS.',
        'url': 'https://files.catbox.moe/eg8hkf.png',
        'width': 468,
        'height': 300,
    },
]


def main():
    print("=" * 70)
    print("INSERT 7 MISSING FIGURES")
    print(f"Document: {DOC_ID}")
    print("=" * 70)

    success = 0
    fail = 0

    for i, fig in enumerate(FIGURES):
        print(f"\n{'─' * 70}")
        print(f"[{i+1}/7] {fig['name']}")
        print(f"  URL: {fig['url']}")
        print(f"  Caption: {fig['caption'][:80]}...")
        print(f"  Anchor: '{fig['anchor_text'][:60]}...'")
        print(f"{'─' * 70}")

        if insert_figure(
            anchor_text=fig['anchor_text'],
            anchor_mode=fig['anchor_mode'],
            caption_text=fig['caption'],
            image_url=fig['url'],
            width=fig['width'],
            height=fig['height'],
        ):
            success += 1
            print(f"  >>> {fig['name']} DONE")
        else:
            fail += 1
            print(f"  >>> {fig['name']} FAILED")

        # Wait between figures to avoid rate limits
        if i < len(FIGURES) - 1:
            time.sleep(3)

    print(f"\n{'=' * 70}")
    print(f"COMPLETE: {success} succeeded, {fail} failed out of 7")
    print(f"{'=' * 70}")


if __name__ == '__main__':
    main()
