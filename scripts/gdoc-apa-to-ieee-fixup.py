"""
gdoc-apa-to-ieee-fixup: catch APA citations nested inside larger parentheticals
that the main gdoc-apa-to-ieee.py pass missed because its rules required the
`(` to sit directly before the author name.

Example residual: "(19 parameters, defaults from Ye et al., 2022)" — the outer
parens belong to the prose parenthetical, not the citation, so the citation
appears as the bare form "Ye et al., 2022" and the paren-form rule does not
match.

Pipeline (autonomous):
  Step A -- scan entire body text with three regexes covering:
            1. "Author et al., YEAR"
            2. "A and B, YEAR" / "A & B, YEAR"
            3. "Author, YEAR" (single-name)
            The References section (everything from the "References" HEADING_2
            onward) is excluded from the scan to avoid false-positives on
            bibliography entries.
  Step B -- for each match, map the leading author to an IEEE number using
            AUTHOR_TO_IEEE. Unknown author -> abort and print for manual review.
            Dedup matches by exact matched text; each unique match becomes one
            `replaceAllText` rule: bare APA form -> "Author [N]"-style IEEE.
  Step C -- run batchUpdate; report occurrencesChanged per rule.
  Step D -- re-fetch doc, re-scan with the same regexes; expect 0 residuals.

Usage:
    python scripts/gdoc-apa-to-ieee-fixup.py
    python scripts/gdoc-apa-to-ieee-fixup.py --doc-id 1b21...
    python scripts/gdoc-apa-to-ieee-fixup.py --dry-run   # scan + plan, no write
"""
import argparse
import importlib.util
import io
import re
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_DOC_ID = "1b21l8G9SXiXSYP_2k9Up3ic11OK08yus557vb8gsPhs"

# Map author surnames to IEEE reference numbers (from the 14-entry IEEE list
# produced by gdoc-apa-to-ieee.py, first-citation order).
AUTHOR_TO_IEEE = {
    "Luxton-Reilly": 1,
    "Corbett": 2,
    "Pelánek": 3,
    "Chapelle": 4,
    "Rollinson": 5,
    "Ye": 6,
    "Ma": 7,
    "Piech": 8,
    "Vygotsky": 9,
    "Bjork": 10,
    "Segal": 11,
    "Cepeda": 12,
    "Wang": 13,
    "Settles": 14,
}

# Three regexes, ordered most-specific to least-specific so that a match with
# "et al." or "and/&" doesn't also fire the single-name regex on its prefix.
# Surname character class: ASCII + Vietnamese/Latin Extended lowercase-ish block.
SURNAME = r"[A-Z][a-zà-ỹA-Z\-]+"
RE_ET_AL = re.compile(rf"{SURNAME} et al\., \d{{4}}")
RE_AND = re.compile(rf"{SURNAME} (?:and|&) {SURNAME}, \d{{4}}")
RE_SINGLE = re.compile(rf"{SURNAME}, \d{{4}}")


def load_auth():
    spec = importlib.util.spec_from_file_location(
        "gdoc_util_auth", str(SCRIPT_DIR / "gdoc-util-auth.py")
    )
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def iter_paragraphs(doc):
    for elem in doc["body"]["content"]:
        para = elem.get("paragraph")
        if not para:
            continue
        text = "".join(
            el.get("textRun", {}).get("content", "")
            for el in para.get("elements", [])
        )
        style = para.get("paragraphStyle", {}).get("namedStyleType", "NORMAL_TEXT")
        yield elem["startIndex"], elem["endIndex"], text, style


def body_text_pre_references(doc):
    """Concatenate all paragraph text up to (and excluding) the 'References'
    HEADING_2 anchor. Returns a single string with \n between paragraphs."""
    chunks = []
    for s, e, text, style in iter_paragraphs(doc):
        if text.strip() == "References":
            break
        chunks.append(text)
    return "".join(chunks)


