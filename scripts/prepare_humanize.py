import json, re

with open('documents/thesis-chapters/processed/chapter4-paragraphs.json', 'r') as f:
    paragraphs = json.load(f)

def extract_specials(text):
    """Extract math, bold, and code spans, replacing with placeholders."""
    placeholders = {}
    counter = [0]
    
    def replace_match(pattern, prefix, txt):
        def replacer(m):
            counter[0] += 1
            key = f'{prefix}{counter[0]}'
            placeholders[key] = m.group(0)
            return key
        return re.sub(pattern, replacer, txt)
    
    # Extract math first (most important to preserve)
    # Handle $$...$$ (display math) - shouldn't be in body paragraphs but just in case
    text = replace_match(r'\$\$[^$]+\$\$', 'DISPMATH', text)
    # Handle $...$ (inline math)
    text = replace_match(r'\$[^$]+\$', 'MATH', text)
    # Handle **...** (bold)
    text = replace_match(r'\*\*[^*]+\*\*', 'BOLD', text)
    # Handle `...` (inline code)
    text = replace_match(r'`[^`]+`', 'CODE', text)
    
    return text, placeholders

def restore_specials(text, placeholders):
    """Restore placeholders with original content."""
    for key, value in sorted(placeholders.items(), key=lambda x: -len(x[0])):
        text = text.replace(key, value)
    return text

# Process each paragraph
prepared = []
for p in paragraphs:
    clean_text, placeholders = extract_specials(p['text'])
    prepared.append({
        'id': p['id'],
        'line': p['line'],
        'original': p['text'],
        'clean_text': clean_text,
        'placeholders': placeholders,
        'words': p['words'],
        'humanized': None,
        'status': 'pending'
    })

with open('documents/thesis-chapters/processed/chapter4-humanize-queue.json', 'w') as f:
    json.dump(prepared, f, indent=2)

print(f"Prepared {len(prepared)} paragraphs for humanization")
print(f"Paragraphs with placeholders: {sum(1 for p in prepared if p['placeholders'])}")

# Show a few examples of cleaned text
for p in prepared[:5]:
    if p['placeholders']:
        print(f"\nP{p['id']} placeholders: {list(p['placeholders'].keys())}")
        print(f"  Clean: {p['clean_text'][:80]}...")
