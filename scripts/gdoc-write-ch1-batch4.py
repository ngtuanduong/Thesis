"""
gdoc-write-ch1-batch4: Batch 4 language cleanup.

PART A: global find-and-replace pairs (marketing/phrase retones).
PART B: delete redundant Ch.1 paragraphs (D1-D5) if anchors match exactly.
PART C: delete Ch.2 duplicate paragraphs if true duplicates found; else flag.

Re-fetches doc between parts. References section is avoided for PART A by
using replaceAllText but scoped via pre-check; since replaceAllText has no
range parameter, we instead pre-verify that none of the BEFORE phrases occur
inside the References range and skip any pair whose matches land in refs.
"""
import importlib.util
import io
import json
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

spec = importlib.util.spec_from_file_location(
    "gdoc_util_auth",
    "C:/Users/duong/WebstormProjects/Thesis/scripts/gdoc-util-auth.py",
)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

service = m.get_docs_service()
DOC_ID = m.DOC_ID

REF_START_IDX = 209787  # paragraph doc-index where References heading begins


def fetch_doc():
    return service.documents().get(documentId=DOC_ID).execute()


def build_full_text(doc):
    """Concatenate all paragraph text, return (full_text, idx_map).

    idx_map: list of (char_start, char_end, para_doc_start, para_doc_end, style)
    """
    full = ""
    idx_map = []
    for elem in doc["body"]["content"]:
        if "paragraph" not in elem:
            continue
        para = elem["paragraph"]
        text = ""
        for el in para.get("elements", []):
            if "textRun" in el:
                text += el["textRun"]["content"]
        style = para.get("paragraphStyle", {}).get("namedStyleType", "NORMAL_TEXT")
        s0 = len(full)
        full += text
        idx_map.append((s0, len(full), elem["startIndex"], elem["endIndex"], style))
    return full, idx_map


def char_to_doc(idx_map, cpos):
    for (s0, e0, ps, pe, st) in idx_map:
        if s0 <= cpos < e0:
            return ps + (cpos - s0)
    return None


def count_body_hits(full, idx_map, needle):
    """Return list of (char_pos, doc_idx) where needle appears and doc_idx < REF_START_IDX."""
    out = []
    i = 0
    while True:
        j = full.find(needle, i)
        if j < 0:
            break
        di = char_to_doc(idx_map, j)
        if di is not None and di < REF_START_IDX:
            out.append((j, di))
        i = j + 1
    return out


# =============================================================================
# PART A
# =============================================================================

