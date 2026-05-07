"""
gdoc-write-conference-paper-docx: replace the conference-paper Google Doc's body by
re-importing a DOCX file via Drive API files.update, preserving formatting
(headings, bold/italic, tables, figures, paragraph spacing).

How it works:
  The Drive API, when you PATCH an existing Google Doc file with a .docx body and
  Content-Type application/vnd.openxmlformats-officedocument.wordprocessingml.document,
  converts the uploaded DOCX and replaces the doc's content in place. The doc ID,
  sharing, and bookmarked URL stay the same. This is the same import Drive performs
  when you drag-drop a .docx into Drive with "Convert uploads" enabled.

Why this is NOT done via Docs API batchUpdate:
  Docs API insertText inserts plain text only — it strips DOCX styling. Drive's
  native DOCX importer is the only supported path that preserves fonts, headings,
  italics, tables, etc.

Source:     Bài báo tham dự hội thảo khoa học.docx (project root) by default
Target doc: env GDOC_CONF_DOC_ID (default: 1b21l8G9SXiXSYP_2k9Up3ic11OK08yus557vb8gsPhs)

Required OAuth scope: https://www.googleapis.com/auth/drive (NOT drive.file —
drive.file only allows access to files the app itself created/opened).
gdoc-util-auth.py already declares this full-drive scope for the service account.

Usage:
    python scripts/gdoc-write-conference-paper-docx.py
    python scripts/gdoc-write-conference-paper-docx.py --source "path/to/file.docx"
    python scripts/gdoc-write-conference-paper-docx.py --doc-id <ID>
    python scripts/gdoc-write-conference-paper-docx.py --dry-run
"""
import argparse
import importlib.util
import io
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
DEFAULT_SOURCE = PROJECT_ROOT / "Bài báo tham dự hội thảo khoa học.docx"
DEFAULT_DOC_ID = "1b21l8G9SXiXSYP_2k9Up3ic11OK08yus557vb8gsPhs"
DOCX_MIME = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
GDOC_MIME = "application/vnd.google-apps.document"


def load_auth():
    spec = importlib.util.spec_from_file_location(
        "gdoc_util_auth", str(SCRIPT_DIR / "gdoc-util-auth.py")
    )
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def verify_read(docs, doc_id, n_chars=300):
    """Read the first n_chars of visible text from the doc."""
    doc = docs.documents().get(documentId=doc_id).execute()
    buf = []
    remaining = n_chars
    for elem in doc["body"]["content"]:
        para = elem.get("paragraph")
        table = elem.get("table")
        if para:
            for el in para.get("elements", []):
                tr = el.get("textRun")
                if not tr:
                    continue
                c = tr.get("content", "")
                buf.append(c)
                remaining -= len(c)
                if remaining <= 0:
                    break
        elif table:
            # traverse first cell to grab any table-leading text
            for row in table.get("tableRows", []):
                for cell in row.get("tableCells", []):
                    for inner in cell.get("content", []):
                        p = inner.get("paragraph")
                        if not p:
                            continue
                        for el in p.get("elements", []):
                            tr = el.get("textRun")
                            if not tr:
                                continue
                            c = tr.get("content", "")
                            buf.append(c)
                            remaining -= len(c)
                            if remaining <= 0:
                                break
                        if remaining <= 0:
                            break
                    if remaining <= 0:
                        break
                if remaining <= 0:
                    break
        if remaining <= 0:
            break
    return "".join(buf)[:n_chars]


def count_structural_elements(docs, doc_id):
    """Rough structural summary of the doc — paragraphs by style, tables, images."""
    doc = docs.documents().get(documentId=doc_id).execute()
    style_counts = {}
    n_tables = 0
    n_images = 0
    n_bold_runs = 0
    n_italic_runs = 0
    for elem in doc["body"]["content"]:
        if "table" in elem:
            n_tables += 1
        para = elem.get("paragraph")
        if not para:
            continue
        style = para.get("paragraphStyle", {}).get("namedStyleType", "NORMAL_TEXT")
        style_counts[style] = style_counts.get(style, 0) + 1
        for el in para.get("elements", []):
            if "inlineObjectElement" in el:
                n_images += 1
            tr = el.get("textRun")
            if not tr:
                continue
            ts = tr.get("textStyle", {})
            if ts.get("bold"):
                n_bold_runs += 1
            if ts.get("italic"):
                n_italic_runs += 1
    return {
        "paragraphs_by_style": style_counts,
        "tables": n_tables,
        "inline_images": n_images,
        "bold_runs": n_bold_runs,
        "italic_runs": n_italic_runs,
    }


