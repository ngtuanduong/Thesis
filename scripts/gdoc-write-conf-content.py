"""
gdoc-write-conf-content: Apply all content-level (non-formatting) revisions
from /Users/avada/.claude/plans/d-i-y-l-c-c-magical-papert.md to the
conference-paper Google Doc.

Scope (Steps 1..3, 5..7 of the brief):
  - Priority 0 (§3.3/§3.4/§3.5/§3.6/§4.1/§4.2 enrichment + LOC update)
  - Priority 1 (2-contribution rewrite + Layer 5 disabled-in-both-arms)
  - Priority 2 (Section 4 rename + soften "first" claims)
  - Priority 4 (combine choppy + defuse "Relevance to this work" template)
  - Priority 5 (Related Work trim 15-20%)
  - Priority 6 (impersonal voice sweep)
  - Priority 7 (one-question-per-section audit; conservative, only removing
    overclaim phrases already targeted elsewhere)

Formatting (headings H2/H3, italic math variables, bold figure/table label,
caption unification) is handled by scripts/gdoc-write-conf-format.py run next.

Strategy: one documents.batchUpdate with replaceAllText requests keyed on
exact current-doc sentences. Each request is idempotent. After the batch, the
script re-fetches the doc and substring-checks a canary from each revision
to confirm the rewrite landed. Any missing canary is printed as a warning.

Usage:
    GDOC_KEY_FILE=/Users/avada/Downloads/infra-inkwell-465003-f2-369235afe5ac.json \
    GDOC_DOC_ID=1b21l8G9SXiXSYP_2k9Up3ic11OK08yus557vb8gsPhs \
    python3 scripts/gdoc-write-conf-content.py
"""
import io
import os
import sys
import importlib.util

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location(
    "gdoc_util_auth", os.path.join(HERE, "gdoc-util-auth.py")
)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

service = mod.get_docs_service()
DOC_ID = os.environ.get("GDOC_DOC_ID") or mod.DOC_ID


# ---------- Replacements ----------
# Each item: (find_text, replace_text, canary_substring_in_replace)
#
# ORDERING MATTERS: any find_text must still exist in the doc at the moment
# its request is processed. The Google Docs API processes replaceAllText
# requests in the order they appear in the batch. We rely on exact uniqueness
# of each find_text so ordering between requests is safe as long as one
# request does not wipe out a substring another request expects.
#
# Canary: a short unique substring from the replacement; after the batch we
# re-fetch the doc and grep for every canary to confirm.

