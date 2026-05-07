"""
gdoc-read-comments: fetch comments from a Google Doc via the Drive API v3.

Outputs 2 files into documents/thesis-chapters/review/:
    - thesis-comments-raw.jsonl   (1 comment per line, raw Drive response)
    - thesis-comments-report.md   (human-readable report)

Default filter: only unresolved + non-deleted comments.

Usage:
    python scripts/gdoc-read-comments.py
    python scripts/gdoc-read-comments.py --doc-id <FILE_ID>
    python scripts/gdoc-read-comments.py --include-resolved
    GDOC_COMMENT_DOC_ID=<id> python scripts/gdoc-read-comments.py

Prerequisite: the target doc must be shared with the service account
(service-account@infra-inkwell-465003-f2.iam.gserviceaccount.com) as Viewer.
"""
import argparse
import importlib.util
import io
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
OUTPUT_DIR = PROJECT_ROOT / "documents" / "thesis-chapters" / "review"

DEFAULT_DOC_ID = "1B72mF57eyHFaCgTI-zVvZ01RWOuJInFemI-dVl_qxvA"

COMMENT_FIELDS = (
    "comments("
    "id,author(displayName,emailAddress),content,htmlContent,"
    "createdTime,modifiedTime,resolved,deleted,"
    "quotedFileContent(value,mimeType),anchor,"
    "replies(id,author(displayName,emailAddress),content,createdTime,modifiedTime)"
    "),nextPageToken"
)


def load_auth():
    spec = importlib.util.spec_from_file_location(
        "gdoc_util_auth", str(SCRIPT_DIR / "gdoc-util-auth.py")
    )
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def fetch_all_comments(drive, file_id):
    out = []
    page_token = None
    while True:
        req = drive.comments().list(
            fileId=file_id,
            fields=COMMENT_FIELDS,
            pageSize=100,
            pageToken=page_token,
        )
        resp = req.execute()
        out.extend(resp.get("comments", []))
        page_token = resp.get("nextPageToken")
        if not page_token:
            break
    return out


def render_report(comments, doc_id, include_resolved):
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    lines = []
    lines.append(f"# Thesis Comments Report")
    lines.append("")
    lines.append(f"- **Doc ID:** `{doc_id}`")
    lines.append(f"- **Pulled at (UTC):** {now}")
    lines.append(f"- **Filter:** {'open + resolved' if include_resolved else 'unresolved only'}")
    lines.append(f"- **Total comments:** {len(comments)}")
    lines.append("")
    lines.append("---")
    lines.append("")

    for i, c in enumerate(comments, 1):
        author = (c.get("author") or {}).get("displayName") or "unknown"
        email = (c.get("author") or {}).get("emailAddress") or ""
        created = c.get("createdTime", "")
        modified = c.get("modifiedTime", "")
        resolved = c.get("resolved", False)
        quoted = ((c.get("quotedFileContent") or {}).get("value") or "").strip()
        content = (c.get("content") or "").strip()
        replies = c.get("replies") or []
        cid = c.get("id", "")

        status = "RESOLVED" if resolved else "OPEN"
        header = f"## Comment #{i} — {author}"
        if email:
            header += f" ({email})"
        header += f" — {status}"
        lines.append(header)
        lines.append("")
        lines.append(f"- **Comment ID:** `{cid}`")
        lines.append(f"- **Created:** {created}")
        if modified and modified != created:
            lines.append(f"- **Modified:** {modified}")
        lines.append("")

        if quoted:
            lines.append("**Quoted text:**")
            lines.append("")
            for qline in quoted.splitlines() or [""]:
                lines.append(f"> {qline}")
            lines.append("")
        else:
            lines.append("**Quoted text:** _(none — comment on image/table or unanchored)_")
            lines.append("")

        lines.append("**Comment:**")
        lines.append("")
        lines.append(content if content else "_(empty)_")
        lines.append("")

        if replies:
            lines.append(f"**Replies ({len(replies)}):**")
            lines.append("")
            for r in replies:
                r_author = (r.get("author") or {}).get("displayName") or "unknown"
                r_created = r.get("createdTime", "")
                r_content = (r.get("content") or "").strip() or "_(empty)_"
                lines.append(f"- **{r_author}** ({r_created}):")
                for rline in r_content.splitlines():
                    lines.append(f"  > {rline}")
            lines.append("")

        lines.append("---")
        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--doc-id",
        default=os.environ.get("GDOC_COMMENT_DOC_ID", DEFAULT_DOC_ID),
        help="Google Doc / Drive file ID (default: %(default)s)",
    )
    parser.add_argument(
        "--include-resolved",
        action="store_true",
        help="Include resolved comments (default: unresolved only)",
    )
    parser.add_argument(
        "--output-dir",
        default=str(OUTPUT_DIR),
        help="Where to write output files (default: %(default)s)",
    )
    args = parser.parse_args()

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    auth = load_auth()
    drive = auth.get_drive_service()

    print(f"Fetching comments for doc {args.doc_id} ...")
    all_comments = fetch_all_comments(drive, args.doc_id)
    print(f"  total returned by Drive: {len(all_comments)}")

    filtered = [c for c in all_comments if not c.get("deleted")]
    if not args.include_resolved:
        filtered = [c for c in filtered if not c.get("resolved")]

    print(f"  after filter ({'open+resolved' if args.include_resolved else 'unresolved only'}): {len(filtered)}")

    jsonl_path = out_dir / "thesis-comments-raw.jsonl"
    with jsonl_path.open("w", encoding="utf-8") as f:
        for c in filtered:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")

    report_path = out_dir / "thesis-comments-report.md"
    report_path.write_text(
        render_report(filtered, args.doc_id, args.include_resolved),
        encoding="utf-8",
    )

    print(f"Wrote: {jsonl_path}")
    print(f"Wrote: {report_path}")


if __name__ == "__main__":
    main()
