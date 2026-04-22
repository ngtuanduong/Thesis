"""
gdoc-read-conf-paper: Export the conference paper Google Doc body to a .txt file,
one paragraph per line, preserving paragraph order.

Uses env var GDOC_DOC_ID (set by caller) to override default doc ID.
Requires GDOC_KEY_FILE env var pointing to the service-account JSON.

Usage:
    GDOC_KEY_FILE=/Users/avada/Downloads/infra-inkwell-465003-f2-369235afe5ac.json \
    GDOC_DOC_ID=1b21l8G9SXiXSYP_2k9Up3ic11OK08yus557vb8gsPhs \
    python3 scripts/gdoc-read-conf-paper.py > /tmp/conf-paper.txt
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
doc = mod.get_document(service=service)

lines = []
for start, end, text, style in mod.iter_paragraphs(doc):
    # iter_paragraphs returns text with trailing newline; strip for export
    stripped = text.rstrip("\n")
    if stripped.strip() == "":
        # preserve blank-paragraph structure but do not write empty lines
        continue
    lines.append(stripped)

out_path = os.environ.get("OUT_PATH")
if out_path:
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"Wrote {len(lines)} paragraphs to {out_path}")
else:
    for line in lines:
        print(line)