REPLACEMENTS = [
    # =========================================================================
    # STEP 1 — Priority 0: content enrichment
    # =========================================================================

    # 0A §3.3 Layer 1 — tier-stratified BKT prior + asymmetric secondary-concept
    # Replace whole §3.3 body paragraph with an expanded version.
    (
        "Layer 1 maintains a per-learner, per-concept mastery posterior using the four-parameter BKT formulation of Corbett and Anderson (1995). Default parameters are tiered by problem difficulty, with easier concepts initialized to higher P(L₀) and P(T) and more challenging concepts initialized to lower priors. A concept is considered mastered when its posterior mastery exceeds the threshold θ_m = 0.85. The mastery threshold θ_m = 0.85 is a design choice informed by the intelligent-tutoring-systems literature, not an optimum obtained by empirical tuning on this dataset; the follow-up pilot will treat it as a calibration target.",
        "Layer 1 maintains a per-learner, per-concept mastery posterior using the four-parameter BKT formulation of Corbett and Anderson (1995). Prior mastery P(L₀) is initialized per difficulty tier from 0.20 at the Foundations tier down to 0.05 at the Expert tier, with transition probability P(T) scaled similarly (0.30 to 0.10); this tier-stratified initialization reduces the BKT posterior's tendency toward premature confidence on harder concepts before the first few observations arrive. For problems that tag secondary concepts in addition to the primary concept, the BKT posterior for secondary concepts is updated asymmetrically — rewarded on success but not penalized on failure — to avoid false negatives when a failure on a multi-concept problem cannot be attributed to a specific concept. A concept is considered mastered when its posterior mastery exceeds the mastery threshold θ_m = 0.85, while a separate, lower prerequisite-competence threshold θ_p = 0.60 governs Layer 3 eligibility (see Section 3.5). Both thresholds are design choices informed by the intelligent-tutoring-systems literature rather than values tuned on this dataset; the follow-up pilot will treat them as calibration targets.",
        "Prior mastery P(L₀) is initialized per difficulty tier from 0.20 at the Foundations tier",
    ),

    # 0B §3.4 Layer 2 — exponential trend-weighted K + problem-side K decay
    (
        "Layer 2 maintains dual Elo ratings: every learner has a rating initialized at 1200, and every problem has a rating initialized at 1000, 1200, or 1400 for Easy, Medium, and Hard tiers respectively, with values clamped to [400, 2800]. A dynamic K-factor in [10, 40] adjusts update magnitude based on recent trend: learners with rapidly changing ratings receive larger updates while stable learners receive smaller ones. The base value K = 25 is a heuristic midpoint chosen for moderate volatility in educational settings, not a tuned optimum. A ZPD filter restricts the candidate pool to problems whose rating differs from the learner's current rating by δ ∈ [50, 250] rating points; this operationalizes the desirable-difficulties principle in a form directly usable by Layer 3.",
        "Layer 2 maintains dual Elo ratings: every learner has a rating initialized at 1200, and every problem has a rating initialized at 1000, 1200, or 1400 for Easy, Medium, and Hard tiers respectively, with values clamped to [400, 2800]. The learner-side K is adjusted using an exponential trend weighting computed over a rolling window of the learner's last 10 submissions: rapidly improving or declining trajectories receive larger K values (up to K_max = 40), while stable trajectories settle toward K_min = 10. The problem-side K decays with attempt count as K_max / √n to prevent long-established problems from swinging on late outliers. Both formulas are design choices for pre-pilot operation; the pilot will treat them as calibration targets. A ZPD filter then restricts the candidate pool to problems whose rating differs from the learner's current rating by δ ∈ [50, 250] rating points; this operationalizes the desirable-difficulties principle in a form directly usable by Layer 3.",
        "exponential trend weighting computed over a rolling window",
    ),

    # 0C §3.5 — dual threshold θ_p vs θ_m (also closes the prerequisite/mastery mismatch)
    (
        "Layer 3 uses a two-level Thompson-sampling bandit. The outer arm selects the next concept to practise; the inner arm selects a specific problem within that concept. Arm eligibility at the outer level is gated by a prerequisite constraint derived from the knowledge graph: a concept becomes eligible only when every one of its prerequisite concepts has reached the mastery threshold θ_m. At the inner level, the ZPD filter from Section 3.4 removes out-of-range problems. The reward function combines three components into a scalar in [0, 1]: expected BKT learning gain with weight w₁ = 0.5, correctness signal w₂ = 0.3, and solve-time efficiency w₃ = 0.2. These weights are a heuristic weighting combining learning gain, difficulty match, and efficiency; they are not learned from empirical data, and re-estimating them from the pilot traces is explicitly listed as future work.",
        "Layer 3 uses a two-level Thompson-sampling bandit. The outer arm selects the next concept to practise; the inner arm selects a specific problem within that concept. Arm eligibility at the outer level is gated by a prerequisite constraint derived from the knowledge graph: a concept becomes eligible only when every one of its prerequisite concepts has reached the prerequisite-competence threshold θ_p = 0.60, which is deliberately set below the mastery threshold θ_m = 0.85 used for completion status; this separation allows the bandit to introduce a new concept as soon as its prerequisites are workably solid, without requiring full mastery first. At the inner level, the ZPD filter from Section 3.4 removes out-of-range problems. The reward function combines three components into a scalar in [0, 1]: expected BKT learning gain with weight w₁ = 0.5, correctness signal w₂ = 0.3, and solve-time efficiency w₃ = 0.2. These weights are a heuristic combining learning gain, difficulty match, and efficiency; they are not learned from empirical data, and re-estimating them from the pilot traces is explicitly listed as future work.",
        "prerequisite-competence threshold θ_p = 0.60",
    ),

    # 0D §3.6 — FSRS 120s/300s timing mapping + 0G impersonal voice + 2B-h softened "first"
    (
        "Layer 4 maintains an FSRS-5 state (19 parameters, defaults from Ye et al., 2022) per learner–concept pair, scheduling reviews when retrievability drops below 0.9. The technical novelty at this layer is the mapping from a code submission outcome to an FSRS rating. FSRS was designed for flashcard recall and expects one of four discrete ratings: Again, Hard, Good, Easy. Programming submissions offer a richer signal space: correctness on hidden tests, number of attempts, and time spent. We map this signal space to FSRS ratings through a decision rule that combines correctness (all tests passed vs partial vs failed), attempt count (first-try vs retries), and time relative to the learner's median on problems of the same difficulty tier. To the best of our knowledge, this is the first reported application of FSRS to programming skill retention.",
        "Layer 4 maintains an FSRS-5 state (19 parameters, defaults from Ye et al., 2022) per learner–concept pair, scheduling reviews when retrievability drops below 0.9. The technical novelty at this layer is the mapping from a code submission outcome to an FSRS rating. FSRS was designed for flashcard recall and expects one of four discrete ratings: Again, Hard, Good, Easy. Programming submissions offer a richer signal space: correctness on hidden tests, number of attempts, and time spent. The signal space is mapped to FSRS ratings through a decision rule that combines correctness (all tests passed vs partial vs failed), attempt count (first-try vs retries), and time relative to the learner's median on problems of the same difficulty tier. Concretely, the mapping assigns a first-attempt correct submission under 120 seconds to Easy (FSRS rating 4), under 300 seconds to Good (rating 3), and at or above 300 seconds to Hard (rating 2); any submission requiring multiple attempts is capped at Hard, and any incorrect final submission is mapped to Again (rating 1). The two time boundaries were chosen so that an average Medium-tier problem solved on the first attempt would typically land on Good. Based on the literature surveyed, this appears to be among the first reported applications of FSRS to programming skill retention.",
        "Concretely, the mapping assigns a first-attempt correct submission under 120 seconds",
    ),

    # 0E §4.2 — rewrite "Why the integration is more than the sum of its parts"
    (
        "Why the integration is more than the sum of its parts. Each layer produces an output that is consumed by another layer. The BKT posterior directly controls which arms are even eligible for the bandit to sample: a learner whose mastery of recursion's prerequisite concepts has not yet exceeded θ_m cannot be recommended a recursion problem, regardless of how interesting that problem would be for exploration. The Elo ratings then narrow the eligible arms to the learner's ZPD, removing both trivially easy and prohibitively hard options. FSRS imposes a separate channel of urgency: when a previously mastered concept's retrievability falls below threshold, the bandit's sampling is overridden in favour of review. Each handoff is simple, but their composition produces an emergent recommendation policy that no single technique achieves alone. This is the structural claim the paper makes: integration, not any individual layer, is the contribution.",
        "Why the integration is more than the sum of its parts. The override channel between Layer 4 and Layer 3 is the clearest operational evidence for this claim. When the FSRS retrievability estimate for a previously mastered concept falls below 0.9, Layer 3's outer-arm sampling is overridden and the concept is surfaced as a review recommendation regardless of its current Thompson posterior. This override is the mechanical realization of the composition described in Table 1: Layer 4 issues urgency, Layer 1 supplies eligibility, Layer 2 narrows the candidate pool, and Layer 3 arbitrates exploration versus exploitation within the surviving set. Each handoff is simple, but their composition yields an emergent recommendation policy that no single technique achieves alone. This is the structural claim the paper makes: integration, not any individual layer, is the contribution.",
        "The override channel between Layer 4 and Layer 3 is the clearest operational evidence",
    ),

    # 0F + 0G §4.1 — frontend-visualization sub-paragraph + LOC update + Priority 4A "Taken together" close
    (
        "Deployment and code metrics. The platform is deployed and operational. The adaptive engine comprises approximately 2,500 lines of Python; the NestJS backend extensions add approximately 4,000 lines of TypeScript; and the React frontend additions contribute approximately 3,000 lines of TypeScript and TSX. The knowledge graph encodes 28 programming concepts with 45 prerequisite edges across five difficulty tiers and seven topic clusters. The code execution sandbox runs each submission under a 256 MB memory limit, a five-second CPU timeout, an unprivileged user, and a disabled network. Under load testing, the recommendation endpoint produces a new Thompson-sampled choice in under 500 ms at a target of 100 concurrent users, satisfying the non-functional requirement established at design time. The source repository, Docker Compose deployment, and configuration templates are packaged as a single open-source release. This is the concrete evidence that the system has been built rather than merely specified.",
        "Deployment and code metrics. The platform is deployed and operational. The adaptive engine comprises approximately 3,900 lines of Python; the NestJS backend extensions add approximately 6,400 lines of TypeScript; and the React frontend contributes approximately 8,400 lines of TypeScript and TSX. The knowledge graph encodes 28 programming concepts with 45 prerequisite edges across five difficulty tiers and seven topic clusters. The code execution sandbox runs each submission under a 256 MB memory limit, a five-second CPU timeout, an unprivileged user, and a disabled network. Under load testing, the recommendation endpoint produces a new Thompson-sampled choice in under 500 ms at a target of 100 concurrent users, satisfying the non-functional requirement established at design time. The source repository, Docker Compose deployment, and configuration templates are packaged as a single open-source release. The learner-facing frontend surfaces the adaptive engine's internal state through three purpose-built views: (i) an interactive prerequisite-graph visualization of the 28-concept knowledge graph in which node opacity encodes current BKT mastery and edge visibility encodes prerequisite satisfaction; (ii) a review queue that renders each due item's FSRS retrievability as a circular indicator and splits the queue into due-now and upcoming segments; and (iii) a progressive three-level Socratic hint panel whose prompts are grounded in the learner's current code, error output, and Layer 1 mastery state. These views are deliberate: the closed-loop pipeline of Figure 3 is a backend property, but it becomes actionable only if the learner can inspect and respond to the state it produces. Taken together, the deployed system, the packaged source repository, and the reproducible Docker-based configuration constitute concrete evidence that the platform has been implemented rather than merely specified.",
        "approximately 3,900 lines of Python",
    ),

    # =========================================================================
    # STEP 2 — Priority 1: 2 contributions + Layer 5 disabled in both arms
    # =========================================================================

    # 1A-a VN Tóm tắt — 2 đóng góp, impersonal
    (
        "Đóng góp: (i) kiến trúc tích hợp đầu tiên cho giáo dục lập trình; (ii) bandit phân cấp theo điều kiện tiên quyết BKT; (iii) lần đầu áp dụng FSRS cho lập trình qua ánh xạ nộp bài sang mức ôn tập.",
        "Bài viết này đưa ra hai đóng góp: (1) thiết kế và triển khai một nền tảng thích ứng năm lớp tích hợp, hợp nhất BKT, Elo, bandit phân cấp và FSRS dưới một đồ thị tri thức chung — trong đó bandit phân cấp có điều kiện tiên quyết dựa trên mức thông thạo BKT và ánh xạ nộp bài sang mức ôn tập FSRS là các chi tiết kỹ thuật nằm bên trong nền tảng; (2) một giao thức đánh giá thí điểm đã đăng ký trước, quy định rõ nghiên cứu tại lớp học sẽ đo ảnh hưởng của nền tảng lên kết quả học.",
        "Bài viết này đưa ra hai đóng góp:",
    ),

    # 1A-b + 2B-b/2B-c EN Abstract — 2 contributions, softened "first"
    (
        "The paper contributes (i) the first integrated adaptive architecture combining all four techniques for programming; (ii) a prerequisite-constrained hierarchical bandit with BKT-based mastery gating; and (iii) the first application of FSRS to programming skill retention through a novel code-submission-to-rating mapping.",
        "This paper makes two contributions: (1) the design and implementation of an integrated five-layer adaptive platform unifying BKT, Elo, hierarchical MAB, and FSRS under a shared knowledge graph — a platform that in turn introduces a prerequisite-constrained hierarchical bandit with BKT-mastery gating and a code-submission-to-FSRS-rating mapping, for which no equivalent system was identified in the literature surveyed by this paper; (2) a pre-registered pilot evaluation protocol specifying the classroom study that will measure the platform's learning effect.",
        "This paper makes two contributions: (1) the design and implementation",
    ),

    # 1B §3.7 — Layer 5 disabled in both arms (add the clarifying phrase)
    (
        "Layer 5 provides Socratic-style hints via a retrieval-augmented generation pipeline grounded in the learner's current BKT state (Wang et al., 2023). The layer is designed as a feature-flagged capability that is disabled by default during evaluation to prevent confounding the effect of Layers 1–4.",
        "Layer 5 provides Socratic-style hints via a retrieval-augmented generation pipeline grounded in the learner's current BKT state (Wang et al., 2023). The layer is designed as a feature-flagged capability that is disabled in both the experimental and control arms of the pilot, so that the measurement of the adaptive recommendation logic in Layers 1–4 is not confounded by the hint channel.",
        "disabled in both the experimental and control arms of the pilot",
    ),

    # 1B §3.8 — full-five-layer → Layers 1-4; Layer 5 disabled in both arms
    (
        "The experimental group uses the full five-layer adaptive engine; the control group uses the identical platform with the adaptive layers replaced by legacy content-based filtering.",
        "The experimental group uses Layers 1–4 of the adaptive engine (Layer 5 LLM hints are disabled in both arms to prevent the hint channel from confounding the measurement of the adaptive recommendation logic itself); the control group uses the identical platform with the adaptive layers replaced by legacy content-based filtering.",
        "The experimental group uses Layers 1–4 of the adaptive engine (Layer 5 LLM hints are disabled in both arms",
    ),

    # 1A-c + 1A-f + 2B-e/f Intro contribution paragraph — full rewrite, no First/Second/Third, impersonal
    (
        "The paper makes three contributions. First, it presents the first integrated multi-layer adaptive architecture combining BKT, Elo, hierarchical MAB, and FSRS for programming education. Second, it introduces a prerequisite-constrained hierarchical bandit in which arm eligibility is gated by BKT mastery estimates and further filtered by Elo-based ZPD constraints. Third, it reports the first application of FSRS to programming skill retention, achieved through a novel mapping from code submission outcomes to FSRS review ratings. A fourth, engineering-level contribution is a fully deployed open-source platform comprising a React frontend, a NestJS API, a FastAPI adaptive engine, a PostgreSQL database, and a Docker-based sandboxed code execution environment.",
        "This paper contributes, at the level of the platform itself, an integrated multi-layer adaptive architecture combining BKT, Elo, hierarchical MAB, and FSRS for programming education; the architecture is realized through a prerequisite-constrained hierarchical bandit in which arm eligibility is gated by BKT mastery estimates and further filtered by Elo-based ZPD constraints, together with an application of FSRS to programming skill retention via a code-submission-to-rating mapping that, based on the literature surveyed, is among the first reported in this setting. The platform is materialized as a fully deployed open-source system comprising a React frontend, a NestJS API, a FastAPI adaptive engine, a PostgreSQL database, and a Docker-based sandboxed code execution environment, rather than being packaged as an additional, separately numbered contribution. Accompanying the platform, this paper also contributes a pre-registered pilot evaluation protocol that specifies the classroom study designed to measure the platform's learning effect.",
        "This paper contributes, at the level of the platform itself, an integrated multi-layer adaptive architecture",
    ),

    # 1A-f Conclusion paragraph 1 — CT1 + CT2, impersonal, no "first"
    (
        "This paper has presented the design and implementation of a five-layer adaptive learning platform for university programming courses. The platform integrates Bayesian Knowledge Tracing, dynamic Elo rating, hierarchical Multi-Armed Bandits with Thompson Sampling, and the Free Spaced Repetition Scheduler into a single closed-loop system unified by a knowledge graph of 28 programming concepts. The paper contributes the first integrated architecture combining all four adaptive techniques for programming education, a prerequisite-constrained hierarchical bandit with BKT-based mastery gating, and the first application of FSRS to programming skill retention via a novel code-submission-to-rating mapping. An open-source implementation accompanies the design.",
        "This paper has presented the design and implementation of a five-layer adaptive learning platform for university programming courses. The platform integrates Bayesian Knowledge Tracing, dynamic Elo rating, hierarchical Multi-Armed Bandits with Thompson Sampling, and the Free Spaced Repetition Scheduler into a single closed-loop system unified by a knowledge graph of 28 programming concepts. The first contribution is the integrated platform itself, whose design embeds a prerequisite-constrained hierarchical bandit with BKT-mastery gating and a code-submission-to-FSRS-rating mapping as internal technical details rather than as separate claims. The second contribution is a pre-registered pilot evaluation protocol that specifies the classroom study in which the platform's learning effect will be measured. An open-source implementation accompanies the design.",
        "The first contribution is the integrated platform itself, whose design embeds a prerequisite-constrained hierarchical bandit",
    ),

    # 1B Conclusion Future Work — add "which was excluded from the pilot"
    (
        "and a full evaluation of the optional LLM Layer 5.",
        "and a full evaluation of the optional LLM Layer 5, which was excluded from the pilot.",
        "a full evaluation of the optional LLM Layer 5, which was excluded from the pilot.",
    ),

    # =========================================================================
    # STEP 3 — Priority 2: Section 4 rename + soften "first" claims
    # =========================================================================

    # 2A Section 4 heading
    (
        "4. Results and Discussion",
        "4. Implemented Artifact and Design Discussion",
        "4. Implemented Artifact and Design Discussion",
    ),

    # 2A Subsection 4.1 heading
    (
        "4.1. Results — the implemented artefact",
        "4.1. Implemented Artifact",
        "4.1. Implemented Artifact",
    ),

    # 2A §1 paper-roadmap — update reference to the renamed section
    (
        "Section 4 reports the implemented artifact and discusses design choices against literature benchmarks.",
        "Section 4 presents the implemented artifact and discusses design choices against literature benchmarks.",
        "Section 4 presents the implemented artifact and discusses design choices against literature benchmarks.",
    ),

    # 2B-a VN Tóm tắt "đầu tiên" — handled in 1A-a above (whole Đóng góp clause is rewritten). No-op here.

    # 2B-d §1 "no prior work integrates all four techniques..."
    (
        "Despite this maturity of the components, no prior work integrates all four techniques into a unified, closed-loop system for programming education.",
        "Despite this maturity of the components, no prior work identified in this review integrates all four techniques into a unified, closed-loop system for programming education.",
        "no prior work identified in this review integrates all four techniques",
    ),

    # 2B-g §2.5 "the literature does not report..." → impersonal
    (
        "Research prototypes have examined individual adaptive components in programming education, but the literature does not report a system that simultaneously integrates knowledge tracing, dynamic difficulty calibration, bandit-based selection, and spaced repetition under a shared knowledge graph.",
        "Research prototypes have examined individual adaptive components in programming education, but the literature surveyed in this paper does not report a system that simultaneously integrates knowledge tracing, dynamic difficulty calibration, bandit-based selection, and spaced repetition under a shared knowledge graph.",
        "the literature surveyed in this paper does not report a system that simultaneously integrates",
    ),

    # =========================================================================
    # STEP 5 — Priority 4: combine choppy + defuse "Relevance to this work" template
    # =========================================================================

    # 4B §1 BKT/Elo/MAB/FSRS 4 cite-sentences — combine into 1-2 flowing sentences
    (
        "The adaptive learning literature offers mature individual remedies for this mismatch. Bayesian Knowledge Tracing (BKT) estimates per-concept mastery from interaction traces (Corbett & Anderson, 1995). Elo-style rating dynamically calibrates problem difficulty relative to learner ability (Pelánek, 2016). Multi-Armed Bandit (MAB) formulations with Thompson Sampling balance exploration and exploitation when selecting the next learning activity (Chapelle & Li, 2011; Rollinson & Brunskill, 2015). The Free Spaced Repetition Scheduler (FSRS) optimizes review intervals to counter skill decay (Ye et al., 2022). Meanwhile, commercial coding platforms such as LeetCode, HackerRank, and Codeforces provide very large problem libraries but rely on static difficulty tags and offer no closed-loop mechanism for personalization; large-scale adaptive platforms such as Duolingo demonstrate the scalability of adaptive techniques in language learning, which suggests potential transfer to programming education.",
        "The adaptive learning literature offers mature individual remedies for this mismatch: Bayesian Knowledge Tracing (BKT) estimates per-concept mastery from interaction traces (Corbett & Anderson, 1995), Elo-style rating dynamically calibrates problem difficulty relative to learner ability (Pelánek, 2016), Multi-Armed Bandit (MAB) formulations with Thompson Sampling balance exploration and exploitation when selecting the next learning activity (Chapelle & Li, 2011; Rollinson & Brunskill, 2015), and the Free Spaced Repetition Scheduler (FSRS) optimizes review intervals to counter skill decay (Ye et al., 2022). Commercial coding platforms such as LeetCode, HackerRank, and Codeforces provide very large problem libraries but rely on static difficulty tags and offer no closed-loop mechanism for personalization, while large-scale adaptive platforms such as Duolingo demonstrate the scalability of adaptive techniques in language learning and suggest potential transfer to programming education.",
        "The adaptive learning literature offers mature individual remedies for this mismatch: Bayesian Knowledge Tracing",
    ),

    # 4C §2.2 — drop "Relevance to this work:" marker
    (
        "Relevance to this work: Layer 2 adopts dual Elo ratings as the difficulty-calibration mechanism, and the Elo deltas are used to filter the candidate pool to the learner's ZPD before the bandit selects.",
        "Layer 2 adopts dual Elo ratings on this basis, and the Elo deltas feed directly into the ZPD filter that constrains Layer 3.",
        "Layer 2 adopts dual Elo ratings on this basis, and the Elo deltas feed directly into the ZPD filter",
    ),

    # 4C §2.4 — drop "Relevance to this work:" marker + softened "not reported previously"
    (
        "Relevance to this work: Layer 4 applies FSRS to programming skill retention, which, to the best of our knowledge, has not been reported previously; Section 3.6 describes the novel submission-to-rating mapping this application requires.",
        "Layer 4 of the proposed platform applies FSRS to programming skill retention — an application that the surveyed literature has not previously reported; Section 3.6 describes the submission-to-rating mapping this application requires.",
        "Layer 4 of the proposed platform applies FSRS to programming skill retention — an application that the surveyed literature has not previously reported",
    ),

    # =========================================================================
    # STEP 6 — Priority 5: trim Related Work 15-20%
    # =========================================================================

    # §2 intro — remove "situates our work" impersonal fix + trim
    (
        "This section reviews the four adaptive techniques that the proposed platform integrates and situates our work with respect to prior programming-education systems. Each subsection closes with the specific design implication that the literature carries for this paper.",
        "This section reviews the four adaptive techniques that the proposed platform integrates and positions the platform with respect to prior programming-education systems.",
        "positions the platform with respect to prior programming-education systems.",
    ),

    # §2.1 — trim neural-variant description
    (
        "Bayesian Knowledge Tracing (Corbett & Anderson, 1995) models mastery of a skill as a two-state hidden Markov process with four parameters: prior knowledge P(L₀), transition P(T), guess P(G), and slip P(S). BKT is interpretable, data-efficient, and remains the reference baseline in modern intelligent tutoring systems (Ma et al., 2014). Deep Knowledge Tracing (Piech et al., 2015) and subsequent neural variants improve raw predictive accuracy but require orders of magnitude more interaction data and sacrifice the interpretability that instructors need to trust the mastery estimate. Relevance to this work: BKT is chosen as Layer 1 because this platform must operate with cold-start populations of a few hundred learners, and because the mastery estimate is consumed downstream by a bandit that benefits from calibrated uncertainty rather than raw point accuracy.",
        "Bayesian Knowledge Tracing (Corbett & Anderson, 1995) models mastery as a two-state hidden Markov process and remains the reference baseline in modern intelligent tutoring systems (Ma et al., 2014) because it is interpretable and data-efficient. Deep Knowledge Tracing (Piech et al., 2015) and subsequent neural variants trade interpretability for predictive accuracy and require orders of magnitude more interaction data. Relevance to this work: BKT is chosen as Layer 1 because the platform must operate with cold-start populations of a few hundred learners, and because the mastery estimate is consumed downstream by a bandit that benefits from calibrated uncertainty rather than raw point accuracy.",
        "Deep Knowledge Tracing (Piech et al., 2015) and subsequent neural variants trade interpretability for predictive accuracy",
    ),

    # §2.2 — tighten Vygotsky + Bjork into a lodged subclause
    (
        "Pelánek (2016) formalized Elo-style rating for adaptive educational systems, showing that dual student–item ratings converge within roughly twenty attempts per learner and stabilize faster than Item Response Theory alternatives in small cohorts. The framework operationalizes Vygotsky's (1978) Zone of Proximal Development (ZPD) and Bjork and Bjork's (2011) desirable-difficulties principle, both of which argue that optimal learning occurs when task difficulty modestly exceeds current ability.",
        "Pelánek (2016) formalized Elo-style rating for adaptive educational systems, showing that dual student–item ratings converge within roughly twenty attempts per learner and stabilize faster than Item Response Theory alternatives in small cohorts, and operationalizes the Zone of Proximal Development (Vygotsky, 1978) and the desirable-difficulties principle (Bjork & Bjork, 2011), both of which argue that optimal learning occurs when task difficulty modestly exceeds current ability.",
        "operationalizes the Zone of Proximal Development (Vygotsky, 1978) and the desirable-difficulties principle (Bjork & Bjork, 2011)",
    ),

    # §2.3 — drop Rollinson & Brunskill sentence (keep Segal as hierarchical justification)
    (
        "Thompson Sampling (Chapelle & Li, 2011) is the de facto choice for exploration–exploitation problems with small effective sample sizes, as is typical in one-semester classroom deployments. Rollinson and Brunskill (2015) demonstrated that bandit policies can outperform fixed curricula when combined with a learner model; Segal et al. (2018) extended this to structured action spaces using hierarchical bandits.",
        "Thompson Sampling (Chapelle & Li, 2011) is the de facto choice for exploration–exploitation problems with small effective sample sizes, as is typical in one-semester classroom deployments; Segal et al. (2018) extended bandit policies to structured action spaces using hierarchical bandits.",
        "Segal et al. (2018) extended bandit policies to structured action spaces using hierarchical bandits.",
    ),

    # §2.4 — drop Settles & Meeder; tighten history
    (
        "The spacing effect — that distributed practice produces better long-term retention than massed practice — is among the most robust findings in cognitive psychology (Cepeda et al., 2006). Algorithmic schedulers have evolved from heuristic SM-2 to machine-learned models (Settles & Meeder, 2016) and, most recently, to the Free Spaced Repetition Scheduler (Ye et al., 2022), which formulates the scheduling problem as a stochastic shortest-path and reports 20–30% fewer reviews than SM-2 for the same retention target. Crucially, the existing FSRS literature evaluates on vocabulary and factual-recall tasks; programming is a procedural skill whose decay dynamics are less well understood.",
        "The spacing effect — that distributed practice produces better long-term retention than massed practice — is among the most robust findings in cognitive psychology (Cepeda et al., 2006). Algorithmic schedulers have evolved from heuristic SM-2 to the Free Spaced Repetition Scheduler (Ye et al., 2022), which formulates the scheduling problem as a stochastic shortest path and reports 20–30% fewer reviews than SM-2 for the same retention target. The existing FSRS literature evaluates on vocabulary and factual-recall tasks, while programming is a procedural skill whose decay dynamics are less well understood.",
        "Algorithmic schedulers have evolved from heuristic SM-2 to the Free Spaced Repetition Scheduler",
    ),
]


