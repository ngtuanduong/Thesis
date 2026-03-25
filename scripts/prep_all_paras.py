"""Prepare all Chapter 5 paragraphs for humanization."""
import json, re

with open('C:/Users/duong/WebstormProjects/Thesis/scripts/ch5_paragraphs.json') as f:
    paras = json.load(f)

all_prepared = []
for idx, para in enumerate(paras):
    p = para['text']
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
    all_prepared.append({
        'idx': idx,
        'words': words,
        'text': cleaned,
        'placeholders': placeholders,
        'original': p
    })

with open('C:/Users/duong/WebstormProjects/Thesis/scripts/ch5_all_prepared.json', 'w') as f:
    json.dump(all_prepared, f, indent=2)

print(f'Prepared {len(all_prepared)} paragraphs')
for item in all_prepared:
    print(f"  P{item['idx']+1}: {item['words']} words, {len(item['placeholders'])} placeholders")
