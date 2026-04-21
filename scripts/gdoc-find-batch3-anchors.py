"""Inspect body text in Sections 1.3, 1.4, 1.7 to confirm anchors."""
import importlib.util, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

spec = importlib.util.spec_from_file_location(
    "gdoc_util_auth",
    "C:/Users/duong/WebstormProjects/Thesis/scripts/gdoc-util-auth.py",
)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

service = m.get_docs_service()
doc = service.documents().get(documentId=m.DOC_ID).execute()
paras = list(m.iter_paragraphs(doc))

def show_range(lo, hi, label):
    print(f"\n=== {label} : [{lo},{hi}) ===")
    for s, e, t, st in paras:
        if s >= lo and s < hi:
            bullet = ""
            # Find if paragraph has bullet
            for elem in doc["body"]["content"]:
                if "paragraph" in elem and elem["startIndex"] == s:
                    if elem["paragraph"].get("bullet"):
                        bullet = "[BULLET]"
                    break
            print(f"[{s:>6}-{e:>6}] {st[:12]:12} {bullet} | {t.strip()[:130]}")

# 1.3: 13704 -> 16856
show_range(13704, 16856, "Section 1.3 Research Objectives")
# 1.4: 16856 -> 19939
show_range(16856, 19939, "Section 1.4 Research Questions")
# 1.7: 27126 -> 30106
show_range(27126, 30106, "Section 1.7 Contributions")
