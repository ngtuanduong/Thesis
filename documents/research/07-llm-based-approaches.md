# LLM-Based Approaches: State of the Art (2024-2026)

LLM approaches address: **"How can large language models enhance adaptive learning?"**

---

## 1. Knowledge Graph + RAG + LLM for Programming Education — 2025

**Paper:** ScienceDirect, 2025

**What it is:** Framework integrating LLM with Retrieval-Augmented Generation leveraging a knowledge graph and user interaction history. Assesses learner code, generates formative feedback, and recommends exercises. Tested in three modes: adaptive-only, GenAI-only, hybrid.

**Why it's better:** The **hybrid GenAI-adaptive mode** achieved:
- Highest number of correct submissions
- Fewest incorrect/incomplete attempts
- Outperformed both adaptive-only AND GenAI-only modes
- Tested on 4,956 code submissions

**Application to our system:** Use KG to structure programming concepts. Use RAG to retrieve relevant problem context and student history. Use LLM to generate personalized feedback and recommend next exercises based on identified weaknesses.

**References:**
- ScienceDirect: https://www.sciencedirect.com/science/article/pii/S2666920X25001663

---

## 2. PyTutor (ChatGPT-based ITS) — 2024

**Paper:** ScienceDirect, 2024

**What it is:** Intelligent tutoring system for Python using ChatGPT for continuous guidance, problem-solving hints, and code explanations.

**Why it's better:** Higher engagement, completion rates, and success rates — particularly effective for weaker students. Key innovation: Socratic "nudge" prompts and adaptive hint specificity.

**Application to our system:** When a student is stuck on a recommended problem, use LLM for scaffolded hints that adjust in specificity based on how many times they've asked for help.

**References:**
- ScienceDirect: https://www.sciencedirect.com/science/article/pii/S2666920X24001127

---

## 3. Multimodal Knowledge Graph + RAG ITS — 2026

**Paper:** Frontiers in Computer Science, 2026

**What it is:** ITS based on automatic construction of multimodal knowledge graphs and retrieval-augmented generation.

**Application to our system:** Automatically construct KG from programming course materials and use RAG for contextually relevant tutoring and recommendations.

**References:**
- Frontiers: https://www.frontiersin.org/journals/computer-science/articles/10.3389/fcomp.2026.1777749/full