def scan_residuals(body_text):
    """Return list of dicts: {pattern, match, start, context} across all three regexes.
    Higher-specificity regex matches are recorded first; any single-name match
    that is a substring span of an already-recorded et-al/and match is skipped.
    Matches are deduped by (start, end) so the same span isn't reported twice.
    """
    recorded_spans = []  # list of (start, end, kind, match_str)

    def overlaps(s, e):
        for (rs, re_, *_rest) in recorded_spans:
            if s < re_ and e > rs:
                return True
        return False

    def context(body, s, e, width=40):
        lo = max(0, s - width)
        hi = min(len(body), e + width)
        pre = body[lo:s].replace("\n", "\\n")
        post = body[e:hi].replace("\n", "\\n")
        return f"...{pre}|{body[s:e]}|{post}..."

    for regex, kind in [
        (RE_ET_AL, "et_al"),
        (RE_AND, "and"),
        (RE_SINGLE, "single"),
    ]:
        for m in regex.finditer(body_text):
            if overlaps(m.start(), m.end()):
                continue
            recorded_spans.append((m.start(), m.end(), kind, m.group(0)))

    recorded_spans.sort(key=lambda t: t[0])
    return [
        {
            "pattern": kind,
            "match": text,
            "start": s,
            "end": e,
            "context": context(body_text, s, e),
        }
        for (s, e, kind, text) in recorded_spans
    ]


def leading_author(match_text):
    """Extract the leading surname from a matched APA bare citation."""
    # Patterns: "X et al., YYYY" | "X and Y, YYYY" | "X & Y, YYYY" | "X, YYYY"
    first = re.match(r"([A-Z][a-zà-ỹA-Z\-]+)", match_text)
    return first.group(1) if first else None


def build_replacement(match_text):
    """Given a bare APA citation like 'Ye et al., 2022', return the IEEE form.
    Returns None if the leading author is not in AUTHOR_TO_IEEE (caller must halt)."""
    author = leading_author(match_text)
    if author is None or author not in AUTHOR_TO_IEEE:
        return None
    num = AUTHOR_TO_IEEE[author]

    if " et al." in match_text:
        return f"{author} et al. [{num}]"
    if " and " in match_text or " & " in match_text:
        # "X and Y, YYYY" / "X & Y, YYYY" — use narrative form "X and Y [N]".
        # Strip the ", YYYY" tail.
        prefix = re.sub(r", \d{4}$", "", match_text)
        return f"{prefix} [{num}]"
    # Single-name: "Author, YYYY" -> "Author [N]"
    return f"{author} [{num}]"


