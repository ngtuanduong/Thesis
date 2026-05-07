"""
gdoc-find-conf-anchors: Inspect structure of the conference-paper Google Doc.
Dumps, for each paragraph:
  - startIndex, endIndex
  - paragraph style (named style type)
  - textRun-level formatting: bold / italic / foregroundColor, with indices
so we know what replacements will preserve style, and what needs explicit
updateTextStyle requests.

Usage:
    GDOC_KEY_FILE=... GDOC_DOC_ID=... OUT_PATH=... python3 scripts/gdoc-find-conf-anchors.py
"""
import io
import os
import sys
import importlib.util
import json

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
for elem in doc["body"]["content"]:
    if "paragraph" not in elem:
        if "table" in elem:
            lines.append(f"[TABLE] start={elem['startIndex']} end={elem['endIndex']}")
        continue
    para = elem["paragraph"]
    style = para.get("paragraphStyle", {}).get("namedStyleType", "NORMAL_TEXT")
    s, e = elem["startIndex"], elem["endIndex"]
    full = ""
    runs = []
    for el in para.get("elements", []):
        if "textRun" in el:
            tr = el["textRun"]
            text = tr["content"]
            ts = tr.get("textStyle", {}) or {}
            flags = []
            if ts.get("bold"): flags.append("B")
            if ts.get("italic"): flags.append("I")
            if ts.get("underline"): flags.append("U")
            if ts.get("strikethrough"): flags.append("S")
            if ts.get("baselineOffset") == "SUBSCRIPT": flags.append("sub")
            if ts.get("baselineOffset") == "SUPERSCRIPT": flags.append("sup")
            flagstr = "".join(flags) or "-"
            runs.append((el["startIndex"], el["endIndex"], flagstr, text))
            full += text
    short = full.rstrip("\n")
    if len(short) > 120:
        short = short[:117] + "..."
    lines.append(f"[{style:20}] {s:6}-{e:6} | {short!r}")
    for rs, re_, fl, tx in runs:
        if fl != "-":
            shorttx = tx.replace("\n", "\\n")
            if len(shorttx) > 80:
                shorttx = shorttx[:77] + "..."
            lines.append(f"    run {rs}-{re_} [{fl}] {shorttx!r}")

out_path = os.environ.get("OUT_PATH")
text = "\n".join(lines) + "\n"
if out_path:
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Wrote anchors dump to {out_path}")
else:
    print(text)
