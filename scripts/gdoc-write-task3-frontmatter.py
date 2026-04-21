"""
gdoc-write-task3-frontmatter.py
Task 3: Reorder front matter + add missing sections
Task 4: Insert abbreviations table
"""
import sys, os, importlib, importlib.util, io

# Fix Windows stdout encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import warnings
warnings.filterwarnings("ignore")

spec = importlib.util.spec_from_file_location("gdoc_util_auth", os.path.join(os.path.dirname(os.path.abspath(__file__)), "gdoc-util-auth.py"))
gdoc_util_auth = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gdoc_util_auth)
get_docs_service = gdoc_util_auth.get_docs_service
DOC_ID = gdoc_util_auth.DOC_ID


def get_doc(service):
    return service.documents().get(documentId=DOC_ID).execute()


def iter_elements(doc):
    """Yield (startIndex, endIndex, text, style) for each paragraph."""
    for elem in doc["body"]["content"]:
        if "paragraph" not in elem:
            si = elem.get("startIndex", 0)
            ei = elem.get("endIndex", si)
            yield si, ei, "", "NON_PARAGRAPH"
            continue
        para = elem["paragraph"]
        text = ""
        for el in para.get("elements", []):
            if "textRun" in el:
                text += el["textRun"]["content"]
        style = para.get("paragraphStyle", {}).get("namedStyleType", "NORMAL_TEXT")
        yield elem["startIndex"], elem["endIndex"], text, style


