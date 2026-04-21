"""
gdoc-read-full: dump the entire Google Doc as JSONL, one paragraph per line.

Usage:
    python scripts/gdoc-read-full.py > /tmp/doc.jsonl
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

doc = m.get_document()
for start, end, text, style in m.iter_paragraphs(doc):
    print(json.dumps({"s": start, "e": end, "style": style, "text": text}, ensure_ascii=False))
