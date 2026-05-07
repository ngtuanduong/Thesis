---
name: DOCX-to-GoogleDoc import script
description: scripts/gdoc-write-conference-paper-docx.py replaces a Google Doc body by PATCHing it with a DOCX via Drive files.update, preserving formatting
type: reference
---

- Script: `scripts/gdoc-write-conference-paper-docx.py`
- Purpose: replace the body of an existing Google Doc with the contents of a DOCX file, preserving headings / bold / italic / tables / images / paragraph spacing. Drive re-imports the DOCX on `files.update` when the target is already a Google Doc (`application/vnd.google-apps.document`).
- Key API call: `drive.files().update(fileId=..., media_body=MediaFileUpload(path, mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document"), supportsAllDrives=True)`. No metadata body is sent — only the media is swapped.
- Why NOT `documents.batchUpdate` with insertText: that strips DOCX styling (plain text only). Drive's native DOCX importer is the only supported path that preserves fonts/headings/italics.
- Required scope: `https://www.googleapis.com/auth/drive` (full drive scope — `drive.file` is insufficient because the file wasn't created by the app). `gdoc-util-auth.py` already declares it.
- Confirmed working on 2026-04-22 against doc `1b21l8G9SXiXSYP_2k9Up3ic11OK08yus557vb8gsPhs` (conference paper): headings/images/italics/bold preserved.
- Default target doc ID is `1b21l8G9SXiXSYP_2k9Up3ic11OK08yus557vb8gsPhs` (the conference paper, distinct from the main thesis doc).