def main():
    service = get_docs_service()
    doc = get_doc(service)

    print("=== STEP 1: Reading document structure ===")
    paragraphs = list(iter_elements(doc))

    # Find key positions
    declaration_body_idx = None  # "Declaration of Originality (Pending)" body text
    acknowledgements_body_idx = None
    toc_line_idx = None
    abstract_heading_idx = None
    chapter1_idx = None
    references_idx = None

    # Also check for existing headings
    has_declaration_heading = False
    has_acknowledgement_heading = False
    has_toc_heading = False
    has_abbreviations_heading = False
    has_list_tables_heading = False
    has_list_figures_heading = False
    has_appendix_heading = False

    for i, (start, end, text, style) in enumerate(paragraphs):
        txt = text.strip()
        if "Declaration of Originality" in txt and declaration_body_idx is None:
            declaration_body_idx = i
        if "Acknowledgements (Pending)" in txt and acknowledgements_body_idx is None:
            acknowledgements_body_idx = i
        if "Table of Contents" in txt and "List of" in txt and toc_line_idx is None:
            toc_line_idx = i
        if txt.upper() == "ABSTRACT" and style in ("HEADING_1", "HEADING_2"):
            abstract_heading_idx = i
        if "CHAPTER 1" in txt and style == "HEADING_1":
            chapter1_idx = i
        if txt.upper() == "REFERENCES" and style == "HEADING_1":
            references_idx = i
        # Check existing headings
        if txt == "DECLARATION OF AUTHORSHIP" and style == "HEADING_1":
            has_declaration_heading = True
        if txt == "ACKNOWLEDGEMENT" and style == "HEADING_1":
            has_acknowledgement_heading = True
        if txt == "TABLE OF CONTENTS" and style == "HEADING_1":
            has_toc_heading = True
        if txt == "ABBREVIATIONS" and style == "HEADING_1":
            has_abbreviations_heading = True
        if txt == "LIST OF TABLES" and style == "HEADING_1":
            has_list_tables_heading = True
        if txt == "LIST OF FIGURES" and style == "HEADING_1":
            has_list_figures_heading = True
        if txt == "APPENDIX" and style == "HEADING_1":
            has_appendix_heading = True

    print(f"  Declaration body: para {declaration_body_idx} (start={paragraphs[declaration_body_idx][0]})")
    print(f"  Acknowledgements body: para {acknowledgements_body_idx} (start={paragraphs[acknowledgements_body_idx][0]})")
    print(f"  TOC combined line: para {toc_line_idx} (start={paragraphs[toc_line_idx][0] if toc_line_idx else 'N/A'})")
    print(f"  Abstract heading: para {abstract_heading_idx} (start={paragraphs[abstract_heading_idx][0]})")
    print(f"  Chapter 1: para {chapter1_idx} (start={paragraphs[chapter1_idx][0]})")
    print(f"  References: para {references_idx}")
    print(f"  Existing headings: DECL={has_declaration_heading} ACK={has_acknowledgement_heading} TOC={has_toc_heading}")
    print(f"  ABBR={has_abbreviations_heading} TABLES={has_list_tables_heading} FIGURES={has_list_figures_heading} APPENDIX={has_appendix_heading}")

    # Print context around the front matter
    print("\n=== Front matter paragraphs ===")
    for i in range(min(45, len(paragraphs))):
        start, end, text, style = paragraphs[i]
        txt = text.strip()[:60]
        print(f"  [{i}] {start}-{end} {style:20s} '{txt}'")

    # ================================================================
    # TASK 3: Build batchUpdate requests
    # Strategy:
    # 1. Delete the "Table of Contents / List of Figures..." combined line if it exists
    # 2. If Abstract is between acknowledgements and the insertion zone, we need to handle it
    # 3. Insert sections after acknowledgements in correct order
    # 4. Add DECLARATION OF AUTHORSHIP and ACKNOWLEDGEMENT headings if missing
    # 5. Add APPENDIX at the end
    # ================================================================

    requests = []

    # --- Step A: Delete the combined TOC line ---
    if toc_line_idx is not None:
        toc_start = paragraphs[toc_line_idx][0]
        toc_end = paragraphs[toc_line_idx][1]
        requests.append({
            "deleteContentRange": {
                "range": {"startIndex": toc_start, "endIndex": toc_end}
            }
        })
        print(f"\n  Will delete TOC combined line at {toc_start}-{toc_end}")

    # Execute deletion first to get clean indices
    if requests:
        print("\n=== Executing deletion of TOC line ===")
        service.documents().batchUpdate(documentId=DOC_ID, body={"requests": requests}).execute()
        print("  Done.")
        # Re-read document
        doc = get_doc(service)
        paragraphs = list(iter_elements(doc))
        requests = []

    # Re-find positions after deletion
    declaration_body_idx = None
    acknowledgements_body_idx = None
    abstract_heading_idx = None
    chapter1_idx = None
    references_idx = None
    has_declaration_heading = False
    has_acknowledgement_heading = False
    has_toc_heading = False
    has_abbreviations_heading = False
    has_list_tables_heading = False
    has_list_figures_heading = False
    has_appendix_heading = False

    for i, (start, end, text, style) in enumerate(paragraphs):
        txt = text.strip()
        if "Declaration of Originality" in txt and declaration_body_idx is None:
            declaration_body_idx = i
        if "Acknowledgements (Pending)" in txt and acknowledgements_body_idx is None:
            acknowledgements_body_idx = i
        if txt.upper() == "ABSTRACT" and style in ("HEADING_1", "HEADING_2"):
            abstract_heading_idx = i
        if "CHAPTER 1" in txt and style == "HEADING_1":
            chapter1_idx = i
        if txt.upper() == "REFERENCES" and style == "HEADING_1":
            references_idx = i
        if txt == "DECLARATION OF AUTHORSHIP" and style == "HEADING_1":
            has_declaration_heading = True
        if txt == "ACKNOWLEDGEMENT" and style == "HEADING_1":
            has_acknowledgement_heading = True
        if txt == "TABLE OF CONTENTS" and style == "HEADING_1":
            has_toc_heading = True
        if txt == "ABBREVIATIONS" and style == "HEADING_1":
            has_abbreviations_heading = True
        if txt == "LIST OF TABLES" and style == "HEADING_1":
            has_list_tables_heading = True
        if txt == "LIST OF FIGURES" and style == "HEADING_1":
            has_list_figures_heading = True
        if txt == "APPENDIX" and style == "HEADING_1":
            has_appendix_heading = True

    print(f"\n=== After cleanup, re-scanned positions ===")
    print(f"  Declaration body: para {declaration_body_idx}")
    print(f"  Acknowledgements body: para {acknowledgements_body_idx}")
    print(f"  Abstract heading: para {abstract_heading_idx}")
    print(f"  Chapter 1: para {chapter1_idx}")

    # --- Step B: Determine if Abstract is already AFTER acknowledgements ---
    # The desired order: ...Acknowledgements... | TOC | ABBREVIATIONS | LIST OF TABLES | LIST OF FIGURES | ABSTRACT | Chapter 1
    # If abstract is currently between ack and ch1, we need to:
    #   - Insert TOC, ABBREVIATIONS, LIST OF TABLES, LIST OF FIGURES before the Abstract
    # If abstract is before ack, we'd need to move it (unlikely based on initial scan)

    # From initial scan: ack=22, abstract=24, ch1=37 -> abstract is after ack, before ch1
    # So we insert the new sections BEFORE the abstract heading

    # The insertion point is right before the Abstract heading
    insert_idx = paragraphs[abstract_heading_idx][0]
    print(f"  Insertion point (before Abstract): index {insert_idx}")

    # --- Step C: Build insertion requests ---
    # We insert in REVERSE order because each insert pushes content down
    # Final order should be: TOC -> ABBREVIATIONS -> LIST OF TABLES -> LIST OF FIGURES -> [Abstract]

    # Sections to insert (in order, will reverse for insertion)
    sections_to_insert = []

    if not has_list_figures_heading:
        sections_to_insert.append(("LIST OF FIGURES", "[To be generated]\n"))
    if not has_list_tables_heading:
        sections_to_insert.append(("LIST OF TABLES", "[To be generated]\n"))
    if not has_abbreviations_heading:
        sections_to_insert.append(("ABBREVIATIONS", ""))  # Task 4 will fill this
    if not has_toc_heading:
        sections_to_insert.append(("TABLE OF CONTENTS", "[Insert Table of Contents here using Google Docs: Insert > Table of Contents]\n"))

    # Reverse so we insert from bottom to top (last section first)
    sections_to_insert.reverse()

    for heading_text, body_text in sections_to_insert:
        # Insert body text first (if any), then heading, then page break
        # Actually for batchUpdate insertText, we insert at a fixed index and text gets pushed
        # So we need to insert in order: pagebreak, heading\n, body\n
        # But since we're inserting multiple sections at the same index, we do them in reverse

        # Each section = pagebreak + heading + newline + body
        # We'll build a text block and then apply styles

        pass  # Will use a different approach below

    # Better approach: build the full text to insert, then apply paragraph styles
    # Insert everything at insert_idx

    # Build text blocks for insertion
    # Format: \n<heading>\n<body>\n for each section
    # We'll track ranges for styling after insertion

    # Actually, the cleanest approach with Google Docs API:
    # 1. Insert text at the position
    # 2. Apply paragraph styles
    # 3. Insert page breaks

    # Let's build a comprehensive set of requests

    requests = []

    # We'll insert sections in order (TOC, ABBREVIATIONS, LIST OF TABLES, LIST OF FIGURES)
    # Each section: page break + heading + body

    # The text to insert (all at insert_idx, in order)
    # Note: inserting at a position pushes existing content forward
    # So we insert the ENTIRE block at once

    insert_text = ""
    style_ranges = []  # (relative_start, relative_end, style)

    sections_forward = []
    if not has_toc_heading:
        sections_forward.append(("TABLE OF CONTENTS", "[Insert Table of Contents here using Google Docs: Insert > Table of Contents]"))
    if not has_abbreviations_heading:
        sections_forward.append(("ABBREVIATIONS", ""))
    if not has_list_tables_heading:
        sections_forward.append(("LIST OF TABLES", "[To be generated]"))
    if not has_list_figures_heading:
        sections_forward.append(("LIST OF FIGURES", "[To be generated]"))

    # Build combined text
    current_offset = 0
    page_break_positions = []  # positions where we need page breaks

    for heading, body in sections_forward:
        # Mark page break position
        page_break_positions.append(current_offset)
        # After page break, we add a newline (the page break element takes one char)
        current_offset += 1  # page break char

        # Heading
        heading_start = current_offset
        heading_line = heading + "\n"
        current_offset += len(heading_line)
        heading_end = current_offset
        style_ranges.append((heading_start, heading_end, "HEADING_1"))

        # Body (if any)
        if body:
            body_line = body + "\n"
            current_offset += len(body_line)

    # Now build the requests in reverse order (because insertions at same index stack)
    # Actually, let's do it the proper way:
    # 1. First insert all text
    # 2. Then apply styles
    # 3. Then insert page breaks

    # Simpler approach: insert each section one by one, re-reading index isn't feasible
    # Best approach: use a single batch with calculated offsets

    # Let's use the approach of inserting text first, then styling
    # Build the plain text (without page breaks first, add those separately)

    plain_text = ""
    heading_ranges = []  # (abs_start, abs_end) for HEADING_1 styling
    offset = 0

    for heading, body in sections_forward:
        # We'll insert a newline for the page break placeholder
        plain_text += "\n"  # placeholder for page break
        offset += 1

        h_start = offset
        plain_text += heading + "\n"
        offset += len(heading) + 1
        h_end = offset
        heading_ranges.append((h_start, h_end))

        if body:
            plain_text += body + "\n"
            offset += len(body) + 1

    total_insert_len = len(plain_text)
    print(f"  Total text to insert: {total_insert_len} chars")
    print(f"  Sections to insert: {[s[0] for s in sections_forward]}")

    # Request 1: Insert the text block
    requests.append({
        "insertText": {
            "location": {"index": insert_idx},
            "text": plain_text
        }
    })

    # Request 2: Style headings as HEADING_1
    for h_start, h_end in heading_ranges:
        abs_start = insert_idx + h_start
        abs_end = insert_idx + h_end - 1  # exclude the trailing newline from style
        requests.append({
            "updateParagraphStyle": {
                "range": {"startIndex": abs_start, "endIndex": abs_end},
                "paragraphStyle": {"namedStyleType": "HEADING_1"},
                "fields": "namedStyleType"
            }
        })

    # Request 3: Insert page breaks at the placeholder newlines
    # We need to replace the \n placeholders with actual page breaks
    # Page breaks must be inserted into existing paragraphs
    # Actually, the approach of inserting \n and then adding page breaks is complex
    # Better: insert page breaks as separate requests BEFORE the heading text

    # Let me redo this with a cleaner approach using individual inserts per section
    # Since each insert shifts indices, we process from LAST to FIRST (reverse order)

    # RESET and use reverse-order insertion approach
    requests = []

    # Insert sections in REVERSE order at the same insert_idx
    # This way each insertion pushes previous ones forward and they end up in correct order
    sections_reverse = list(reversed(sections_forward))

    for heading, body in sections_reverse:
        # Insert body first (if any), then heading, then page break
        # Because we insert at the same index, later inserts appear BEFORE earlier ones
        # So: insert body -> insert heading\n -> insert pagebreak
        # Result at insert_idx: [pagebreak][heading\n][body\n]

        if body:
            requests.append({
                "insertText": {
                    "location": {"index": insert_idx},
                    "text": body + "\n"
                }
            })
            # Style body as NORMAL_TEXT (default, but let's be explicit)
            body_len = len(body) + 1
            requests.append({
                "updateParagraphStyle": {
                    "range": {"startIndex": insert_idx, "endIndex": insert_idx + body_len},
                    "paragraphStyle": {"namedStyleType": "NORMAL_TEXT"},
                    "fields": "namedStyleType"
                }
            })

        # Insert heading
        requests.append({
            "insertText": {
                "location": {"index": insert_idx},
                "text": heading + "\n"
            }
        })
        heading_len = len(heading) + 1
        requests.append({
            "updateParagraphStyle": {
                "range": {"startIndex": insert_idx, "endIndex": insert_idx + heading_len},
                "paragraphStyle": {"namedStyleType": "HEADING_1"},
                "fields": "namedStyleType"
            }
        })

        # Insert page break (as a new paragraph with page break)
        requests.append({
            "insertText": {
                "location": {"index": insert_idx},
                "text": "\n"
            }
        })
        requests.append({
            "insertPageBreak": {
                "location": {"index": insert_idx}
            }
        })

    # --- Step D: Add DECLARATION OF AUTHORSHIP heading if missing ---
    if not has_declaration_heading and declaration_body_idx is not None:
        decl_start = paragraphs[declaration_body_idx][0]
        # Insert heading before the declaration body text
        requests.append({
            "insertText": {
                "location": {"index": decl_start},
                "text": "DECLARATION OF AUTHORSHIP\n"
            }
        })
        requests.append({
            "updateParagraphStyle": {
                "range": {"startIndex": decl_start, "endIndex": decl_start + len("DECLARATION OF AUTHORSHIP\n")},
                "paragraphStyle": {"namedStyleType": "HEADING_1"},
                "fields": "namedStyleType"
            }
        })
        # Page break before declaration heading
        requests.append({
            "insertText": {
                "location": {"index": decl_start},
                "text": "\n"
            }
        })
        requests.append({
            "insertPageBreak": {
                "location": {"index": decl_start}
            }
        })

    # --- Step E: Add ACKNOWLEDGEMENT heading if missing ---
    if not has_acknowledgement_heading and acknowledgements_body_idx is not None:
        ack_start = paragraphs[acknowledgements_body_idx][0]
        requests.append({
            "insertText": {
                "location": {"index": ack_start},
                "text": "ACKNOWLEDGEMENT\n"
            }
        })
        requests.append({
            "updateParagraphStyle": {
                "range": {"startIndex": ack_start, "endIndex": ack_start + len("ACKNOWLEDGEMENT\n")},
                "paragraphStyle": {"namedStyleType": "HEADING_1"},
                "fields": "namedStyleType"
            }
        })
        requests.append({
            "insertText": {
                "location": {"index": ack_start},
                "text": "\n"
            }
        })
        requests.append({
            "insertPageBreak": {
                "location": {"index": ack_start}
            }
        })

    # --- Step F: Add APPENDIX at end ---
    if not has_appendix_heading:
        # Find end of document
        doc_end = paragraphs[-1][1]
        # Insert at end
        requests.append({
            "insertText": {
                "location": {"index": doc_end - 1},
                "text": "\nAPPENDIX\n[To be added]\n"
            }
        })
        # Style APPENDIX as HEADING_1
        # After insertion at doc_end-1, "APPENDIX" starts at doc_end-1+1 = doc_end
        appendix_start = doc_end
        requests.append({
            "updateParagraphStyle": {
                "range": {"startIndex": appendix_start, "endIndex": appendix_start + len("APPENDIX\n")},
                "paragraphStyle": {"namedStyleType": "HEADING_1"},
                "fields": "namedStyleType"
            }
        })

    print(f"\n=== Executing Task 3: {len(requests)} requests ===")

    if requests:
        try:
            service.documents().batchUpdate(documentId=DOC_ID, body={"requests": requests}).execute()
            print("  Task 3 batchUpdate SUCCESS")
        except Exception as e:
            print(f"  Task 3 FAILED: {e}")
            return

    # ================================================================
    # TASK 4: Insert abbreviations under ABBREVIATIONS heading
    # ================================================================
    print("\n=== Task 4: Insert Abbreviations ===")

    # Re-read document
    doc = get_doc(service)
    paragraphs = list(iter_elements(doc))

    # Find ABBREVIATIONS heading
    abbr_heading_idx = None
    for i, (start, end, text, style) in enumerate(paragraphs):
        if text.strip() == "ABBREVIATIONS" and style == "HEADING_1":
            abbr_heading_idx = i
            break

    if abbr_heading_idx is None:
        print("  ERROR: ABBREVIATIONS heading not found!")
        return

    # Insert after the ABBREVIATIONS heading
    abbr_heading_end = paragraphs[abbr_heading_idx][1]
    print(f"  ABBREVIATIONS heading found at para {abbr_heading_idx}, end={abbr_heading_end}")

    abbreviations = [
        "API\tApplication Programming Interface",
        "AUC\tArea Under the Curve",
        "BKT\tBayesian Knowledge Tracing",
        "CLI\tCommand Line Interface",
        "FSRS\tFree Spaced Repetition Scheduler",
        "H-MAB\tHierarchical Multi-Armed Bandit",
        "IRB\tInstitutional Review Board",
        "IRT\tItem Response Theory",
        "LLM\tLarge Language Model",
        "MAB\tMulti-Armed Bandit",
        "NLG\tNormalized Learning Gain",
        "NLP\tNatural Language Processing",
        "RAG\tRetrieval-Augmented Generation",
        "ROC\tReceiver Operating Characteristic",
        "SUS\tSystem Usability Scale",
        "TAM\tTechnology Acceptance Model",
        "ZPD\tZone of Proximal Development",
    ]

    abbr_text = "\n".join(abbreviations) + "\n"
    insert_pos = abbr_heading_end

    requests4 = []
    requests4.append({
        "insertText": {
            "location": {"index": insert_pos},
            "text": abbr_text
        }
    })

    # Style as NORMAL_TEXT and set font to Times New Roman 13pt
    requests4.append({
        "updateParagraphStyle": {
            "range": {"startIndex": insert_pos, "endIndex": insert_pos + len(abbr_text)},
            "paragraphStyle": {"namedStyleType": "NORMAL_TEXT"},
            "fields": "namedStyleType"
        }
    })
    requests4.append({
        "updateTextStyle": {
            "range": {"startIndex": insert_pos, "endIndex": insert_pos + len(abbr_text)},
            "textStyle": {
                "fontSize": {"magnitude": 13, "unit": "PT"},
                "weightedFontFamily": {"fontFamily": "Times New Roman"}
            },
            "fields": "fontSize,weightedFontFamily"
        }
    })

    print(f"  Inserting {len(abbreviations)} abbreviation entries")

    try:
        service.documents().batchUpdate(documentId=DOC_ID, body={"requests": requests4}).execute()
        print("  Task 4 batchUpdate SUCCESS")
    except Exception as e:
        print(f"  Task 4 FAILED: {e}")
        return

    # ================================================================
    # VERIFICATION
    # ================================================================
    print("\n=== VERIFICATION: Re-reading front matter structure ===")
    doc = get_doc(service)
    paragraphs = list(iter_elements(doc))

    print("\nFinal front matter sections (HEADING_1 only):")
    for i, (start, end, text, style) in enumerate(paragraphs):
        if style == "HEADING_1":
            txt = text.strip()[:70]
            print(f"  [{i}] {txt}")
        if "CHAPTER 2" in text:
            break

    print("\n=== REPORT ===")
    print("Task 3: Structural sections inserted")
    print("Task 4: 17 abbreviation entries inserted")
    print("Tasks 3-4 DONE")


if __name__ == "__main__":
    main()