# Ordered list: (pair_id, before, after)
# Ordering matters within overlapping pairs:
#   - #23 "approximately 30 topics" must run BEFORE #24 "30 topics"
#   - #22 "knowledge graph of 28" should run BEFORE #20 "28 concepts" so that
#     the overlapping occurrence at 185612/185631 is consumed as a unit.
PAIRS = [
    (1, "first integrated multi-layer adaptive architecture combining BKT, Elo, MAB, and FSRS for programming education",
        "integrated multi-layer adaptive architecture that combines BKT, Elo, MAB, and FSRS for programming education"),
    (2, "the first integrated", "an integrated"),
    (3, "fully unified", "integrated"),
    (4, "a novel contribution", "a contribution of this thesis"),
    (5, "novel contribution", "contribution of this thesis"),
    (6, "addresses the gap", "addresses this integration question"),
    (7, "addresses this integration gap", "addresses this integration question"),
    (8, "To the best of our knowledge, this thesis is the first to apply the FSRS algorithm to programming concept review scheduling.",
        "Within the scope of the programming education literature surveyed in Chapter 2, this thesis appears to be among the first to apply the FSRS algorithm to programming concept review scheduling."),
    (9, "To the best of our knowledge, this is the first application of the FSRS algorithm [12] to programming skill retention, constituting the third key contribution of this thesis.",
        "Within the scope of the literature surveyed in Chapter 2, this appears to be among the first applications of the FSRS algorithm [12] to programming skill retention, and is described here as a secondary contribution of the thesis."),
    (10, "produces emergent adaptive behavior that no single technique achieves alone",
         "exhibits adaptive behaviour that combines signals from multiple techniques"),
    (11, "will demonstrate significantly higher", "will show higher"),
    (12, "comprehensive whole-system demonstration of the adaptive system",
         "whole-system description of the adaptive platform"),
    (13, "for the first time in the programming education domain",
         "as an early application in the programming education domain"),
    (14, "a novel rating mapping", "a rating mapping"),
    (15, "the research gap this thesis targets lies precisely at their intersection --- bringing the adaptive sophistication of the latter category into the programming education domain.",
         "the question this thesis investigates sits at their intersection: how to bring the adaptive mechanisms of the latter category into the programming education domain of the former."),
    (16, "the research gap this thesis targets lies precisely at their intersection - bringing the adaptive sophistication of the latter category into the programming education domain.",
         "the question this thesis investigates sits at their intersection: how to bring the adaptive mechanisms of the latter category into the programming education domain of the former."),
    (17, "This row represents a proposed system, not yet deployed and validated at scale. All other rows represent production systems.",
         "This row describes the platform proposed in this thesis. At the time of writing it has been implemented but not yet evaluated in a classroom pilot. All other rows describe production systems."),
    (18, "A controlled pilot experiment with 40--60 participants over a 4-week intervention period, with a follow-up retention test at Week 8. A formal power analysis (detailed in Chapter 5) indicates that this sample size is sufficient to detect large effect sizes (Cohen's d >= 0.8) at alpha = 0.05 with 80% power; the study is therefore framed as a preliminary assessment rather than a definitive large-scale validation.",
         "A pilot evaluation protocol is specified for a between-subjects study with 40-60 participants, a four-week intervention, and a two-week retention follow-up. A power analysis (Chapter 5) indicates that the nominal sample size can only detect large effect sizes (Cohen's d >= 0.8) at alpha = 0.05 with 80% power. Execution of the intervention and reporting of results are beyond the scope of this thesis; the study is presented as a preliminary design rather than a completed evaluation."),
    (19, "A controlled pilot experiment with 40-60 participants over a 4-week intervention period, with a follow-up retention test at Week 8. A formal power analysis (detailed in Chapter 5) indicates that this sample size is sufficient to detect large effect sizes (Cohen's d >= 0.8) at alpha = 0.05 with 80% power; the study is therefore framed as a preliminary assessment rather than a definitive large-scale validation.",
         "A pilot evaluation protocol is specified for a between-subjects study with 40-60 participants, a four-week intervention, and a two-week retention follow-up. A power analysis (Chapter 5) indicates that the nominal sample size can only detect large effect sizes (Cohen's d >= 0.8) at alpha = 0.05 with 80% power. Execution of the intervention and reporting of results are beyond the scope of this thesis; the study is presented as a preliminary design rather than a completed evaluation."),
    # Concept count normalisation, ordered to respect overlaps:
    (23, "approximately 30 topics", "approximately 30 programming concepts"),
    (22, "knowledge graph of 28", "knowledge graph of approximately 30"),
    (21, "28 programming concepts", "approximately 30 programming concepts"),
    (20, "28 concepts", "approximately 30 programming concepts"),
    (24, "30 topics", "approximately 30 programming concepts"),
]

# Sort pairs for reporting by original id
def run_part_a():
    print("\n=== PART A: global replacements ===")
    report = {}
    doc = fetch_doc()
    full, idx_map = build_full_text(doc)

    # Pre-scan: count body hits for each pair (before any changes)
    for pid, before, after in PAIRS:
        hits = count_body_hits(full, idx_map, before)
        # Also warn if any match lies in References:
        i = 0
        ref_hits = 0
        while True:
            j = full.find(before, i)
            if j < 0: break
            di = char_to_doc(idx_map, j)
            if di is not None and di >= REF_START_IDX:
                ref_hits += 1
            i = j + 1
        report[pid] = {"before": before, "pre_count": len(hits), "ref_count": ref_hits}
        print(f"  pair #{pid}: body_hits={len(hits)} ref_hits={ref_hits}")

    # Build replaceAllText requests in a strict order (pairs with overlap first).
    # Bundle ~10 per batchUpdate.
    ordered_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
                   23, 22, 21, 20, 24]
    id_to_pair = {p[0]: p for p in PAIRS}

    # Skip any pair whose only matches are in References. We already know from
    # scan that ref_hits are 0 in all cases (References uses different text).
    requests_all = []
    for pid in ordered_ids:
        p = id_to_pair[pid]
        before, after = p[1], p[2]
        if report[pid]["pre_count"] == 0:
            continue  # nothing to do; replaceAllText still safe but skip to reduce noise
        if report[pid]["ref_count"] > 0:
            print(f"  WARNING: pair #{pid} has {report[pid]['ref_count']} hits in References; skipping to avoid mutating bibliography.")
            continue
        requests_all.append((pid, {
            "replaceAllText": {
                "containsText": {"text": before, "matchCase": True},
                "replaceText": after,
            }
        }))

    # Send in chunks of 10
    CHUNK = 10
    applied_counts = {}
    for i in range(0, len(requests_all), CHUNK):
        chunk = requests_all[i:i + CHUNK]
        pid_list = [c[0] for c in chunk]
        req_list = [c[1] for c in chunk]
        print(f"  sending batch: pair ids {pid_list}")
        resp = service.documents().batchUpdate(
            documentId=DOC_ID, body={"requests": req_list}
        ).execute()
        replies = resp.get("replies", [])
        for pid, reply in zip(pid_list, replies):
            occ = reply.get("replaceAllText", {}).get("occurrencesChanged", 0)
            applied_counts[pid] = applied_counts.get(pid, 0) + occ

    # Fill zeros for pairs we did not send
    for pid, _, _ in PAIRS:
        applied_counts.setdefault(pid, 0)

    # Report
    for pid, before, after in PAIRS:
        report[pid]["applied"] = applied_counts[pid]
    return report


