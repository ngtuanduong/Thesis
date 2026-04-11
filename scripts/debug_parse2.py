#!/usr/bin/env python3
"""Check if line endings are causing parsing issues."""
with open("C:/Users/duong/WebstormProjects/Thesis/documents/thesis-chapters/chapter4-implementation.md", "rb") as f:
    raw = f.read()

# Check line endings
crlf_count = raw.count(b'\r\n')
lf_count = raw.count(b'\n') - crlf_count
cr_count = raw.count(b'\r') - crlf_count
print(f"CRLF: {crlf_count}, LF-only: {lf_count}, CR-only: {cr_count}")

# Now read normally and check specific lines
with open("C:/Users/duong/WebstormProjects/Thesis/documents/thesis-chapters/chapter4-implementation.md") as f:
    text = f.read()

lines = text.split('\n')
print(f"\nTotal lines: {len(lines)}")

# Check around line 265
for i in range(260, 275):
    if i < len(lines):
        line = lines[i]
        print(f"  Line {i+1}: repr={repr(line[:60])}")
        print(f"           starts with '## ': {line.startswith('## ')}")
        print(f"           starts with '### ': {line.startswith('### ')}")
        if line.strip():
            print(f"           stripped starts with '#': {line.strip().startswith('#')}")
