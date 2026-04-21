"""
gdoc-write-ch5-batch2: apply Batch 2 (T3 insert §5.5, T6 rewrite Abstract).

Pre-reads the live doc to locate insertion indices, then performs a single
batchUpdate:
 - T6: deleteContentRange(abstract_start, abstract_end) + insertText(abstract_start, new_abstract)
        + updateParagraphStyle(NORMAL_TEXT) for the three new paragraphs to match body style.
 - T3: insertText(before_references_index, new_section_5_5)
        + updateParagraphStyle HEADING_2 for '5.5 Threats to Validity'
        + updateTextStyle (bold) for each lead-in label.

Because T3's insertion index is later in the doc than T6's edit, we must apply
T3 BEFORE T6 (since T6 changes all indices after 505). Actually the abstract
edit is at 505 and §5.5 is at 210117, so T6 shifts indices. We therefore run
T3 first (it doesn't affect the abstract indices), then T6.
"""
import importlib.util, io, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

spec = importlib.util.spec_from_file_location(
    "gdoc_util_auth",
    "C:/Users/duong/WebstormProjects/Thesis/scripts/gdoc-util-auth.py",
)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

service = m.get_docs_service()
DOC_ID = m.DOC_ID


def fetch_doc():
    return service.documents().get(documentId=DOC_ID).execute()


def iter_paras(doc):
    return list(m.iter_paragraphs(doc))


# =============================================================================
# Content
# =============================================================================

SEC55_HEADING = "5.5 Threats to Validity"

SEC55_INTRO = (
    "Several characteristics of the proposed pilot limit the strength of the "
    "conclusions that can be drawn from it. They are stated explicitly so that "
    "readers can calibrate the weight given to any future results."
)

SEC55_PARAS = [
    (
        "Small and single-site sample.",
        " Recruitment is confined to a single cohort at Hanoi University, with a "
        "target of 40-60 participants and a fallback plan for as few as 20-30. "
        "With approximately 20-30 students per condition in the nominal case, the "
        "study is only powered to detect large effect sizes (Cohen's d >= 0.8). "
        "Generalization to other institutions, curricula, or student populations "
        "is therefore not supported by the data that this pilot can produce.",
    ),
    (
        "Short intervention window.",
        " The four-week intervention, together with a two-week gap before the "
        "retention test, is short relative to the full forgetting curves that the "
        "FSRS algorithm is designed to exploit. Results on RQ3 should therefore "
        "be read as suggestive of short-term retention differences rather than as "
        "a validation of long-term spaced repetition benefits in programming.",
    ),
    (
        "Confounded treatment condition.",
        " The experimental group receives Layers 1-4 of the adaptive pipeline "
        "simultaneously (BKT, Dynamic Elo, Hierarchical MAB, and FSRS), while the "
        "control group receives none of these components. Any observed difference "
        "between the two groups therefore cannot be attributed to any single "
        "layer - for example, a positive effect on RQ2 cannot be cleanly separated "
        "from the effect of FSRS review scheduling, and vice versa. Within-system "
        "analyses based on feature-flag replay may offer partial triangulation, "
        "but they rely on the same set of interaction logs and cannot replicate a "
        "true ablation experiment. Layer 5 (LLM hints) is disabled in the pilot "
        "and is therefore not a source of confounding.",
    ),
    (
        "Metric-model coupling.",
        " Several of the reported metrics, notably BKT prediction AUC and Elo "
        "convergence speed, are computed using the same model that also drives "
        "the platform's recommendations. A favourable value on these metrics "
        "demonstrates internal consistency of the model but does not, on its own, "
        "constitute independent evidence of learning effectiveness.",
    ),
    (
        "Self-selection, novelty, and attention effects.",
        " Participation is voluntary, and the experimental interface is more "
        "feature-rich than the control interface. Observed differences may partly "
        "reflect novelty, increased perceived attention, or self-selection of "
        "more motivated students into the study rather than the adaptive "
        "mechanisms themselves.",
    ),
    (
        "Assessment instrument.",
        " The pre-test and post-test are parallel-form instruments constructed "
        "for this study and have not been independently validated. Their "
        "reliability and concurrent validity will be reported post hoc, but this "
        "remains a limitation of the pilot.",
    ),
]

SEC55_CLOSING = (
    "Taken together, these threats mean that any findings reported from this "
    "pilot should be interpreted as preliminary evidence about the feasibility "
    "and perceived value of the integrated platform, not as a definitive "
    "comparative evaluation of the individual adaptive techniques."
)

