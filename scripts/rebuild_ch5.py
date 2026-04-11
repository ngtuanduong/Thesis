"""Rebuild chapter5-evaluation.md with humanized paragraphs."""
import json, re

SRC = 'C:/Users/duong/WebstormProjects/Thesis/documents/thesis-chapters/chapter5-evaluation.md'
with open(SRC) as f:
    original = f.read()

with open('C:/Users/duong/WebstormProjects/Thesis/scripts/ch5_paragraphs.json') as f:
    para_info = json.load(f)

with open('C:/Users/duong/WebstormProjects/Thesis/scripts/ch5_humanized.json') as f:
    humanized = json.load(f)

# Build mapping: original text -> humanized text
replacements = {}
for i, pinfo in enumerate(para_info):
    key = str(i)
    if key in humanized:
        orig = pinfo['text']
        repl = humanized[key]
        replacements[orig] = repl

# Perform replacements in the original file
result = original
replaced_count = 0
for orig_text, new_text in replacements.items():
    if orig_text in result:
        result = result.replace(orig_text, new_text, 1)
        replaced_count += 1
    else:
        # Try matching first 80 chars
        short = orig_text[:80]
        if short in result:
            # Find the full paragraph in result and replace
            idx = result.index(short)
            # Find end of paragraph (next blank line or heading)
            end = idx
            while end < len(result) and result[end] != '\n':
                end += 1
            # Check if next line continues paragraph
            while end + 1 < len(result):
                next_line_start = end + 1
                next_line_end = result.index('\n', next_line_start) if '\n' in result[next_line_start:] else len(result)
                next_line = result[next_line_start:next_line_end].strip()
                if not next_line or next_line.startswith('#') or next_line.startswith('|') or next_line.startswith('*Table') or next_line.startswith('*Figure') or next_line.startswith('$$') or next_line.startswith('```'):
                    break
                end = next_line_end
            result = result[:idx] + new_text + result[end:]
            replaced_count += 1
        else:
            print(f'WARNING: Could not find paragraph {short[:60]}...')

with open(SRC, 'w') as f:
    f.write(result)

print(f'Replaced {replaced_count}/{len(replacements)} paragraphs')
print(f'File saved: {SRC}')
