#!/usr/bin/env python3
"""Verify parser fix by running the corrected parse_chapter."""
import re

def parse_chapter():
    with open("C:/Users/duong/WebstormProjects/Thesis/documents/thesis-chapters/chapter4-implementation.md") as f:
        text = f.read()

    blocks = []
    lines = text.split('\n')
    i = 0
    in_code = False
    code_buf = []

    while i < len(lines):
        line = lines[i]

        if line.startswith('```'):
            if in_code:
                blocks.append(('code', '\n'.join(code_buf)))
                code_buf = []
                in_code = False
            else:
                in_code = True
            i += 1
            continue

        if in_code:
            code_buf.append(line)
            i += 1
            continue

        if line.startswith('# ') and not line.startswith('## '):
            blocks.append(('h1', line[2:].strip()))
            i += 1
            continue

        if line.startswith('## ') and not line.startswith('### '):
            blocks.append(('h2', line[3:].strip()))
            i += 1
            continue

        if line.startswith('### ') and not line.startswith('#### '):
            blocks.append(('h3', line[4:].strip()))
            i += 1
            continue

        if line.startswith('#### '):
            blocks.append(('h4', line[5:].strip()))
            i += 1
            continue

        if line.startswith('*Table ') and line.endswith('*'):
            blocks.append(('caption', line.strip('*').strip()))
            i += 1
            continue

        if line.startswith('*Figure ') and line.endswith('*'):
            blocks.append(('caption', line.strip('*').strip()))
            i += 1
            continue

        if '|' in line and line.strip().startswith('|'):
            table_lines = []
            while i < len(lines) and '|' in lines[i] and lines[i].strip().startswith('|'):
                if not lines[i].strip().replace('|', '').replace('-', '').replace(':', '').strip() == '':
                    table_lines.append(lines[i])
                i += 1
            if table_lines:
                blocks.append(('table', table_lines))
            continue

        if line.strip().startswith('$$'):
            stripped = line.strip()
            # Single-line math: $$...$$
            if stripped.endswith('$$') and len(stripped) > 4:
                math_content = stripped[2:-2].strip()
                blocks.append(('math', math_content))
                i += 1
                continue
            # Multi-line math
            math_lines = [stripped.lstrip('$')]
            i += 1
            while i < len(lines) and not lines[i].strip().endswith('$$'):
                math_lines.append(lines[i].strip())
                i += 1
            if i < len(lines):
                math_lines.append(lines[i].strip().rstrip('$'))
            blocks.append(('math', ' '.join(l for l in math_lines if l)))
            i += 1
            continue

        if not line.strip():
            i += 1
            continue

        para_lines = [line]
        i += 1
        while (i < len(lines) and lines[i].strip()
               and not lines[i].startswith('#')
               and not lines[i].startswith('```')
               and not lines[i].startswith('*Table ')
               and not lines[i].startswith('*Figure ')
               and not (lines[i].strip().startswith('|') and '|' in lines[i])
               and not lines[i].startswith('$$')):
            para_lines.append(lines[i])
            i += 1
        para = ' '.join(para_lines)
        blocks.append(('para', para))

    return blocks


blocks = parse_chapter()
print(f"Total blocks: {len(blocks)}")

type_counts = {}
for bt, _ in blocks:
    type_counts[bt] = type_counts.get(bt, 0) + 1
for t, c in sorted(type_counts.items()):
    print(f"  {t}: {c}")

print()
print("=== ALL HEADINGS ===")
for i, (bt, content) in enumerate(blocks):
    if bt in ('h1', 'h2', 'h3', 'h4'):
        print(f"  Block {i:3d}: {bt} -> {content[:80]}")

expected_headings = [
    "4.1", "4.2", "4.2.1", "4.2.2", "4.2.3", "4.2.4",
    "4.3", "4.3.1", "4.3.2",
    "4.4", "4.4.1", "4.4.2",
    "4.5", "4.5.1", "4.5.2", "4.5.3",
    "4.6", "4.6.1", "4.6.2", "4.6.3",
    "4.7", "4.8", "4.8.1", "4.8.2", "4.8.3", "4.8.4",
    "4.9", "4.9.1", "4.9.2", "4.9.3",
    "Chapter Summary"
]

print()
print("=== HEADING CHECKLIST ===")
all_heading_text = [c for bt, c in blocks if bt in ('h1', 'h2', 'h3', 'h4')]
for exp in expected_headings:
    found = any(exp in h for h in all_heading_text)
    status = "OK" if found else "MISSING"
    print(f"  {status}: {exp}")