# Abstract replacement
ABSTRACT_P1 = (
    "Programming education in large university courses faces a long-standing "
    "tension between the individualized, practice-intensive nature of programming "
    "skill acquisition and the uniform, resource-constrained reality of classroom "
    "instruction, with introductory failure rates reported at around 30-40% "
    "worldwide. Existing online coding platforms such as LeetCode, HackerRank, "
    "and Codeforces offer extensive problem repositories but use static "
    "difficulty tiers and do not adapt a learning path to the individual student. "
    "Prior academic work on adaptive learning for programming has typically "
    "addressed one component - knowledge tracing, difficulty calibration, "
    "problem recommendation, or spaced repetition - in isolation."
)
ABSTRACT_P2 = (
    "This thesis proposes and implements an Adaptive Learning Platform for "
    "University Programming Courses that combines several of these components "
    "into a single closed-loop system. The platform is built around a manually "
    "curated knowledge graph of approximately 30 Python programming concepts and "
    "five adaptive layers: Bayesian Knowledge Tracing for per-concept mastery "
    "estimation, a Dynamic K-Value Elo rating system for difficulty calibration, "
    "a Hierarchical Multi-Armed Bandit with Thompson Sampling for problem "
    "selection, the Free Spaced Repetition Scheduler (FSRS) for review "
    "scheduling, and an optional Retrieval-Augmented LLM hint module. The system "
    "is delivered as a working full-stack application (React, NestJS, FastAPI, "
    "PostgreSQL, Docker-based code sandbox)."
)
ABSTRACT_P3 = (
    "The platform is accompanied by a pilot evaluation protocol describing a "
    "between-subjects, pre-test / post-test study with 40-60 undergraduate "
    "students at Hanoi University over a four-week intervention and a two-week "
    "retention follow-up, using Normalized Learning Gain, model prediction "
    "accuracy, engagement metrics, SUS, and TAM. At the time of writing, the "
    "intervention has not been executed and no experimental outcomes are "
    "reported. The thesis's primary contributions are therefore (i) the "
    "integrated platform and (ii) the pilot evaluation design. Layer 5 (LLM "
    "hints) is presented as an optional extension."
)


# =============================================================================
# Step 1: locate anchors from live doc
# =============================================================================

print("=== Reading doc to locate anchors ===")
doc = fetch_doc()
paras = iter_paras(doc)

# Abstract: find paragraph starting with "Programming education at universities worldwide"
abstract_start = None
abstract_end = None
for (s, e, t, st) in paras:
    if t.startswith("Programming education at universities worldwide faces a persistent challenge"):
        abstract_start = s
        break
if abstract_start is None:
    print("FAIL: abstract anchor not found")
    sys.exit(1)

# abstract_end = startIndex of the paragraph beginning "Keywords:" minus 1 (the trailing empty para before Keywords)
# Look for Keywords paragraph
keywords_start = None
for (s, e, t, st) in paras:
    if t.startswith("Keywords:"):
        keywords_start = s
        break
if keywords_start is None:
    print("FAIL: Keywords anchor not found")
    sys.exit(1)

# There's an empty separator paragraph between last abstract para and Keywords.
# We want to delete [abstract_start, keywords_start - 1) — leaving one empty separator paragraph intact.
# Paragraph immediately before Keywords: find it
prev_empty_start = None
for i, (s, e, t, st) in enumerate(paras):
    if s == keywords_start:
        prev_empty_start = paras[i - 1][0]
        break
# prev_empty_start is the start of the empty '\n' paragraph before Keywords (index 4283 in recon)
abstract_end = prev_empty_start  # delete up to but not including this empty paragraph
print(f"Abstract delete range: [{abstract_start}, {abstract_end})  (empty sep kept, Keywords at {keywords_start})")

# Chapter 5 end / References start
# The References heading paragraph text starts with "eference:" (a glyph anomaly).
# Find the paragraph whose text begins with 'eference' or 'References' and is HEADING_2, occurring after §5.3 content.
ref_start = None
for (s, e, t, st) in paras:
    if st.startswith("HEADING") and ("eference" in t or t.startswith("References")):
        if s > 200000:  # after Chapter 5 area
            ref_start = s
            break
if ref_start is None:
    print("FAIL: References heading anchor not found")
    sys.exit(1)
print(f"References heading starts at {ref_start}; inserting §5.5 here.")


# =============================================================================
# Step 2: build §5.5 insertion text
# =============================================================================

# Structure text so each paragraph is separated by '\n'.
# Paragraph 1: heading
# Paragraph 2: intro
# Paragraphs 3-8: six bold-lead-in body paragraphs
# Paragraph 9: closing
sec55_text_parts = [SEC55_HEADING, SEC55_INTRO]
for label, rest in SEC55_PARAS:
    sec55_text_parts.append(label + rest)
sec55_text_parts.append(SEC55_CLOSING)

sec55_text = "\n".join(sec55_text_parts) + "\n"

# Compute character offsets (relative to ref_start) for later styling requests.
# In Google Docs insertText, inserted '\n' becomes a paragraph break and each
# paragraph break occupies one index position. So offsets in the document
# correspond exactly to character offsets within sec55_text.
offsets = []
pos = 0
for part in sec55_text_parts:
    offsets.append((pos, pos + len(part)))  # start, end (exclusive) of this paragraph's text
    pos += len(part) + 1  # +1 for the '\n'

heading_off = offsets[0]
intro_off = offsets[1]
para_offs = offsets[2:2 + len(SEC55_PARAS)]
closing_off = offsets[-1]


