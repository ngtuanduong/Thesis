"""
gdoc-write-conf-fix-relevance: Restore the "Relevance to this work:" marker at
§2.5 so the 3-of-5 distribution (§2.1, §2.3, §2.5) required by the plan holds.
The earlier trim3 pass dropped it. Replace the current §2.5 closing sentence
with the plan-intended wording, which still keeps the §2 body comfortably
inside the 450-480 word target.

Usage:
    GDOC_KEY_FILE=... GDOC_DOC_ID=... python3 scripts/gdoc-write-conf-fix-relevance.py
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
    (
        "This gap is the paper's core motivation, and Table 1 summarizes the four techniques' complementary roles.",
        "Relevance to this work: this gap is the paper's core motivation, and Table 1 summarizes the four techniques' complementary roles.",
        "Relevance to this work: this gap is the paper's core motivation",
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
    for i, reply in enumerate(result.get("replies", [])):
        occ = reply.get("replaceAllText", {}).get("occurrencesChanged", 0)
        print(f"[{i}] occurrencesChanged={occ} find={REPLACEMENTS[i][0][:70]!r}...")

    doc = mod.get_document(service=service, doc_id=DOC_ID)
    joined = "\n".join(text for _s, _e, text, _st in mod.iter_paragraphs(doc))
    missing = [c for _f, _r, c in REPLACEMENTS if c not in joined]
    if missing:
        print(f"FAIL: missing canaries: {missing}")
    else:
        print(f"OK: {len(REPLACEMENTS)} canaries present.")


if __name__ == "__main__":
    main()
