"""Inspect paragraphs at tail of Chapter 5 (between 5.3 end and References)."""
import importlib.util, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
spec = importlib.util.spec_from_file_location("gdoc_util_auth","C:/Users/duong/WebstormProjects/Thesis/scripts/gdoc-util-auth.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
service = m.get_docs_service()
doc = service.documents().get(documentId=m.DOC_ID).execute()
paras = list(m.iter_paragraphs(doc))
for i,(s,e,t,st) in enumerate(paras):
    if 1090 <= i <= 1105:
        print(f"[{i}] s={s} e={e} style={st}")
        print(f"    text={t[:300]!r}")
