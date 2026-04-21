"""Write Declaration of Authorship and Acknowledgement sections into the thesis Google Doc."""
import importlib.util
import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

spec = importlib.util.spec_from_file_location(
    "gdoc_util_auth",
    "C:/Users/duong/WebstormProjects/Thesis/scripts/gdoc-util-auth.py",
)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

service = m.get_docs_service()
DOC_ID = m.DOC_ID


def get_document():
    return service.documents().get(documentId=DOC_ID).execute()


def iter_paragraphs(doc):
    for elem in doc["body"]["content"]:
        if "paragraph" not in elem:
            continue
        para = elem["paragraph"]
        text = ""
        for el in para.get("elements", []):
            if "textRun" in el:
                text += el["textRun"]["content"]
        style = para.get("paragraphStyle", {}).get("namedStyleType", "NORMAL_TEXT")
        yield elem["startIndex"], elem["endIndex"], text, style


doc = get_document()

decl_start = decl_end = ack_start = ack_end = None
for start, end, text, style in iter_paragraphs(doc):
    stripped = text.strip()
    if "Declaration of Originality (Pending)" in stripped:
        decl_start, decl_end = start, end
    if "Acknowledgements (Pending)" in stripped:
        ack_start, ack_end = start, end

assert decl_start is not None, "Declaration placeholder not found"
assert ack_start is not None, "Acknowledgements placeholder not found"

print(f"Declaration: [{decl_start}, {decl_end})")
print(f"Acknowledgements: [{ack_start}, {ack_end})")

# Process in reverse order (higher index first)
ACK_TEXT = (
    "I would like to express my sincere gratitude to my supervisor, Mr. Bui Quoc Khanh, "
    "for his continuous guidance, constructive feedback, and patient support throughout the "
    "development of this thesis. His expertise and encouragement were invaluable in shaping "
    "both the direction and the quality of this work.\n"
    "I am also grateful to the Faculty of Information Technology at Hanoi University for "
    "providing the academic environment, resources, and opportunities that made this research possible.\n"
)

DECL_INTRO = (
    'I, Nguyen Tuan Duong, hereby declare that this thesis titled '
    '\u201cAdaptive Learning Platform for University Programming Courses\u201d '
    'and the work presented in it are entirely my own. I confirm that:\n'
)
DECL_BULLETS = [
    "This work was done wholly while in candidature for a Bachelor\u2019s degree at Hanoi University.\n",
    "Where I have consulted the published work of others, this is always clearly attributed.\n",
    "Where I have quoted from the work of others, the source is always given. With the exception of such quotations, this thesis is entirely my own work.\n",
    "I have acknowledged all main sources of help.\n",
    "No portion of this work has been submitted for any other degree or qualification at this or any other institution.\n",
]
DECL_SIGNATURE = "Hanoi, 2026\nNguyen Tuan Duong\nStudent ID: 2201040036\n"

DECL_TEXT = DECL_INTRO + "".join(DECL_BULLETS) + DECL_SIGNATURE

# --- Batch 1: Replace Acknowledgements (higher index) ---
requests_ack = [
    {"deleteContentRange": {"range": {"startIndex": ack_start, "endIndex": ack_end - 1}}},
    {"insertText": {"location": {"index": ack_start}, "text": ACK_TEXT}},
]
result = service.documents().batchUpdate(documentId=DOC_ID, body={"requests": requests_ack}).execute()
print(f"Acknowledgements replaced. Replies: {len(result.get('replies', []))}")

# --- Batch 2: Replace Declaration (lower index — not shifted by ack changes) ---
# Re-read doc to get fresh indices since Ack insertion may have shifted things
doc = get_document()
decl_start = decl_end = None
for start, end, text, style in iter_paragraphs(doc):
    if "Declaration of Originality (Pending)" in text.strip():
        decl_start, decl_end = start, end
        break

assert decl_start is not None, "Declaration placeholder not found after ack replacement"
print(f"Declaration (fresh): [{decl_start}, {decl_end})")

requests_decl = [
    {"deleteContentRange": {"range": {"startIndex": decl_start, "endIndex": decl_end - 1}}},
    {"insertText": {"location": {"index": decl_start}, "text": DECL_TEXT}},
]

# Calculate bullet ranges
bullet_start_offset = len(DECL_INTRO)
bullet_ranges = []
offset = bullet_start_offset
for b in DECL_BULLETS:
    b_start = decl_start + offset
    b_end = b_start + len(b)
    bullet_ranges.append((b_start, b_end))
    offset += len(b)

# Add bullet formatting requests
for b_start, b_end in bullet_ranges:
    requests_decl.append({
        "createParagraphBullets": {
            "range": {"startIndex": b_start, "endIndex": b_end},
            "bulletPreset": "BULLET_DISC_CIRCLE_SQUARE",
        }
    })

result = service.documents().batchUpdate(documentId=DOC_ID, body={"requests": requests_decl}).execute()
print(f"Declaration replaced with bullets. Replies: {len(result.get('replies', []))}")

# --- Verify ---
doc = get_document()
found_old = False
for start, end, text, style in iter_paragraphs(doc):
    if "(Pending)" in text:
        found_old = True
        print(f"WARNING: Still found '(Pending)' at [{start},{end}): {text.strip()[:80]}")

if not found_old:
    print("VERIFIED: No '(Pending)' placeholders remain. DONE.")
else:
    print("PARTIAL: Some placeholders still exist.")
