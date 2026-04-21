"""Find anchors needed for Batch 2: Abstract block and end-of-Chapter-5 insertion point."""
import importlib.util
import io
import sys

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

print(f"Total paragraphs: {len(paras)}")
print()
print("=== Paragraphs containing 'Abstract' or 'Keyword' or 'bstract' ===")
for i, (s, e, t, st) in enumerate(paras):
    tl = t.strip()
    if "bstract" in tl or tl.lower().startswith("keyword") or "Keyword" in tl:
        print(f"[{i}] s={s} e={e} style={st}")
        print(f"    text={tl[:200]!r}")

print()
print("=== Paragraphs matching headings 5.x, 6 CONCLUSION, REFERENCES ===")
for i, (s, e, t, st) in enumerate(paras):
    tl = t.strip()
    if st.startswith("HEADING") or tl.upper().startswith("CHAPTER") or tl.upper().startswith("REFERENCES") or tl.startswith("5.") or tl.upper().startswith("BIBLIOGRAPHY"):
        print(f"[{i}] s={s} e={e} style={st}")
        print(f"    text={tl[:160]!r}")

print()
print("=== First 40 paragraphs (front matter) ===")
for i, (s, e, t, st) in enumerate(paras[:40]):
    tl = t.strip()
    print(f"[{i}] s={s} e={e} style={st} text={tl[:120]!r}")
