---
name: quillbot-free-tier-limits
description: QuillBot AI Humanizer free tier has 125-word limit and blocks after ~3 uses requiring sign-up
type: feedback
---

QuillBot AI Humanizer free tier limits to 125 words per humanization and shows a "Sign up to use Advanced Humanize" modal after approximately 3 uses, blocking further humanizations without an account.

**Why:** Discovered during Chapter 1 humanization session on 2026-03-18. The text-humanizer agent instructions say 200-word limit but it is actually 125 words now.

**How to apply:** When humanizing thesis text, pre-split paragraphs into chunks of ~120 words at sentence boundaries. For bulk processing, either: (1) sign up for QuillBot, (2) pre-compute humanized text and embed it in the publishing script's HUMANIZED_PARAGRAPHS dict, or (3) reload the page between uses to reset the session counter (may not always work).
