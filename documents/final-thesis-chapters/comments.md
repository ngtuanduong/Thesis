# Thesis Comments Report

- **Doc ID:** `1B72mF57eyHFaCgTI-zVvZ01RWOuJInFemI-dVl_qxvA`
- **Pulled at (UTC):** 2026-05-10T08:30:04+00:00
- **Total comments:** 23  (open: 21, resolved: 2)
- **Located in a chapter:** 21 / 23  (unlocated are typically resolved comments — DOCX export drops their anchors)

> Location info is derived by exporting the Google Doc as DOCX and reading the inline comment anchor markers. Each comment's containing chapter (and the nearest sub-heading) is shown alongside the actual paragraph text the advisor was looking at.

---

## Comment #1 — Bui Quoc Khanh — OPEN

- **Comment ID:** `AAAB4sc04rg`
- **Created:** 2026-04-21T13:53:00.000Z
- **Located in:** [14-chapter-6-conclusion/14-chapter-6-conclusion.md](14-chapter-6-conclusion/14-chapter-6-conclusion.md) — CHAPTER 6. CONCLUSION
- **Nearest sub-heading:** (H2) 6.1. Summary of Work

**Anchored text (what the comment is pointing to):**

> In summary, this thesis designed, implemented, and deployed a working adaptive learning platform, and specified a rigorous evaluation protocol for future empirical validation.

**Comment:**

one-sentence takeaway cho slide cuối hội thảo

---

## Comment #2 — Bui Quoc Khanh — OPEN

- **Comment ID:** `AAAB4sc04rY`
- **Created:** 2026-04-21T13:52:00.000Z
- **Located in:** [12-chapter-5-pilot-evaluation-design-and-preliminary/12-chapter-5-pilot-evaluation-design-and-preliminary.md](12-chapter-5-pilot-evaluation-design-and-preliminary/12-chapter-5-pilot-evaluation-design-and-preliminary.md) — CHAPTER 5. PILOT EVALUATION DESIGN AND PRELIMINARY PROTOCOL
- **Nearest sub-heading:** (H3) Experimental Design Overview

**Anchored text (what the comment is pointing to):**

> This design holds constant the effect of the four-layer adaptive engine (Layers 1-4) while varying for other potential influences such as platform newness, problem content, or practicing with the online system itself. Both groups use the same interface; the only difference is the algorithm that oper

**Comment:**

Câu này viết chưa chuẩn logic. Không phải ‘holds constant the effect of the four-layer adaptive engine’, mà là ‘holds constant the platform interface and problem environment while varying the recommendation logic’.

---

## Comment #3 — Bui Quoc Khanh — OPEN

- **Comment ID:** `AAAB4sc04rc`
- **Created:** 2026-04-21T13:52:00.000Z
- **Located in:** [12-chapter-5-pilot-evaluation-design-and-preliminary/12-chapter-5-pilot-evaluation-design-and-preliminary.md](12-chapter-5-pilot-evaluation-design-and-preliminary/12-chapter-5-pilot-evaluation-design-and-preliminary.md) — CHAPTER 5. PILOT EVALUATION DESIGN AND PRELIMINARY PROTOCOL
- **Nearest sub-heading:** (H2) 5.4. Threats to Validity

**Anchored text (what the comment is pointing to):**

> Taken together, these threats mean that any findings reported from this pilot should be interpreted as preliminary evidence about the feasibility and perceived value of the integrated platform, not as a definitive comparative evaluation of the individual adaptive techniques.

**Comment:**

Đây là câu nên trích lại gần như y nguyên khi trả lời Q&A

---

## Comment #4 — Bui Quoc Khanh — OPEN

- **Comment ID:** `AAAB4sc04rU`
- **Created:** 2026-04-21T13:51:00.000Z
- **Located in:** [12-chapter-5-pilot-evaluation-design-and-preliminary/12-chapter-5-pilot-evaluation-design-and-preliminary.md](12-chapter-5-pilot-evaluation-design-and-preliminary/12-chapter-5-pilot-evaluation-design-and-preliminary.md) — CHAPTER 5. PILOT EVALUATION DESIGN AND PRELIMINARY PROTOCOL
- **Nearest sub-heading:** (H2) Chapter Summary

**Anchored text (what the comment is pointing to):**

> At the time of writing, the adaptive learning platform has been designed, implemented, and deployed in a functional form, as documented in Chapters 3 and 4. However, the full classroom intervention described in this chapter has not yet been executed. This chapter therefore presents the pilot evaluat