# =============================================================================
# PART B: Chapter 1 deletions (D1-D5). Exact-anchor match as specified.
# =============================================================================

D_ANCHORS = [
    ("D1", "This heterogeneity creates a fundamental tension in traditional lecture-based instruction."),
    ("D2", "Within the Vietnamese university context specifically, these challenges are no less pressing."),
    ("D3", "Research spanning several decades has validated this premise."),
    ("D4", "Academic research, similarly, has tended to study these adaptive components in isolation."),
    ("D5", "In summary, the core problem this thesis addresses is the mismatch"),
]


def run_part_b():
    print("\n=== PART B: Chapter 1 paragraph deletions ===")
    report = {}
    doc = fetch_doc()
    # Per-paragraph scan: delete paragraph whose text starts with anchor.
    # Collect ranges then issue deleteContentRange bottom-up in one batch.
    paras = list(m.iter_paragraphs(doc))
    hits = []
    for tag, anchor in D_ANCHORS:
        matched = None
        for s, e, t, st in paras:
            if t.startswith(anchor):
                matched = (s, e, t)
                break
        if matched:
            hits.append((tag, matched))
            report[tag] = {"status": "APPLIED", "range": (matched[0], matched[1]), "text": matched[2][:120]}
        else:
            report[tag] = {"status": "NOT FOUND"}

    # Apply bottom-up
    hits_sorted = sorted(hits, key=lambda x: x[1][0], reverse=True)
    if hits_sorted:
        requests = []
        for tag, (s, e, t) in hits_sorted:
            requests.append({
                "deleteContentRange": {"range": {"startIndex": s, "endIndex": e}}
            })
        resp = service.documents().batchUpdate(
            documentId=DOC_ID, body={"requests": requests}
        ).execute()
        print(f"  deleted {len(requests)} Ch.1 paragraphs")
    else:
        print("  no Ch.1 paragraph anchors matched exactly")
    return report


# =============================================================================
# PART C: Chapter 2 duplicate hunt (report only unless true duplicate)
# =============================================================================

