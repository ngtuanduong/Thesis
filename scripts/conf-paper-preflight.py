"""
conf-paper-preflight: validate the assembled conference paper against the HTKH rules
and the advisor-driven content checklist.

Usage:
    python scripts/conf-paper-preflight.py documents/conference-paper/paper-final.md

Checks:
    - Abstract VI length in [150, 200] words
    - Abstract EN length in [150, 200] words
    - Total EN body (sections 1-5) reasonable (2500-3800 words)
    - References count <= 15
    - Every inline citation has a matching reference entry (no orphans)
    - Every reference entry is cited at least once (no unused references)
    - No forbidden patterns: "figure above", "table below", "hình trên", "bảng dưới"
    - Every Figure X / Table Y reference has a placeholder in the assembled file
"""
import argparse
import io
import re
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


def extract_tagged_block(text, tag):
    m = re.search(rf"<!-- {tag}_BEGIN -->(.*?)<!-- {tag}_END -->", text, re.S)
    return m.group(1).strip() if m else None


def word_count(text):
    if not text:
        return 0
    # Strip the bold label like "**Tóm tắt:**" or "**Abstract:**" whether the colon
    # is inside the ** (our convention) or outside.
    stripped = re.sub(r"\*\*[^*]+?\*\*:?", "", text).strip()
    return len(re.findall(r"\S+", stripped))


def _strip_possessive(s):
    return re.sub(r"[‘’']s$", "", s)


def extract_citations(text):
    """Return set of (first-author-surname, year) keys used inline.

    Matches both parenthetical `(Author, Year)` and narrative `Author (Year)` styles.
    Handles chained parenthetical citations separated by `;`.
    """
    keys = set()
    pat_paren_block = re.compile(r"\(([^()]{4,}?(?:19|20)\d{2}[a-z]?)\)")
    cite_in_paren = re.compile(r"([^;]+?),\s*((?:19|20)\d{2}[a-z]?)")
    pat_narr = re.compile(
        r"\b([A-Z][A-Za-z\-']+?)(?:[‘’']s)?"
        r"(?:\s+(?:and|&)\s+[A-Z][A-Za-z\-']+(?:[‘’']s)?|\s+et\s+al\.)?"
        r"\s+\(((?:19|20)\d{2}[a-z]?)\)"
    )
    for m in pat_paren_block.finditer(text):
        block = m.group(1)
        for sub in re.split(r";\s*", block):
            cm = cite_in_paren.match(sub.strip())
            if not cm:
                continue
            author_part = cm.group(1).strip()
            year = cm.group(2)
            first_token = re.split(r"\s+(?:and|&)\s+|,\s*|\s+et\s+al", author_part)[0].strip()
            surname = _strip_possessive(first_token)
            if surname and surname[0].isupper():
                keys.add((surname.lower(), year))
    for m in pat_narr.finditer(text):
        surname = _strip_possessive(m.group(1))
        year = m.group(2)
        keys.add((surname.lower(), year))
    return keys


def extract_reference_keys(refs_text):
    """Return set of (first-author-surname, year) keys from references list."""
    keys = set()
    for line in refs_text.splitlines():
        line = line.strip()
        m = re.match(r"^\d+\.\s+([^()]+?)\((\d{4}[a-z]?)\)", line)
        if not m:
            continue
        authors_raw = m.group(1).strip().rstrip(",").strip()
        year = m.group(2)
        first_surname = authors_raw.split(",")[0].strip()
        if first_surname:
            keys.add((first_surname.lower(), year))
    return keys


def count_references(refs_text):
    return len(re.findall(r"^\s*\d+\.\s+", refs_text, re.M))


def check_forbidden_patterns(text):
    forbidden = ["figure above", "table below", "hình trên", "bảng dưới", "figure below", "table above"]
    hits = []
    for pat in forbidden:
        for m in re.finditer(re.escape(pat), text, re.I):
            line_start = text.rfind("\n", 0, m.start()) + 1
            line_end = text.find("\n", m.end())
            line = text[line_start:line_end].strip()
            hits.append((pat, line[:120]))
    return hits


def check_figure_placeholders(body):
    refs = set(re.findall(r"\bFigure\s+(\d+)\b", body))
    phs = set(re.findall(r"\[FIGURE_(\d+)_HERE\]", body))
    missing_ph = refs - phs
    unused_ph = phs - refs
    return refs, phs, missing_ph, unused_ph


def check_table_placeholders(body):
    refs = set(re.findall(r"\bTable\s+(\d+)\b", body))
    phs = set(re.findall(r"\[TABLE_(\d+)_HERE\]", body))
    missing_ph = refs - phs
    unused_ph = phs - refs
    return refs, phs, missing_ph, unused_ph


