"""Dump full abstract paragraph text for T6 anchoring."""
import importlib.util, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
spec = importlib.util.spec_from_file_location("gdoc_util_auth","C:/Users/duong/WebstormProjects/Thesis/scripts/gdoc-util-auth.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
doc = m.get_document()
paras = list(m.iter_paragraphs(doc))
for i,(s,e,t,st) in enumerate(paras):
    if 24 <= i <= 36:
        print(f"[{i}] s={s} e={e} style={st}")
        print(f"    FULL={t!r}")
        print()
