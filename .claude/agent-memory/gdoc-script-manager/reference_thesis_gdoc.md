---
name: Thesis Google Doc + service-account auth
description: Doc ID, scopes, and credentials file used by all gdoc-* scripts in this repo
type: reference
---

- Thesis Google Doc ID: `1O4wJNovNTFjD5DORC-WOJ2AftbcjfyoQ6HuzRSlYFfA`
- Service account key: `C:/Users/duong/WebstormProjects/Thesis/infra-inkwell-465003-f2-369235afe5ac.json` (git-ignored, in repo root)
- Scopes: `https://www.googleapis.com/auth/documents`, `https://www.googleapis.com/auth/drive`
- Shared helper module: `scripts/gdoc-util-auth.py` exports `get_docs_service()`, `get_document()`, `iter_paragraphs(doc)`, constants `DOC_ID`, `KEY_FILE`, `SCOPES`. Env vars `GDOC_KEY_FILE` and `GDOC_DOC_ID` override defaults.
- Import pattern from hyphenated filename: use `importlib.util.spec_from_file_location("gdoc_util_auth", "...scripts/gdoc-util-auth.py")` since filenames contain hyphens.