# =============================================================================
# Step 3: build the ABSTRACT replacement text
# =============================================================================

abstract_text = ABSTRACT_P1 + "\n\n" + ABSTRACT_P2 + "\n\n" + ABSTRACT_P3 + "\n"
# When deleting [abstract_start, abstract_end) we removed the paragraphs 25-33
# AND the final '\n' of paragraph 33 (which ended at abstract_end). So the
# inserted text must end with '\n' to restore a paragraph break before the
# empty-sep paragraph that we kept.


# =============================================================================
# Step 4: issue T3 first (higher index), then T6 (lower index)
# =============================================================================

print("\n=== T3: insert §5.5 before References ===")

t3_requests = []

# 1) insert
t3_requests.append({
    "insertText": {
        "location": {"index": ref_start},
        "text": sec55_text,
    }
})

# 2) style heading paragraph as HEADING_2 (matches 5.1, 5.2, 5.3)
h_s = ref_start + heading_off[0]
h_e = ref_start + heading_off[1] + 1  # +1 to include the paragraph break
t3_requests.append({
    "updateParagraphStyle": {
        "range": {"startIndex": h_s, "endIndex": h_e},
        "paragraphStyle": {"namedStyleType": "HEADING_2"},
        "fields": "namedStyleType",
    }
})

# 3) ensure all body paragraphs after heading are NORMAL_TEXT
body_s = ref_start + intro_off[0]
body_e = ref_start + closing_off[1] + 1
t3_requests.append({
    "updateParagraphStyle": {
        "range": {"startIndex": body_s, "endIndex": body_e},
        "paragraphStyle": {"namedStyleType": "NORMAL_TEXT"},
        "fields": "namedStyleType",
    }
})

# 4) bold each lead-in label
for (label, _rest), (p_s_off, _p_e_off) in zip(SEC55_PARAS, para_offs):
    lbl_s = ref_start + p_s_off
    lbl_e = ref_start + p_s_off + len(label)
    t3_requests.append({
        "updateTextStyle": {
            "range": {"startIndex": lbl_s, "endIndex": lbl_e},
            "textStyle": {"bold": True},
            "fields": "bold",
        }
    })

resp = service.documents().batchUpdate(
    documentId=DOC_ID, body={"requests": t3_requests}
).execute()
print(f"T3 applied: {len(t3_requests)} requests, {len(resp.get('replies', []))} replies")


# =============================================================================
# T6: Abstract replacement (indices unaffected by T3 which was later in doc)
# =============================================================================

print("\n=== T6: rewrite Abstract ===")

t6_requests = [
    {
        "deleteContentRange": {
            "range": {"startIndex": abstract_start, "endIndex": abstract_end}
        }
    },
    {
        "insertText": {
            "location": {"index": abstract_start},
            "text": abstract_text,
        }
    },
    # Style all three new paragraphs as NORMAL_TEXT (defensive).
    {
        "updateParagraphStyle": {
            "range": {
                "startIndex": abstract_start,
                "endIndex": abstract_start + len(abstract_text),
            },
            "paragraphStyle": {"namedStyleType": "NORMAL_TEXT"},
            "fields": "namedStyleType",
        }
    },
    # Clear any inherited bold/italic from prior content (defensive).
    {
        "updateTextStyle": {
            "range": {
                "startIndex": abstract_start,
                "endIndex": abstract_start + len(abstract_text),
            },
            "textStyle": {"bold": False, "italic": False},
            "fields": "bold,italic",
        }
    },
]

resp = service.documents().batchUpdate(
    documentId=DOC_ID, body={"requests": t6_requests}
).execute()
print(f"T6 applied: {len(t6_requests)} requests, {len(resp.get('replies', []))} replies")


# =============================================================================
# Verification
# =============================================================================

print("\n=== Verification ===")
doc2 = fetch_doc()
full_text = []
for elem in doc2["body"]["content"]:
    if "paragraph" in elem:
        for el in elem["paragraph"].get("elements", []):
            if "textRun" in el:
                full_text.append(el["textRun"]["content"])
full = "".join(full_text)

checks = [
    ("T3 heading", "5.5 Threats to Validity"),
    ("T3 intro", "Several characteristics of the proposed pilot limit the strength"),
    ("T3 label 1", "Small and single-site sample."),
    ("T3 label 6", "Assessment instrument."),
    ("T3 closing", "Taken together, these threats mean that any findings reported"),
    ("T6 p1", "Programming education in large university courses faces a long-standing"),
    ("T6 p2", "This thesis proposes and implements an Adaptive Learning Platform"),
    ("T6 p3", "The platform is accompanied by a pilot evaluation protocol"),
    ("T6 OLD gone", "Programming education at universities worldwide faces a persistent challenge"),
]
for label, needle in checks:
    present = needle in full
    if label == "T6 OLD gone":
        status = "OK " if not present else "FAIL (old text still present)"
    else:
        status = "OK " if present else "MISS"
    print(f"  [{label}] {status}  '{needle[:70]}'")

print("\nDONE.")