def main():
    requests = []
    canaries = []
    for find_text, replace_text, canary in REPLACEMENTS:
        requests.append({
            "replaceAllText": {
                "containsText": {"text": find_text, "matchCase": True},
                "replaceText": replace_text,
            }
        })
        canaries.append((canary, find_text[:60], replace_text[:60]))

    print(f"Sending batchUpdate with {len(requests)} replaceAllText requests...")
    result = service.documents().batchUpdate(
        documentId=DOC_ID,
        body={"requests": requests},
    ).execute()

    # Report replies
    replies = result.get("replies", [])
    hit_zero = []
    for i, reply in enumerate(replies):
        occ = reply.get("replaceAllText", {}).get("occurrencesChanged", 0)
        print(f"  [{i:02}] occurrencesChanged={occ}  find={REPLACEMENTS[i][0][:60]!r}...")
        if occ == 0:
            hit_zero.append(i)

    if hit_zero:
        print(f"\nWARNING: {len(hit_zero)} requests matched 0 occurrences:")
        for i in hit_zero:
            print(f"  [{i:02}] {REPLACEMENTS[i][0][:100]!r}")

    # Verify canaries
    print("\nRe-fetching doc and verifying canaries...")
    doc = mod.get_document(service=service, doc_id=DOC_ID)
    body_text = []
    for _s, _e, text, _style in mod.iter_paragraphs(doc):
        body_text.append(text)
    joined = "\n".join(body_text)

    missing = []
    for canary, old_snip, new_snip in canaries:
        if canary not in joined:
            missing.append((canary, old_snip))
    if missing:
        print(f"\nFAIL: {len(missing)} canaries missing:")
        for c, s in missing:
            print(f"  canary={c!r}  find-was={s!r}")
    else:
        print(f"\nOK: all {len(canaries)} canaries present in updated doc.")


if __name__ == "__main__":
    main()