def upload_docx_as_doc(drive, doc_id, docx_path):
    """PATCH the existing Google Doc with the DOCX body; Drive re-imports it.

    Uses MediaFileUpload + files().update with the DOCX mime_type on the media
    and targetMimeType=application/vnd.google-apps.document via the file metadata
    is implicit (the existing file is already a Google Doc). Drive detects the
    incoming DOCX media and converts on import.
    """
    from googleapiclient.http import MediaFileUpload

    media = MediaFileUpload(
        str(docx_path),
        mimetype=DOCX_MIME,
        resumable=False,
    )
    # No metadata body needed — we only want to replace the content.
    # Drive auto-converts DOCX media into the existing Google Doc in place.
    updated = drive.files().update(
        fileId=doc_id,
        media_body=media,
        fields="id,name,mimeType,modifiedTime,size",
        supportsAllDrives=True,
    ).execute()
    return updated


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--source", default=str(DEFAULT_SOURCE))
    ap.add_argument("--doc-id", default=DEFAULT_DOC_ID)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    src = Path(args.source)
    if not src.exists():
        print(f"ERROR: source DOCX not found: {src}")
        sys.exit(1)
    if src.suffix.lower() != ".docx":
        print(f"ERROR: source is not a .docx file: {src}")
        sys.exit(1)

    size_kb = src.stat().st_size / 1024
    print(f"Source DOCX:  {src}")
    print(f"  Size:       {size_kb:.1f} KB")
    print(f"Target doc:   https://docs.google.com/document/d/{args.doc_id}/edit")

    if args.dry_run:
        print("\n[DRY RUN] would PATCH Drive file with the DOCX above.")
        return

    auth = load_auth()
    print(f"Auth scopes:  {auth.SCOPES}")
    if "https://www.googleapis.com/auth/drive" not in auth.SCOPES:
        print("ERROR: drive scope not present in gdoc-util-auth.SCOPES — aborting.")
        print("       Re-auth with the full /auth/drive scope before retrying.")
        sys.exit(2)

    drive = auth.get_drive_service()
    docs = auth.get_docs_service()

    # Pre-flight: confirm the target is actually a Google Doc (so DOCX re-import is valid).
    print("\nPre-flight: checking target file metadata...")
    try:
        meta = drive.files().get(
            fileId=args.doc_id,
            fields="id,name,mimeType,modifiedTime",
            supportsAllDrives=True,
        ).execute()
    except Exception as e:
        print(f"ERROR: could not fetch target file metadata: {e}")
        sys.exit(3)
    print(f"  name:      {meta.get('name')}")
    print(f"  mimeType:  {meta.get('mimeType')}")
    print(f"  modified:  {meta.get('modifiedTime')}")
    if meta.get("mimeType") != GDOC_MIME:
        print(f"ERROR: target is not a Google Doc (got {meta.get('mimeType')}); refusing to overwrite.")
        sys.exit(4)

    print("\nUploading DOCX via Drive files.update (Drive will re-import/convert)...")
    updated = upload_docx_as_doc(drive, args.doc_id, src)
    print(f"  Drive returned: name={updated.get('name')}  mimeType={updated.get('mimeType')}  modified={updated.get('modifiedTime')}")
    if updated.get("mimeType") != GDOC_MIME:
        print(f"WARN: after update, mimeType is {updated.get('mimeType')} (expected Google Doc). Proceeding to verify anyway.")

    # Verify: read doc contents via Docs API.
    print("\n--- Verify: first 300 chars of doc body ---")
    first300 = verify_read(docs, args.doc_id, 300)
    print(first300)
    print("--- end verify ---")

    # Find a citation marker in the first 6000 chars.
    doc_head = verify_read(docs, args.doc_id, 6000)
    found_1 = "[1]" in doc_head

    # Structural fingerprint post-import.
    print("\nStructural summary (via Docs API):")
    summary = count_structural_elements(docs, args.doc_id)
    for k, v in summary.items():
        print(f"  {k}: {v}")

    print("\nVerification checks:")
    print(f"  contains '[1]' in first 6000 chars: {found_1}")
    # Vietnamese title check — loose: look for diacritics / specific keyword fragments
    # from the known paper title without hardcoding the exact line.
    vi_markers = ["Nghiên cứu", "học tập", "thích ứng", "cá nhân", "sinh viên"]
    vi_hits = [m for m in vi_markers if m in doc_head]
    print(f"  Vietnamese title markers found: {vi_hits}")

    print("\n=== DONE ===")
    print(f"Open https://docs.google.com/document/d/{args.doc_id}/edit to verify visually.")


if __name__ == "__main__":
    main()
