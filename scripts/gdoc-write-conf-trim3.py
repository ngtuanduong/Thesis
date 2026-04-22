"""
gdoc-write-conf-trim3: Final fine-grained trim of §2 Related Work to land
inside 450-480 words. After trim2, §2 body sits at 483 words (incl. caption
497). We need to shave ~5-15 more words to settle inside 450-480 body.

Usage:
    GDOC_KEY_FILE=... GDOC_DOC_ID=... python3 scripts/gdoc-write-conf-trim3.py
"""
import io
import os
import sys
import importlib.util

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location(
    "gdoc_util_auth", os.path.join(HERE, "gdoc-util-auth.py")
)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

service = mod.get_docs_service()
DOC_ID = os.environ.get("GDOC_DOC_ID") or mod.DOC_ID


REPLACEMENTS = [
    # §2 intro — drop the "and positions the platform…" tail which is a minor
    # duplicate of the gap-statement at §2.5.
    (
        "This section reviews the four adaptive techniques that the proposed platform integrates and positions the platform with respect to prior programming-education systems.",
        "This section reviews the four adaptive techniques that the proposed platform integrates.",
        "This section reviews the four adaptive techniques that the proposed platform integrates.",
    ),

    # §2.5 — drop the "Research prototypes have examined individual adaptive
    # components in programming education, but" lead-in; go straight to the gap.
    (
        "Research prototypes have examined individual adaptive components in programming education, but the literature surveyed in this paper does not report a system that simultaneously integrates knowledge tracing, dynamic difficulty calibration, bandit-based selection, and spaced repetition under a shared knowledge graph.",
        "The literature surveyed in this paper does not report a system that simultaneously integrates knowledge tracing, dynamic difficulty calibration, bandit-based selection, and spaced repetition under a shared knowledge graph for programming education.",
        "The literature surveyed in this paper does not report a system that simultaneously integrates knowledge tracing, dynamic difficulty calibration, bandit-based selection, and spaced repetition under a shared knowledge graph for programming education.",
    ),
]


def main():
    requests = [{
        "replaceAllText": {
            "containsText": {"text": f, "matchCase": True},
            "replaceText": r,
        }
    } for f, r, _c in REPLACEMENTS]
    result = service.documents().batchUpdate(
        documentId=DOC_ID,
        body={"requests": requests},
    ).execute()
    zero = []
    for i, reply in enumerate(result.get("replies", [])):
        occ = reply.get("replaceAllText", {}).get("occurrencesChanged", 0)
        print(f"[{i}] occurrencesChanged={occ} find={REPLACEMENTS[i][0][:70]!r}...")
        if occ == 0:
            zero.append(i)
    if zero:
        print(f"WARNING: {len(zero)} requests missed. Indices: {zero}")

    doc = mod.get_document(service=service, doc_id=DOC_ID)
    joined = "\n".join(text for _s, _e, text, _st in mod.iter_paragraphs(doc))
    missing = [c for _f, _r, c in REPLACEMENTS if c not in joined]
    if missing:
        print(f"FAIL: missing canaries: {missing}")
    else:
        print(f"OK: all {len(REPLACEMENTS)} canaries present.")


if __name__ == "__main__":
    main()
