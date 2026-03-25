#!/usr/bin/env python3
"""
Replace ALL existing inline images in the thesis Google Doc with updated versions,
and INSERT new images where captions exist but images are missing (Chapters 1 & 2).

Processes ONE image at a time, re-reading the document after each change.
"""

import time
import sys
from google.oauth2 import service_account
from googleapiclient.discovery import build

# ─── Configuration ───────────────────────────────────────────────────────────
DOC_ID = '1cJlWFX9QCEsqYo7mp6cpCWAba3Xc433-IRu8nlR63o0'
SERVICE_ACCOUNT_FILE = '/Users/avada/WebstormProjects/Thesis/infra-inkwell-465003-f2-369235afe5ac.json'
SCOPES = ['https://www.googleapis.com/auth/documents', 'https://www.googleapis.com/auth/drive']

# ─── Authenticate ────────────────────────────────────────────────────────────
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


# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 1: Replace existing Chapter 3 images
# ═══════════════════════════════════════════════════════════════════════════════
# Map from the caption text after each image -> new catbox URL and dimensions
# Based on discovery: each image is followed by a caption paragraph

CH3_REPLACEMENTS = [
    # (caption_starts_with, new_url, width_pt, height_pt)
    ('Figure 3.1.', 'https://files.catbox.moe/jys7rk.png', 468, 350),
    ('Table 3.1.', 'https://files.catbox.moe/4d3ygq.png', 468, 350),  # Design principles -> functional req tables
    ('Figure 3.2.', 'https://files.catbox.moe/sf8vd7.png', 468, 350),
    # Image #6 has "Table 3.3" before it and "Figure 3.6" after it — it's the hyperparameter table + layer matrix combo
    # Actually the caption BEFORE is "Table 3.3." and caption AFTER is "Figure 3.6."
    # This single image seems to be for Table 3.3 (hyperparameters). We need to replace it
    # and also insert Figure 3.6 separately.
    ('Table 3.3.', 'https://files.catbox.moe/la6fjg.png', 468, 400),
    ('Figure 3.3.', 'https://files.catbox.moe/5rfxe2.png', 468, 400),
    ('Figure 3.4.', 'https://files.catbox.moe/gebge3.png', 468, 350),
    ('Figure 3.7.', 'https://files.catbox.moe/wv360d.png', 468, 350),
    ('Figure 3.5.', 'https://files.catbox.moe/ljib2p.png', 468, 400),
    ('Table 3.5.', 'https://files.catbox.moe/0wxoie.png', 468, 300),
]


def find_image_before_caption(doc, caption_prefix):
    """
    Find an inline image that appears just before a caption matching caption_prefix.
    Returns the image's startIndex or None.
    """
    content = doc.get('body', {}).get('content', [])

    # Find the caption paragraph
    caption_element_idx = None
    for i, element in enumerate(content):
        if 'paragraph' not in element:
            continue
        text = ''
        for elem in element['paragraph'].get('elements', []):
            if 'textRun' in elem:
                text += elem['textRun']['content']
        if text.strip().startswith(caption_prefix):
            caption_element_idx = i
            break

    if caption_element_idx is None:
        return None

    # Look backwards from the caption for an image
    for j in range(caption_element_idx - 1, max(0, caption_element_idx - 5), -1):
        el = content[j]
        if 'paragraph' in el:
            for elem in el['paragraph'].get('elements', []):
                if 'inlineObjectElement' in elem:
                    return elem.get('startIndex', 0)

    return None


def find_caption_start(doc, caption_prefix):
    """Find the startIndex of a caption paragraph."""
    content = doc.get('body', {}).get('content', [])
    for element in content:
        if 'paragraph' not in element:
            continue
        text = ''
        for elem in element['paragraph'].get('elements', []):
            if 'textRun' in elem:
                text += elem['textRun']['content']
        if text.strip().startswith(caption_prefix):
            return element.get('startIndex', 0)
    return None


def replace_image(caption_prefix, new_url, width, height):
    """Replace an existing image (found before the caption) with a new one."""
    doc = get_doc()
    img_start = find_image_before_caption(doc, caption_prefix)

    if img_start is None:
        print(f"  WARNING: No image found before caption '{caption_prefix}' — will try INSERT instead")
        return insert_image_before_caption(caption_prefix, new_url, width, height)

    print(f"  Found image at index {img_start}, deleting...")

    # Delete old image
    try:
        batch_update([{
            'deleteContentRange': {
                'range': {
                    'startIndex': img_start,
                    'endIndex': img_start + 1,
                }
            }
        }])
    except Exception as e:
        print(f"  ERROR deleting: {str(e)[:200]}")
        return False

    time.sleep(1.5)

    # Re-read doc to get fresh index for the caption
    doc = get_doc()
    caption_start = find_caption_start(doc, caption_prefix)
    if caption_start is None:
        print(f"  ERROR: Caption '{caption_prefix}' not found after deletion")
        return False

    # Insert new image just before the caption
    insert_idx = caption_start

    print(f"  Inserting new image at index {insert_idx}...")
    try:
        result = batch_update([
            {
                'insertInlineImage': {
                    'location': {'index': insert_idx},
                    'uri': new_url,
                    'objectSize': {
                        'width': {'magnitude': width, 'unit': 'PT'},
                        'height': {'magnitude': height, 'unit': 'PT'},
                    }
                }
            }
        ])
        print(f"  SUCCESS: Inserted {new_url.split('/')[-1]}")
        return True
    except Exception as e:
        print(f"  ERROR inserting: {str(e)[:200]}")
        return False


