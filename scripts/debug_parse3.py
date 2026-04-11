#!/usr/bin/env python3
"""Trace the parser step by step around the problematic area."""
with open("C:/Users/duong/WebstormProjects/Thesis/documents/thesis-chapters/chapter4-implementation.md") as f:
    text = f.read()

lines = text.split('\n')

# Simulate parser from around line 185 (the $$ math block area before 4.4.2)
# Look for the $$ lines
for i in range(180, 270):
    if i < len(lines):
        line = lines[i]
        if '$$' in line:
            print(f"  Line {i+1}: {repr(line[:80])}")

print()

# The issue is likely the $$ math parser consuming too many lines
# Let's trace from line 184 onward
print("=== Tracing from line 184 ===")
i = 184  # This should be near the first $$ in section 4.4
while i < min(len(lines), 270):
    line = lines[i]

    if line.startswith('```'):
        print(f"  Line {i+1}: CODE BLOCK START/END: {repr(line[:40])}")
        i += 1
        continue

    if line.strip().startswith('$$'):
        print(f"  Line {i+1}: MATH START: {repr(line[:80])}")
        # Simulate the math parser
        math_lines = [line.strip().lstrip('$')]
        j = i + 1
        while j < len(lines) and not lines[j].strip().endswith('$$'):
            print(f"    Line {j+1}: MATH CONT: {repr(lines[j][:80])}")
            j += 1
        if j < len(lines):
            print(f"    Line {j+1}: MATH END: {repr(lines[j][:80])}")
        print(f"    Math parser consumed lines {i+1} to {j+1}")
        i = j + 1
        continue

    if line.startswith('## ') or line.startswith('### '):
        print(f"  Line {i+1}: HEADING: {repr(line[:60])}")
        i += 1
        continue

    if not line.strip():
        i += 1
        continue

    # Paragraph
    if line.strip():
        print(f"  Line {i+1}: PARA START: {repr(line[:80])}...")
        j = i + 1
        while (j < len(lines) and lines[j].strip()
               and not lines[j].startswith('#')
               and not lines[j].startswith('```')
               and not lines[j].startswith('*Table ')
               and not lines[j].startswith('*Figure ')
               and not (lines[j].strip().startswith('|') and '|' in lines[j])
               and not lines[j].startswith('$$')):
            print(f"    Line {j+1}: PARA CONT: {repr(lines[j][:80])}")
            j += 1
        print(f"    Para consumed lines {i+1} to {j}")
        if j < len(lines):
            print(f"    Next line {j+1}: {repr(lines[j][:60])}")
        i = j
        continue

    i += 1
