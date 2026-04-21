"""Extract fenced code blocks from thesis markdown and save as JSON."""
import re
import json
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

MD_DIR = "C:/Users/duong/WebstormProjects/Thesis/documents/thesis-chapters"
OUT = "C:/tmp/equations/code_blocks.json"

all_blocks = []

for fname, ch in [("chapter4-implementation.md", 4)]:
    with open(f"{MD_DIR}/{fname}", "r", encoding="utf-8") as f:
        content = f.read()

    pattern = re.compile(r"```(\w*)\n(.*?)```", re.DOTALL)
    for m in pattern.finditer(content):
        lang = m.group(1) or "text"
        code = m.group(2).rstrip("\n")
        first_line = code.split("\n")[0].strip()[:80]
        n_lines = len(code.split("\n"))
        all_blocks.append({
            "chapter": ch,
            "lang": lang,
            "code": code,
            "lines": n_lines,
            "first_line": first_line,
        })

print(f"Found {len(all_blocks)} fenced code blocks:")
for i, b in enumerate(all_blocks):
    print(f"  [{i+1}] {b['lang']:8s} {b['lines']:3d} lines | {b['first_line']}")

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(all_blocks, f, indent=2, ensure_ascii=False)
print(f"\nSaved to {OUT}")