**Comment:**

Đây là câu quan trọng nhất của Chapter 5. Giữ, và đưa nguyên tinh thần này vào slide evaluation ở hội thảo.

---

## Comment #5 — Bui Quoc Khanh — OPEN

- **Comment ID:** `AAAB4sc04rQ`
- **Created:** 2026-04-21T13:50:00.000Z
- **Located in:** [11-chapter-4-implementation/11-chapter-4-implementation.md](11-chapter-4-implementation/11-chapter-4-implementation.md) — CHAPTER 4. IMPLEMENTATION
- **Nearest sub-heading:** (H2) Chapter Summary

**Anchored text (what the comment is pointing to):**

> This chapter discussed the implementation of the adaptive learning platform: the technology stack, knowledge graph construction, the four adaptive layers (BKT, Elo, MAB, FSRS), the optional LLM feedback layer, the frontend components, and the deployment configuration. In total, the implementation tr

**Comment:**

Đưa cái này vào hội thảo

**Replies (1):**

- **Bui Quoc Khanh** (2026-04-21T13:50:00.000Z):
  > Đây là bằng chứng rất tốt cho việc hệ thống đã được triển khai thật, không chỉ là conceptual design

---

## Comment #6 — Bui Quoc Khanh — OPEN

- **Comment ID:** `AAAB4sc04rI`
- **Created:** 2026-04-21T13:49:00.000Z
- **Located in:** [11-chapter-4-implementation/11-chapter-4-implementation.md](11-chapter-4-implementation/11-chapter-4-implementation.md) — CHAPTER 4. IMPLEMENTATION
- **Nearest sub-heading:** (H3) 4.5.2. Reward Function

**Anchored text (what the comment is pointing to):**

> There are three parts to the reward signal that guides MAB learning: learning gain, difficulty match, and efficiency. Learning gain carries a weight of 0.5 and measures the change in BKT mastery before and after the attempt. Because raw mastery deltas are typically small (0.01--0.05 per interaction)

**Comment:**

Thêm một câu nói rõ đây là heuristic weighting để kết hợp learning gain, difficulty match, and efficiency; chưa phải weight được học từ dữ liệu thực nghiệm.

---

## Comment #7 — Bui Quoc Khanh — OPEN

- **Comment ID:** `AAAB4sc04rE`
- **Created:** 2026-04-21T13:48:00.000Z
- **Located in:** [10-chapter-3-system-requirements-and-architecture/10-chapter-3-system-requirements-and-architecture.md](10-chapter-3-system-requirements-and-architecture/10-chapter-3-system-requirements-and-architecture.md) — CHAPTER 3. SYSTEM REQUIREMENTS AND ARCHITECTURE
- **Nearest sub-heading:** (H3) 3.3.3. Layer 2: Difficulty Calibrator (Dynamic Elo)

**Anchored text (what the comment is pointing to):**

