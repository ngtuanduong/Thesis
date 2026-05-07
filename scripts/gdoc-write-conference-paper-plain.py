"""
gdoc-write-conference-paper-plain: overwrite the conference-paper Google Doc with the
contents of a plain text file, one paragraph per line, preserving the document's
existing paragraph style (no new formatting applied).

Source:     Bài báo tham dự hội thảo khoa học.txt (project root) by default
Target doc: env GDOC_CONF_DOC_ID (default: 1b21l8G9SXiXSYP_2k9Up3ic11OK08yus557vb8gsPhs)

Why a separate script from gdoc-write-conference-paper.py: that one parses a tagged
markdown assembly file (<!-- TITLE_VI_BEGIN --> etc.) and applies HTKH 2025 styling.
This script is for a plain .txt mirror of the same paper after the references/citations
were rewritten to IEEE format, where the goal is a literal content overwrite with no
styling side-effects.

Usage:
    python scripts/gdoc-write-conference-paper-plain.py
    python scripts/gdoc-write-conference-paper-plain.py --source "path/to/file.txt"
    python scripts/gdoc-write-conference-paper-plain.py --doc-id <ID>
    python scripts/gdoc-write-conference-paper-plain.py --dry-run
"""
import argparse
import importlib.util
import io
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
DEFAULT_SOURCE = PROJECT_ROOT / "Bài báo tham dự hội thảo khoa học.txt"
DEFAULT_DOC_ID = "1b21l8G9SXiXSYP_2k9Up3ic11OK08yus557vb8gsPhs"


def load_auth():
    spec = importlib.util.spec_from_file_location(
        "gdoc_util_auth", str(SCRIPT_DIR / "gdoc-util-auth.py")
    )
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def get_end_index(docs, doc_id):
    doc = docs.documents().get(documentId=doc_id).execute()
    content = doc["body"]["content"]
    return content[-1]["endIndex"] if content else 1


def clear_doc(docs, doc_id):
    end = get_end_index(docs, doc_id)
    if end > 2:
        docs.documents().batchUpdate(
            documentId=doc_id,
            body={"requests": [{"deleteContentRange": {"range": {"startIndex": 1, "endIndex": end - 1}}}]},
        ).execute()


def build_text(lines):
    """Join non-empty lines with a single '\n' (one paragraph per line).
    Skip empty lines so the doc does not end up with empty paragraphs.
    The trailing newline is omitted — Docs always has an implicit final paragraph."""
    kept = [ln for ln in (l.rstrip("\r\n") for l in lines) if ln.strip() != ""]
    return "\n".join(kept)


def verify_read(docs, doc_id, n_chars=200):
    doc = docs.documents().get(documentId=doc_id).execute()
    buf = []
    remaining = n_chars
    for elem in doc["body"]["content"]:
        para = elem.get("paragraph")
        if not para:
            continue
        for el in para.get("elements", []):
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
    joined = "".join(buf)
    return joined[:n_chars]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--source", default=str(DEFAULT_SOURCE))
    ap.add_argument("--doc-id", default=DEFAULT_DOC_ID)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    src = Path(args.source)
    if not src.exists():
        print(f"ERROR: source file not found: {src}")
        sys.exit(1)

    raw = src.read_text(encoding="utf-8-sig")  # utf-8-sig strips a leading BOM if present
    lines = raw.splitlines()
    payload = build_text(lines)
    print(f"Source file: {src}")
    print(f"  {len(lines)} raw lines, {sum(1 for l in lines if l.strip())} non-empty lines")
    print(f"  Payload length: {len(payload)} chars")
    print(f"  First 120 chars of payload: {payload[:120]!r}")

    if args.dry_run:
        print("\n[DRY RUN] would clear doc and insert the payload above.")
        return

    auth = load_auth()
    docs = auth.get_docs_service()

    print(f"\nTarget doc: {args.doc_id}")
    end_before = get_end_index(docs, args.doc_id)
    print(f"Current doc endIndex: {end_before}")

    print("Clearing doc content...")
    clear_doc(docs, args.doc_id)
    end_after_clear = get_end_index(docs, args.doc_id)
    print(f"endIndex after clear: {end_after_clear}")

    print(f"Inserting {len(payload)} chars at index 1...")
    docs.documents().batchUpdate(
        documentId=args.doc_id,
        body={"requests": [{"insertText": {"location": {"index": 1}, "text": payload}}]},
    ).execute()
    end_after_insert = get_end_index(docs, args.doc_id)
    print(f"endIndex after insert: {end_after_insert}")

    print("\n--- Verify: first 200 chars read back from doc ---")
    first200 = verify_read(docs, args.doc_id, 200)
    print(first200)
    print("--- end verify ---")

    # Look for any IEEE numeric citation [N] in the first 4000 chars of the doc body
    doc_head = verify_read(docs, args.doc_id, 4000)
    found_1 = "[1]" in doc_head
    print(f"\n[1] found in first 4000 chars: {found_1}")

    print("\n=== DONE ===")
    print(f"Open https://docs.google.com/document/d/{args.doc_id}/edit to verify.")


if __name__ == "__main__":
    main()