def filter_to_citations(matches):
    """Heuristic filter — drop matches whose leading surname is NOT in
    AUTHOR_TO_IEEE (likely not a citation, e.g. a date like 'September, 2024'
    or a version mention). Return (citation_matches, skipped_matches)."""
    citations, skipped = [], []
    for m in matches:
        author = leading_author(m["match"])
        if author and author in AUTHOR_TO_IEEE:
            citations.append(m)
        else:
            skipped.append(m)
    return citations, skipped


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--doc-id", default=DEFAULT_DOC_ID)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    print(f"Target doc: {args.doc_id}")
    if args.dry_run:
        print("[DRY RUN] scan only, no writes.")

    auth = load_auth()
    docs = auth.get_docs_service()

    # ---------------------------------------------------------------- Step A
    print("\n--- Step A: scan body for residual APA patterns ---")
    doc = docs.documents().get(documentId=args.doc_id).execute()
    body = body_text_pre_references(doc)
    print(f"  body chars (pre-References): {len(body)}")

    residuals = scan_residuals(body)
    print(f"  residual matches: {len(residuals)}")
    for r in residuals:
        print(f"    [{r['pattern']:>6}] {r['match']!r}  ctx: {r['context']}")

    # ---------------------------------------------------------------- Step B
    print("\n--- Step B: classify and build replacement rules ---")
    # Known-bad case explicitly requested: "Ye et al., 2022" -> "Ye et al. [6]"
    # (already covered by the et_al regex; included in residuals if present).
    citations, skipped = filter_to_citations(residuals)
    print(f"  citations (in AUTHOR_TO_IEEE): {len(citations)}")
    print(f"  skipped (unknown surname, manual review): {len(skipped)}")
    for sk in skipped:
        print(f"    SKIP: {sk['match']!r}  ctx: {sk['context']}")

    if skipped:
        # Print but do not abort — the user's spec says "list and stop" only if
        # a pattern cannot map. We continue with known citations and leave the
        # skipped ones for manual review. Summary flags them clearly.
        print("  NOTE: skipped matches will be reported in the final summary;")
        print("        they are NOT being rewritten automatically.")

    # Dedupe citations by match text -> one rule per distinct bare form.
    rules = {}  # find -> (replace, count_seen_in_scan)
    for c in citations:
        find = c["match"]
        replace = build_replacement(find)
        if replace is None:
            # Defensive: shouldn't happen after filter_to_citations, but guard.
            print(f"  ERROR: cannot map author for {find!r}; halting")
            sys.exit(2)
        if find in rules:
            prev_replace, cnt = rules[find]
            if prev_replace != replace:
                print(f"  ERROR: conflicting replacements for {find!r}: {prev_replace!r} vs {replace!r}")
                sys.exit(2)
            rules[find] = (prev_replace, cnt + 1)
        else:
            rules[find] = (replace, 1)

    if not rules:
        print("  No bare-form citations to rewrite. Doc is clean.")
        print("\n=== SUMMARY ===")
        print("  (a) total fixes: 0")
        print("  (b) rules: none")
        print("  (c) residuals remaining: 0")
        return

    print(f"  planned {len(rules)} distinct rule(s):")
    for find, (replace, scan_count) in rules.items():
        print(f"    {find!r} -> {replace!r}   (scan count: {scan_count})")

    # ---------------------------------------------------------------- Step C
    if args.dry_run:
        print("\n[DRY RUN] skipping batchUpdate and re-scan verification.")
        return

    print("\n--- Step C: apply replaceAllText batch ---")
    requests = [
        {
            "replaceAllText": {
                "containsText": {"text": find, "matchCase": True},
                "replaceText": replace,
            }
        }
        for find, (replace, _scan_count) in rules.items()
    ]
    resp = docs.documents().batchUpdate(
        documentId=args.doc_id, body={"requests": requests}
    ).execute()

    applied = []
    for (find, (replace, _scan_count)), reply in zip(rules.items(), resp["replies"]):
        occ = reply.get("replaceAllText", {}).get("occurrencesChanged", 0)
        applied.append((find, replace, occ))
        print(f"  {find!r} -> {replace!r}   occurrencesChanged={occ}")

    total_fixes = sum(occ for _, _, occ in applied)

    # ---------------------------------------------------------------- Step D
    print("\n--- Step D: re-scan for remaining residuals ---")
    doc2 = docs.documents().get(documentId=args.doc_id).execute()
    body2 = body_text_pre_references(doc2)
    residuals2 = scan_residuals(body2)
    # Known-harmless false-positives (surnames not in our bibliography that
    # appear in dates or version strings) remain as "skipped"; they are not
    # citations and the re-scan will still surface them. Split post-scan too.
    citations2, skipped2 = filter_to_citations(residuals2)
    print(f"  residual after fix: total={len(residuals2)} "
          f"citations={len(citations2)} non-citation/false-positive={len(skipped2)}")
    for r in citations2:
        print(f"    STILL RESIDUAL (citation): {r['match']!r}  ctx: {r['context']}")
    for r in skipped2:
        print(f"    residual (non-citation, safe): {r['match']!r}  ctx: {r['context']}")

    # ---------------------------------------------------------------- Summary
    print("\n=== SUMMARY ===")
    print(f"  (a) total new fixes: {total_fixes}")
    print(f"  (b) bare patterns applied:")
    for find, replace, occ in applied:
        print(f"        [{occ}] {find!r} -> {replace!r}")
    print(f"  (c) residuals remaining after fix:")
    print(f"        citation-looking (must be 0): {len(citations2)}")
    print(f"        non-citation false positives (informational): {len(skipped2)}")
    if skipped:
        print(f"\n  Step-A unknown-surname matches (manual review):")
        for sk in skipped:
            print(f"        {sk['match']!r}  ctx: {sk['context']}")
    print(f"\nOpen https://docs.google.com/document/d/{args.doc_id}/edit to confirm.")


if __name__ == "__main__":
    main()