> The base value K_base is set to 25. Elo [17] originally recommended K = 32 for new players and K = 16 for established players in chess; the base value of 25 serves as a midpoint suitable for the educational context, where rating volatility should be moderate. The function f_novelty(n) = max(1.0, 2.0

**Comment:**

Thêm 1 câu giải thích K=25 là heuristic midpoint chosen for moderate volatility in education, not a tuned optimum.Hội đồng thường hỏi ngay về hyperparameter.

---

## Comment #8 — Bui Quoc Khanh — OPEN

- **Comment ID:** `AAAB4sc04rA`
- **Created:** 2026-04-21T13:47:00.000Z
- **Located in:** [10-chapter-3-system-requirements-and-architecture/10-chapter-3-system-requirements-and-architecture.md](10-chapter-3-system-requirements-and-architecture/10-chapter-3-system-requirements-and-architecture.md) — CHAPTER 3. SYSTEM REQUIREMENTS AND ARCHITECTURE
- **Nearest sub-heading:** (H3) 3.3.2. Layer 1: Knowledge Tracer (BKT)

**Anchored text (what the comment is pointing to):**

> The mastery threshold of 0.85 was selected based on standard practice in BKT implementations, where mastery at or above 0.80 to 0.90 is recommended for prerequisite gating [16]. Setting the threshold at 0.95 would require excessive practice on already-understood concepts, while 0.70 risks advancing 

**Comment:**

Thêm 1 câu chốt rõ: threshold này là design choice informed by literature, not empirically optimized on this dataset. Như vậy sẽ tránh bị hỏi vặn “vì sao 0.85 mà không phải 0.8 hay 0.9”.

---

## Comment #9 — Bui Quoc Khanh — OPEN

- **Comment ID:** `AAAB4sc04q8`
- **Created:** 2026-04-21T13:46:00.000Z
- **Located in:** [10-chapter-3-system-requirements-and-architecture/10-chapter-3-system-requirements-and-architecture.md](10-chapter-3-system-requirements-and-architecture/10-chapter-3-system-requirements-and-architecture.md) — CHAPTER 3. SYSTEM REQUIREMENTS AND ARCHITECTURE
- **Nearest sub-heading:** (H4) 2.4.3 How This Thesis Addresses the Integration Question

**Anchored text (what the comment is pointing to):**

> CHAPTER 3. SYSTEM REQUIREMENTS AND ARCHITECTURE

**Comment:**

Chapter 3–4 – phần kỹ thuật là điểm mạnh, nên làm nổi hơn

---

## Comment #10 — Bui Quoc Khanh — OPEN

- **Comment ID:** `AAAB4sc04q4`
- **Created:** 2026-04-21T13:44:00.000Z
- **Modified:** 2026-04-21T13:45:00.000Z
- **Located in:** [09-chapter-2-literature-review-and-theoretical-backgr/09-chapter-2-literature-review-and-theoretical-backgr.md](09-chapter-2-literature-review-and-theoretical-backgr/09-chapter-2-literature-review-and-theoretical-backgr.md) — CHAPTER 2. LITERATURE REVIEW AND THEORETICAL BACKGROUND
- **Nearest sub-heading:** (H4) 2.2.6 Knowledge Graphs and Graph Neural Networks

**Anchored text (what the comment is pointing to):**

> 2.2.7 Large Language Models in Education

**Comment:**

Rút 20–30% độ dài. Giữ lại đúng phần phục vụ cho lựa chọn kiến trúc của thesis; bỏ bớt benchmark chi tiết không phục vụ trực tiếp cho quyết định thiết kế

**Replies (2):**

- **Bui Quoc Khanh** (2026-04-21T13:44:00.000Z):
  > vì sao chọn BKT thay vì DKT2, vì sao dùng FSRS, vì sao LLM là optional.
- **Bui Quoc Khanh** (2026-04-21T13:45:00.000Z):
  > Cuối các đoạn nên có phần relevance to this thesis, đây là phần có giá trị nhất của literature review

---

## Comment #11 — Bui Quoc Khanh — OPEN

- **Comment ID:** `AAAB4sc04qs`
- **Created:** 2026-04-21T13:43:00.000Z
- **Located in:** [09-chapter-2-literature-review-and-theoretical-backgr/09-chapter-2-literature-review-and-theoretical-backgr.md](09-chapter-2-literature-review-and-theoretical-backgr/09-chapter-2-literature-review-and-theoretical-backgr.md) — CHAPTER 2. LITERATURE REVIEW AND THEORETICAL BACKGROUND
- **Nearest sub-heading:** (H4) 2.2.6 Knowledge Graphs and Graph Neural Networks

**Anchored text (what the comment is pointing to):**

> 2.2.6 Knowledge Graphs and Graph Neural Networks

**Comment:**

Rút 20–30% độ dài. Giữ lại đúng phần phục vụ cho lựa chọn kiến trúc của thesis; bỏ bớt benchmark chi tiết không phục vụ trực tiếp cho quyết định thiết kế

---

## Comment #12 — Bui Quoc Khanh — OPEN

- **Comment ID:** `AAAB4sc04qo`
- **Created:** 2026-04-21T13:43:00.000Z
- **Located in:** [09-chapter-2-literature-review-and-theoretical-backgr/09-chapter-2-literature-review-and-theoretical-backgr.md](09-chapter-2-literature-review-and-theoretical-backgr/09-chapter-2-literature-review-and-theoretical-backgr.md) — CHAPTER 2. LITERATURE REVIEW AND THEORETICAL BACKGROUND
- **Nearest sub-heading:** (H4) 2.2.2 Deep Knowledge Tracing and Recent Advances

**Anchored text (what the comment is pointing to):**

> 2.2.2 Deep Knowledge Tracing and Recent Advances

**Comment:**

Rút 20–30% độ dài. Giữ lại đúng phần phục vụ cho lựa chọn kiến trúc của thesis; bỏ bớt benchmark chi tiết không phục vụ trực tiếp cho quyết định thiết kế

---

## Comment #13 — Bui Quoc Khanh — OPEN

- **Comment ID:** `AAAB4sc04qg`
- **Created:** 2026-04-21T13:42:00.000Z
- **Located in:** [08-chapter-1-introduction/08-chapter-1-introduction.md](08-chapter-1-introduction/08-chapter-1-introduction.md) — CHAPTER 1. INTRODUCTION
- **Nearest sub-heading:** (H2) 1.8. Thesis Structure

**Anchored text (what the comment is pointing to):**

> Figure 1.4. Thesis structure roadmap showing chapter flow, contributions, and research question mapping.

**Comment:**

Kiểm tra Figure 1.4 đã khớp với contribution mới chưa. Nếu hình vẫn thể hiện logic contribution bản cũ thì phải sửa để đồng bộ với Section 1.7 và Chapter 6.

---

## Comment #14 — Bui Quoc Khanh — OPEN

- **Comment ID:** `AAAB4sc04qc`
- **Created:** 2026-04-21T11:25:00.000Z
- **Located in:** [08-chapter-1-introduction/08-chapter-1-introduction.md](08-chapter-1-introduction/08-chapter-1-introduction.md) — CHAPTER 1. INTRODUCTION
- **Nearest sub-heading:** (H2) 1.7. Contributions

**Anchored text (what the comment is pointing to):**

> This thesis makes two main contributions, together with one optional extension.

**Comment:**

Phần này đã ổn hơn nhiều. Chỉ cần thêm 1 câu ngắn ở cuối: Contribution 1 is implemented and demonstrated technically; Contribution 2 is specified but not yet empirically executed. Hội đồng cần tthays em phân biệt rõ giữa artifact đã có và evaluation chưa chạy.

---

## Comment #15 — Bui Quoc Khanh — OPEN

- **Comment ID:** `AAAB4sc04qY`
- **Created:** 2026-04-21T11:23:00.000Z
- **Located in:** [08-chapter-1-introduction/08-chapter-1-introduction.md](08-chapter-1-introduction/08-chapter-1-introduction.md) — CHAPTER 1. INTRODUCTION
- **Nearest sub-heading:** (H4) 1.6.1 Scope

**Anchored text (what the comment is pointing to):**

> Evaluation: A pilot evaluation protocol is specified for a between-subjects study with 40-60 participants, a four-week intervention, and a two-week retention follow-up. A power analysis (Chapter 5) indicates that the nominal sample size can only detect large effect sizes (Cohen's d >= 0.8) at alpha 

**Comment:**

Nên nhấn mạnh cái này ở hội thảo

---

## Comment #16 — Bui Quoc Khanh — OPEN

- **Comment ID:** `AAAB4sc04qU`
- **Created:** 2026-04-21T11:22:00.000Z
- **Located in:** [08-chapter-1-introduction/08-chapter-1-introduction.md](08-chapter-1-introduction/08-chapter-1-introduction.md) — CHAPTER 1. INTRODUCTION
- **Nearest sub-heading:** (H4) 1.5.1 Architecture Overview

**Anchored text (what the comment is pointing to):**

> Layer 3: Problem Selector (Hierarchical Multi-Armed Bandit). The problem selector will be designed as a Hierarchical Multi-Armed Bandit problem to be solved through Thompson Sampling [18], [19]. At Level 1, the system will select a concept to be studied from a set of concepts that the learner can ha

**Comment:**

Thesis đã nói system is implemented/deployed rồi, nên chuyển các câu này sang hiện tại hoặc quá khứ nhất quán, dungf thì lung tung quá

---

## Comment #17 — Bui Quoc Khanh — OPEN

- **Comment ID:** `AAAB4sc04qQ`
- **Created:** 2026-04-21T11:21:00.000Z
- **Located in:** [08-chapter-1-introduction/08-chapter-1-introduction.md](08-chapter-1-introduction/08-chapter-1-introduction.md) — CHAPTER 1. INTRODUCTION
- **Nearest sub-heading:** (H2) 1.4. Research Questions

**Anchored text (what the comment is pointing to):**

> RQ1: How accurately does the learner model embedded in the platform predict student performance? This question evaluates the foundational capability of the learner model. It is assessed by the AUC-ROC of BKT and Elo predictions on held-out submissions, the recommendation acceptance rate per difficul

**Comment:**

RQ1 đang ôm hơi nhiều thứ. Giữ trọng tâm là predictive validity; acceptance rate và convergence speed nên hạ xuống supporting indicators trong Chapter 5.

---

## Comment #18 — Bui Quoc Khanh — OPEN

- **Comment ID:** `AAAB4sc04qM`
- **Created:** 2026-04-21T11:17:00.000Z
- **Located in:** [07-abstract/07-abstract.md](07-abstract/07-abstract.md) — ABSTRACT

**Anchored text (what the comment is pointing to):**

> The platform is accompanied by a pilot evaluation protocol describing a between-subjects, pre-test / post-test study with 40-60 undergraduate students at Hanoi University over a four-week intervention and a two-week retention follow-up, using Normalized Learning Gain, model prediction accuracy, enga

**Comment:**

thêm một câu ngắn: the thesis should be read as an implementation thesis with a pilot protocol, not as a completed classroom evaluation.”Đây là câu bảo vệ thesis trước phản biện “thế kết quả đâu?”

---

## Comment #19 — Bui Quoc Khanh — OPEN

- **Comment ID:** `AAAB4sc04qk`
- **Created:** 2026-04-21T11:17:00.000Z
- **Located in:** [09-chapter-2-literature-review-and-theoretical-backgr/09-chapter-2-literature-review-and-theoretical-backgr.md](09-chapter-2-literature-review-and-theoretical-backgr/09-chapter-2-literature-review-and-theoretical-backgr.md) — CHAPTER 2. LITERATURE REVIEW AND THEORETICAL BACKGROUND
- **Nearest sub-heading:** (H4) 2.1.1 Adaptive Learning and Intelligent Tutoring Systems

**Anchored text (what the comment is pointing to):**

> Adaptive system evolution continued in the form of web-based Adaptive Educational Hypermedia (AEH) systems in the 2000s. Examples of AEH systems include AHA! [22] and KnowledgeTree [23]. These systems adapt hyperlinks' visibility and content presentation based on user models. Although the accessibil

**Comment:**

Sai factual. Duolingo là language learning, không phải programming. Sửa thành: Duolingo demonstrates the scalability of adaptive techniques in language learning, which suggests potential transfer to programming education

---

## Comment #20 — Bui Quoc Khanh — OPEN

- **Comment ID:** `AAAB4sc04qI`
- **Created:** 2026-04-21T11:14:00.000Z
- **Located in:** [06-list-of-figures/06-list-of-figures.md](06-list-of-figures/06-list-of-figures.md) — LIST OF FIGURES

**Anchored text (what the comment is pointing to):**

> Figure 1.3. Five-layer adaptive engine architecture overview Figure 1.4. Thesis structure roadmap showing chapter flow, contributions, and research question mapping

**Comment:**

Figure 1.1 đâu

---

## Comment #21 — Bui Quoc Khanh — OPEN

- **Comment ID:** `AAAB4sc04qE`
- **Created:** 2026-04-21T11:13:00.000Z
- **Located in:** [03-table-of-contents/03-table-of-contents.md](03-table-of-contents/03-table-of-contents.md) — TABLE OF CONTENTS

**Comment:**

3.1.3 đâu

---

## Comment #22 — Bui Quoc Khanh — RESOLVED

- **Comment ID:** `AAAB4sc04qA`
- **Created:** 2026-04-21T11:13:00.000Z
- **Modified:** 2026-04-21T16:11:04.976Z
- **Located in:** _(resolved comment — Google Docs DOCX export strips inline anchors for resolved comments, so position is not recoverable. Locate manually if still relevant.)_

**Comment:**

Lỗi typo

**Replies (1):**

- **Nguyễn Tuấn Dương** (2026-04-21T16:11:04.976Z):
  > _(empty)_

---

## Comment #23 — Bui Quoc Khanh — RESOLVED

- **Comment ID:** `AAAB4sc04p8`
- **Created:** 2026-04-21T11:12:00.000Z
- **Modified:** 2026-04-21T16:14:43.889Z
- **Located in:** _(resolved comment — Google Docs DOCX export strips inline anchors for resolved comments, so position is not recoverable. Locate manually if still relevant.)_

**Comment:**

Cần 2 bìa, một bìa tiếng Anh và một bìa tiếng Việt

**Replies (1):**

- **Nguyễn Tuấn Dương** (2026-04-21T16:14:43.889Z):
  > _(empty)_

---