def run_part_c():
    print("\n=== PART C: Chapter 2 duplicate scan ===")
    doc = fetch_doc()
    paras = list(m.iter_paragraphs(doc))
    CH2_S, CH2_E = 31143, 79210  # approximate; will update from headings

    # Find real Ch2/Ch3 heading indices dynamically
    ch2_s = ch3_s = None
    for s, e, t, st in paras:
        if st.startswith("HEADING") and t.strip().startswith("Chapter 2:"):
            ch2_s = s
        if st.startswith("HEADING") and (t.strip().startswith("Chapter 3:") or t.strip().startswith("CHAPTER 3")):
            ch3_s = s
            break
    if ch2_s is None or ch3_s is None:
        print("  WARNING: failed to locate Ch2/Ch3 headings; using heuristic bounds")
        ch2_s, ch3_s = CH2_S, CH2_E
    print(f"  Ch2 range in doc indices: [{ch2_s}, {ch3_s})")

    # Failure-rate duplicates
    failure_paras = []
    for s, e, t, st in paras:
        if not (ch2_s <= s < ch3_s):
            continue
        lt = t.lower()
        if ("30-40%" in lt or "30\x96" in lt or "30 to 40" in lt) and "fail" in lt:
            failure_paras.append((s, e, t))
        elif "introductory programming" in lt and "high failure" in lt:
            failure_paras.append((s, e, t))
    print(f"  Ch2 'failure rate' paragraphs: {len(failure_paras)}")
    for p in failure_paras:
        print("    ", p[0], repr(p[2][:120]))

    # LeetCode/HackerRank/Codeforces paragraphs
    leet_paras = []
    for s, e, t, st in paras:
        if not (ch2_s <= s < ch3_s):
            continue
        lt = t.lower()
        if "static difficulty" in lt or ("leetcode" in lt and "hackerrank" in lt and "codeforces" in lt):
            leet_paras.append((s, e, t, st))
    print(f"  Ch2 LeetCode/HackerRank/Codeforces paragraphs: {len(leet_paras)}")
    for p in leet_paras:
        print("    ", p[0], p[3], repr(p[2][:140]))

    # Only act on true duplicates (same opening sentence repeated).
    # Our scan shows no true duplicate — flag all for manual review.
    flagged = []
    deleted = []
    if len(failure_paras) > 1:
        first = failure_paras[0]
        # Check semantic near-dup by comparing first ~80 chars
        anchor = first[2][:80]
        dupes = [p for p in failure_paras[1:] if p[2][:80] == anchor]
        if dupes:
            requests = [{"deleteContentRange": {"range": {"startIndex": p[0], "endIndex": p[1]}}} for p in sorted(dupes, key=lambda x: x[0], reverse=True)]
            service.documents().batchUpdate(documentId=DOC_ID, body={"requests": requests}).execute()
            deleted.extend((p[0], p[2][:120]) for p in dupes)
        else:
            flagged.extend((p[0], p[2][:120]) for p in failure_paras)
    elif failure_paras:
        # single, nothing to dedupe
        pass

    if len(leet_paras) > 1:
        # keep first, but only delete true semantic duplicates; otherwise flag.
        first = leet_paras[0]
        anchor = first[2][:80]
        for p in leet_paras[1:]:
            if p[2][:80] == anchor:
                # true duplicate — safe to delete
                service.documents().batchUpdate(
                    documentId=DOC_ID,
                    body={"requests": [{"deleteContentRange": {"range": {"startIndex": p[0], "endIndex": p[1]}}}]},
                ).execute()
                deleted.append((p[0], p[2][:120]))
            else:
                flagged.append((p[0], p[2][:120]))

    return {"deleted": deleted, "flagged": flagged}


# =============================================================================
# Orchestrate
# =============================================================================

report_a = run_part_a()
report_b = run_part_b()
report_c = run_part_c()

# =============================================================================
# Final report
# =============================================================================
print("\n" + "=" * 70)
print("BATCH 4 REPORT")
print("=" * 70)

print("\nPART A:")
for pid, before, after in PAIRS:
    info = report_a.get(pid, {})
    applied = info.get("applied", 0)
    pre = info.get("pre_count", 0)
    tag = "" if applied > 0 else ("NOT FOUND" if pre == 0 else "ERROR")
    print(f"  #{pid:>2}: applied={applied}  pre_scan_body_hits={pre}  {tag}".rstrip())

print("\nPART B:")
for tag, _ in D_ANCHORS:
    info = report_b.get(tag, {})
    st = info.get("status", "??")
    if st == "APPLIED":
        print(f"  {tag}: APPLIED  range={info['range']}  text={info['text']!r}")
    else:
        print(f"  {tag}: NOT FOUND")

print("\nPART C:")
print(f"  DELETED: {len(report_c['deleted'])}")
for s, t in report_c["deleted"]:
    print(f"    at {s}: {t!r}")
print(f"  FLAGGED for manual review: {len(report_c['flagged'])}")
for s, t in report_c["flagged"]:
    print(f"    at {s}: {t!r}")

# Determine final status
partial = False
for pid, before, after in PAIRS:
    info = report_a.get(pid, {})
    if info.get("pre_count", 0) > 0 and info.get("applied", 0) == 0:
        partial = True
        break

print()
print("Batch 4 DONE" if not partial else "Batch 4 PARTIAL")