def report(label, ok, detail=""):
    mark = "PASS" if ok else "FAIL"
    print(f"  [{mark}] {label}" + (f" — {detail}" if detail else ""))
    return ok


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("file", help="Assembled paper markdown file")
    args = ap.parse_args()

    text = Path(args.file).read_text(encoding="utf-8")

    all_pass = True

    print("=" * 60)
    print(f"Conference Paper Preflight — {args.file}")
    print("=" * 60)

    abs_vi = extract_tagged_block(text, "ABSTRACT_VI")
    abs_en = extract_tagged_block(text, "ABSTRACT_EN")
    kw_vi = extract_tagged_block(text, "KEYWORDS_VI")
    kw_en = extract_tagged_block(text, "KEYWORDS_EN")
    title_vi = extract_tagged_block(text, "TITLE_VI")
    title_en = extract_tagged_block(text, "TITLE_EN")
    authors = extract_tagged_block(text, "AUTHORS")

    print("\n[Front matter]")
    all_pass &= report("Title VI present", bool(title_vi))
    all_pass &= report("Title EN present", bool(title_en))
    all_pass &= report("Authors block present", bool(authors))

    wc_abs_vi = word_count(abs_vi)
    wc_abs_en = word_count(abs_en)
    all_pass &= report(f"Abstract VI in [150, 200]", 150 <= wc_abs_vi <= 200, f"{wc_abs_vi} words")
    all_pass &= report(f"Abstract EN in [150, 200]", 150 <= wc_abs_en <= 200, f"{wc_abs_en} words")

    kw_vi_count = len([w for w in re.split(r";", kw_vi or "") if w.strip() and not w.strip().startswith("**")])
    kw_en_count = len([w for w in re.split(r";", kw_en or "") if w.strip() and not w.strip().startswith("**")])
    all_pass &= report(f"Keywords VI count in [3, 5]", 3 <= kw_vi_count <= 5, f"{kw_vi_count} keywords")
    all_pass &= report(f"Keywords EN count in [3, 5]", 3 <= kw_en_count <= 5, f"{kw_en_count} keywords")

    body_match = re.search(r"# 1\.\s*Introduction.*?(?=# References|\Z)", text, re.S)
    body = body_match.group(0) if body_match else ""
    body_clean = re.sub(r"\[FIGURE_\d+_HERE\].*?(?=\n)", "", body)
    body_clean = re.sub(r"\[TABLE_\d+_HERE\].*?(?=\n)", "", body_clean)
    body_clean = re.sub(r"^#.*$", "", body_clean, flags=re.M)
    wc_body = len(re.findall(r"\S+", body_clean))
    print("\n[Body]")
    all_pass &= report(f"Body length in [2500, 3800]", 2500 <= wc_body <= 3800, f"{wc_body} words")

    refs_match = re.search(r"# References(.*)", text, re.S)
    refs_text = refs_match.group(1) if refs_match else ""
    n_refs = count_references(refs_text)
    print("\n[References]")
    all_pass &= report(f"References <= 15", n_refs <= 15, f"{n_refs} entries")
    all_pass &= report(f"References >= 8",   n_refs >= 8,  f"{n_refs} entries")

    cited = extract_citations(body)
    ref_keys = extract_reference_keys(refs_text)
    orphan_cites = cited - ref_keys
    unused_refs = ref_keys - cited
    def keys_to_str(keys):
        return ", ".join(f"{k[0]} {k[1]}" for k in sorted(keys))
    all_pass &= report(
        "Every inline citation has a matching reference",
        not orphan_cites,
        ("orphans: " + keys_to_str(orphan_cites)[:200]) if orphan_cites else "",
    )
    all_pass &= report(
        "Every reference is cited at least once",
        not unused_refs,
        ("unused: " + keys_to_str(unused_refs)[:200]) if unused_refs else "",
    )

    print("\n[Forbidden patterns]")
    hits = check_forbidden_patterns(text)
    all_pass &= report("No 'figure above/below' / 'table above/below' / 'hình trên' / 'bảng dưới'",
                        not hits, f"{len(hits)} hits" if hits else "")
    for pat, line in hits:
        print(f"      - '{pat}' -> '{line}'")

    print("\n[Figure/Table placeholders]")
    fig_refs, fig_phs, fig_miss, fig_unused = check_figure_placeholders(text)
    tbl_refs, tbl_phs, tbl_miss, tbl_unused = check_table_placeholders(text)
    all_pass &= report(f"Every 'Figure N' reference has [FIGURE_N_HERE]", not fig_miss, f"missing: {sorted(fig_miss)}" if fig_miss else f"{len(fig_refs)} refs/{len(fig_phs)} placeholders")
    all_pass &= report(f"No unused [FIGURE_N_HERE]", not fig_unused, f"unused: {sorted(fig_unused)}" if fig_unused else "")
    all_pass &= report(f"Every 'Table N' reference has [TABLE_N_HERE]", not tbl_miss, f"missing: {sorted(tbl_miss)}" if tbl_miss else f"{len(tbl_refs)} refs/{len(tbl_phs)} placeholders")
    all_pass &= report(f"No unused [TABLE_N_HERE]", not tbl_unused, f"unused: {sorted(tbl_unused)}" if tbl_unused else "")

    print("\n" + "=" * 60)
    print("RESULT: " + ("ALL PASS" if all_pass else "FAILURES"))
    print("=" * 60)
    sys.exit(0 if all_pass else 1)


if __name__ == "__main__":
    main()