def insert_image_before_caption(caption_prefix, new_url, width, height):
    """Insert an image before a caption where no image currently exists."""
    doc = get_doc()
    caption_start = find_caption_start(doc, caption_prefix)
    if caption_start is None:
        print(f"  ERROR: Caption '{caption_prefix}' not found")
        return False

    insert_idx = caption_start
    print(f"  Inserting new image at index {insert_idx} (before '{caption_prefix}')...")

    try:
        batch_update([
            {
                'insertInlineImage': {
                    'location': {'index': insert_idx},
                    'uri': new_url,
                    'objectSize': {
                        'width': {'magnitude': width, 'unit': 'PT'},
                        'height': {'magnitude': height, 'unit': 'PT'},
                    }
                }
            }
        ])
        print(f"  SUCCESS: Inserted {new_url.split('/')[-1]}")
        return True
    except Exception as e:
        print(f"  ERROR inserting: {str(e)[:200]}")
        return False


# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 2: Insert Chapter 1 & 2 images (captions exist, images don't)
# ═══════════════════════════════════════════════════════════════════════════════

CH1_INSERTIONS = [
    ('Table 1.1.', 'https://files.catbox.moe/9e9rxp.png', 468, 300),
    # Chapter 1 Figures: captions may not be in the doc yet. Let's check.
]

CH2_INSERTIONS = [
    ('Table 2.2.', 'https://files.catbox.moe/yuqiqy.png', 468, 400),
    ('Table 2.3.', 'https://files.catbox.moe/wjupha.png', 468, 300),
]

# Figures that might not have captions in the doc yet — we'll check and skip if missing
CH1_FIGURE_INSERTIONS = [
    ('Figure 1.1.', 'https://files.catbox.moe/8w2yoy.png', 468, 350),
    ('Figure 1.2.', 'https://files.catbox.moe/7a37u4.png', 468, 350),
    ('Figure 1.3.', 'https://files.catbox.moe/ughnpo.png', 468, 350),
    ('Figure 1.4.', 'https://files.catbox.moe/xj4fhd.png', 468, 400),
]

CH2_FIGURE_INSERTIONS = [
    ('Figure 2.1.', 'https://files.catbox.moe/d3k3b9.png', 468, 350),
    ('Figure 2.2.', 'https://files.catbox.moe/226gnb.png', 468, 300),
    ('Figure 2.3.', 'https://files.catbox.moe/eg8hkf.png', 468, 300),
]

# Figure 3.6 needs to be inserted (caption exists but no image above it)
CH3_INSERTIONS = [
    ('Figure 3.6.', 'https://files.catbox.moe/osuijb.png', 468, 350),
]


def main():
    print("=" * 70)
    print("VISUAL REPLACEMENT & INSERTION SCRIPT")
    print(f"Document: {DOC_ID}")
    print("=" * 70)

    success = 0
    fail = 0
    skip = 0

    # ─── PHASE 1: Replace existing Chapter 3 images ─────────────────────────
    print("\n" + "=" * 70)
    print("PHASE 1: Replacing existing Chapter 3 images")
    print("=" * 70)

    for caption_prefix, url, w, h in CH3_REPLACEMENTS:
        print(f"\n>>> {caption_prefix} -> {url.split('/')[-1]}")
        if replace_image(caption_prefix, url, w, h):
            success += 1
        else:
            fail += 1
        time.sleep(2)

    # ─── PHASE 2: Insert missing images (Ch 1, 2, and Ch 3 Figure 3.6) ─────
    print("\n" + "=" * 70)
    print("PHASE 2: Inserting missing images for Chapters 1, 2, and Figure 3.6")
    print("=" * 70)

    all_insertions = (
        CH1_INSERTIONS + CH1_FIGURE_INSERTIONS +
        CH2_INSERTIONS + CH2_FIGURE_INSERTIONS +
        CH3_INSERTIONS
    )

    for caption_prefix, url, w, h in all_insertions:
        print(f"\n>>> {caption_prefix} -> {url.split('/')[-1]}")

        # First check if caption exists
        doc = get_doc()
        caption_start = find_caption_start(doc, caption_prefix)
        if caption_start is None:
            print(f"  SKIP: Caption '{caption_prefix}' not found in document")
            skip += 1
            continue

        # Check if there's already an image before this caption
        img_start = find_image_before_caption(doc, caption_prefix)
        if img_start is not None:
            print(f"  Image already exists at {img_start}, replacing...")
            if replace_image(caption_prefix, url, w, h):
                success += 1
            else:
                fail += 1
        else:
            if insert_image_before_caption(caption_prefix, url, w, h):
                success += 1
            else:
                fail += 1

        time.sleep(2)

    # ─── Summary ────────────────────────────────────────────────────────────
    print(f"\n{'=' * 70}")
    print(f"COMPLETE")
    print(f"  Success: {success}")
    print(f"  Failed:  {fail}")
    print(f"  Skipped: {skip} (caption not found in document)")
    print(f"  Total:   {success + fail + skip}")
    print(f"{'=' * 70}")


if __name__ == '__main__':
    main()
