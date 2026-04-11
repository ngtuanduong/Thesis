"""Prepare a paragraph for humanization by replacing math/code/citations with placeholders."""
import json, re, sys

with open('C:/Users/duong/WebstormProjects/Thesis/scripts/ch5_paragraphs.json') as f:
    paras = json.load(f)

idx = int(sys.argv[1]) if len(sys.argv) > 1 else 0
p = paras[idx]['text']

placeholders = {}
counter = [0]

def replace_match(prefix):
    def _replace(m):
        counter[0] += 1
        key = f'{prefix}{counter[0]}'
        placeholders[key] = m.group(0)
        return key
    return _replace

# inline math $...$
cleaned = re.sub(r'\$[^$]+\$', replace_match('MATH'), p)
# bold **...**
cleaned = re.sub(r'\*\*([^*]+)\*\*', r'\1', cleaned)
# code `...`
cleaned = re.sub(r'`([^`]+)`', replace_match('CODE'), cleaned)
# citations [nn]
cleaned = re.sub(r'\[\d+\]', replace_match('CITE'), cleaned)
# em dashes
cleaned = cleaned.replace('---', ' -- ')

words = len(cleaned.split())
print(f'P{idx+1}: {words} words')
print(f'Placeholders: {json.dumps(placeholders)}')
print('---TEXT---')
print(cleaned)
print('---END---')

# Save placeholders for restoration
with open(f'C:/Users/duong/WebstormProjects/Thesis/scripts/ch5_p{idx}_placeholders.json', 'w') as f:
    json.dump(placeholders, f, indent=2)
