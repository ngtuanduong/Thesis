# Chapter 2: Literature Review and Theoretical Foundations

This chapter establishes the theoretical and technical foundations upon which the adaptive learning platform is built. Section 2.1 presents the pedagogical and cognitive theories that motivate the system's design: adaptive learning principles, the Zone of Proximal Development, desirable difficulties, and the spacing effect. Section 2.2 surveys the specific technologies and algorithms employed across the five adaptive layers, including Bayesian Knowledge Tracing, Deep Knowledge Tracing, the Elo rating system, Multi-Armed Bandits, FSRS spaced repetition, knowledge graphs, and large language models in education. Section 2.3 reviews existing commercial and academic systems, analyzing their adaptive capabilities. Finally, Section 2.4 synthesizes the literature to identify the research gap that this thesis addresses: the absence of an integrated multi-layer adaptive platform for programming education.

## 2.1 Theoretical Foundations

### 2.1.1 Adaptive Learning and Intelligent Tutoring Systems

Adaptive learning refers to educational approaches that adjust instructional content, pace, and methodology based on individual learner characteristics and performance [6]. The fundamental premise is that learning outcomes improve when instruction is matched to the learner's current knowledge state, cognitive capacity, and learning trajectory. Brusilovsky [6] identified two principal modes of adaptation in web-based educational systems: *adaptive presentation*, which modifies the content shown to the learner, and *adaptive navigation support*, which guides the learner through the content space by recommending, annotating, or hiding links. Paramythis and Loidl-Reisinger [7] extended this taxonomy to four dimensions: adaptive interaction, adaptive content selection, adaptive assessment, and adaptive collaboration. The platform proposed in this thesis focuses primarily on adaptive content selection (choosing which problem to recommend) and adaptive assessment (calibrating problem difficulty to the individual learner).

The earliest adaptive educational systems were Intelligent Tutoring Systems (ITS), developed in the 1970s through 1990s. Anderson, Boyle, and Reiser [3] introduced the LISP Tutor and subsequently the Cognitive Tutor series, grounded in the ACT-R cognitive architecture. These systems maintained an explicit *student model* --- a computational representation of what the learner knows --- and used production rules to select instructional actions. The Cognitive Tutor for mathematics demonstrated improvements of 50--100% in problem-solving skills compared to traditional instruction in controlled studies [8]. A critical insight from the Cognitive Tutor research was the distinction between *model tracing*, which compares the student's solution steps against an expert model, and *knowledge tracing*, which estimates mastery of underlying skills. Both mechanisms require a fine-grained decomposition of domain knowledge into discrete skills or concepts --- a principle that directly informs the knowledge graph foundation of the platform proposed in this thesis.

The evolution of adaptive systems continued through web-based Adaptive Educational Hypermedia (AEH) in the 2000s, exemplified by systems such as AHA! [22] and KnowledgeTree [23]. These platforms adapted hyperlink visibility and content presentation based on overlay user models. The shift from desktop to web dramatically increased accessibility, though the underlying adaptation mechanisms remained largely rule-based. The current generation of adaptive platforms, emerging from the 2010s onward, leverages machine learning for data-driven adaptation. ALEKS uses Knowledge Space Theory to map student states and select optimal learning paths [9]. Khan Academy employs a mastery-based learning model requiring demonstrated proficiency before advancement [24]. Duolingo applies spaced repetition and half-life regression for language learning [10]. These platforms demonstrate that machine learning-driven adaptation can operate effectively at the scale of millions of users, motivating the application of similar techniques to programming education.

### 2.1.2 Zone of Proximal Development

The Zone of Proximal Development (ZPD), introduced by Vygotsky [20], is one of the most influential constructs in educational psychology. Vygotsky defined the ZPD as the distance between a learner's *actual developmental level*, determined by independent problem-solving ability, and their *potential developmental level*, determined by problem-solving ability under guidance or in collaboration with more capable peers. Tasks below the ZPD are too easy and produce minimal learning; tasks above the ZPD are too difficult and produce frustration and disengagement; tasks within the ZPD represent the optimal challenge level where meaningful learning occurs.

The ZPD has been operationalized in various computational forms within adaptive learning systems. In this thesis, the ZPD is operationalized through the Elo rating system (Layer 2): problems whose Elo difficulty rating falls within a calibrated range above the student's Elo ability rating are considered to be within the student's ZPD. Specifically, the system recommends problems where the problem rating falls within the range of the student rating plus a minimum offset to the student rating plus a maximum offset, where these offsets are hyperparameters corresponding to expected success rates of approximately 36--64%. This range aligns with the flow theory of Csikszentmihalyi [25], which posits that optimal engagement (the "flow state") occurs when challenge is matched to skill. The ZPD serves as a hard constraint in the problem selection pipeline: problems outside the student's ZPD are excluded from consideration regardless of other factors, ensuring that every recommendation falls within the learner's productive struggle zone.

### 2.1.3 Desirable Difficulties

Bjork and Bjork [21] introduced the framework of *desirable difficulties* --- conditions that make learning more effortful in the short term but enhance long-term retention and transfer. The key insight is counterintuitive: making retrieval practice easier (e.g., by providing hints or reducing spacing between reviews) improves immediate performance but impairs durable learning. Conversely, conditions that introduce productive struggle --- such as spacing practice over time, interleaving different topics, and testing rather than restudying --- create stronger and more flexible memory traces.

Three specific desirable difficulties are directly relevant to the design of the proposed platform:

1. **The spacing effect.** Distributing practice over time produces stronger long-term retention than massing practice in a single session [26]. This principle motivates the integration of FSRS spaced repetition scheduling (Layer 4).

2. **The testing effect.** Retrieving information from memory strengthens the memory trace more effectively than restudying the same material [27]. In the context of programming education, this means that solving a problem involving a concept (retrieval practice) is more effective for retention than re-reading notes about that concept. The platform's review mechanism operationalizes this by presenting new problems tagged with the concept due for review, rather than simply displaying the concept definition.

3. **Interleaving.** Mixing practice across different categories or topics improves the learner's ability to discriminate between problem types and select appropriate strategies [28]. The Hierarchical MAB (Layer 3) naturally produces interleaved practice by balancing exploration across multiple concepts rather than drilling a single concept exhaustively.

The desirable difficulties framework provides theoretical justification for the platform's design choice of recommending problems that are challenging but achievable (ZPD-constrained), scheduling reviews at the point of near-forgetting (FSRS), and varying the concepts practiced within each session (MAB exploration).

### 2.1.4 Spacing Effect and Forgetting Curves

The scientific study of memory decay began with Ebbinghaus [29], who demonstrated through self-experimentation that newly learned information is forgotten rapidly at first, with the rate of forgetting decelerating over time. This pattern, known as the *forgetting curve*, has been replicated extensively across diverse materials and populations. The mathematical form of the forgetting curve has been debated, with exponential, power-law, and logarithmic models proposed. Contemporary evidence favors a power-law formulation [30]:

$$R(t) = (1 + t / (c \cdot S))^{-1}$$

where $R(t)$ is retrievability (the probability of successful recall) at time $t$ after the last review, $S$ is the stability of the memory (a measure of its strength), and $c$ is a scaling constant. This is the formulation adopted by the FSRS algorithm [12], with $c = 9$ and $S$ defined such that $R(S) = 0.9$ (stability is the time at which retrievability drops to 90%).

The *spacing effect* --- the finding that distributed practice produces stronger retention than massed practice --- was also identified by Ebbinghaus and has been confirmed by Cepeda et al. [26] in a comprehensive quantitative synthesis of 254 studies. The optimal inter-study interval depends on the desired retention interval: longer retention goals require longer spacing between reviews. This relationship is precisely what spaced repetition algorithms exploit: by modeling each learner's memory decay characteristics and scheduling reviews at the point of optimal difficulty (just before the learner would forget), the system maximizes retention while minimizing the total number of reviews required.

The application of these memory science principles to programming education is a novel aspect of this thesis. While spaced repetition has been extensively applied to vocabulary learning [10] and factual recall, its application to procedural skills such as programming is underexplored. Programming concepts are not simply facts to be recalled; they are procedures to be executed. The thesis addresses this distinction through a rating mapping that translates code submission outcomes into FSRS review ratings, as detailed in Chapter 4.

## 2.2 Related Technologies

### 2.2.1 Bayesian Knowledge Tracing

Bayesian Knowledge Tracing (BKT), introduced by Corbett and Anderson [16], is the foundational algorithm for modeling student knowledge in adaptive learning systems. BKT formulates knowledge tracing as a Hidden Markov Model (HMM) with two hidden states --- *Learned* ($L$) and *Not Learned* ($\lnot L$) --- and four parameters per skill:

- $P(L_0)$: the prior probability that the student already knows the skill before any practice (typically 0.0--0.5);
- $P(T)$: the probability of transitioning from $\lnot L$ to $L$ after a single practice opportunity (the *learn rate*, typically 0.01--0.4);
- $P(G)$: the probability of a correct response when the skill is not known (the *guess rate*, typically 0.0--0.3);
- $P(S)$: the probability of an incorrect response when the skill is known (the *slip rate*, typically 0.0--0.2).

The model assumes that once a skill is learned, it remains learned (no forgetting), and that learning can only occur through practice opportunities. Given an observed response (correct or incorrect), BKT updates the posterior mastery probability using Bayes' theorem. After a correct response:

$$P(L_t \mid \text{correct}) = \frac{P(L_{t-1}) \cdot (1 - P(S))}{P(L_{t-1}) \cdot (1 - P(S)) + (1 - P(L_{t-1})) \cdot P(G)} \tag{2.1}$$

After an incorrect response:

$$P(L_t \mid \text{incorrect}) = \frac{P(L_{t-1}) \cdot P(S)}{P(L_{t-1}) \cdot P(S) + (1 - P(L_{t-1})) \cdot (1 - P(G))} \tag{2.2}$$

The learning transition is then applied:

$$P(L_{t+1}) = P(L_t \mid \text{obs}) + (1 - P(L_t \mid \text{obs})) \cdot P(T) \tag{2.3}$$

**Strengths.** BKT offers several advantages that make it suitable as the baseline knowledge tracer for this thesis. First, its parameters are directly interpretable: $P(T)$ has a clear pedagogical meaning as the learn rate, and $P(L_t)$ serves as a readily understandable mastery probability that can be used for prerequisite gating. Second, BKT is computationally efficient, requiring $O(1)$ operations per update, making it suitable for real-time applications. Third, BKT has been extensively studied and validated over three decades of research in Intelligent Tutoring Systems [8], [16]. Fourth, BKT performs well with sparse data --- even a few interactions per student per skill produce meaningful mastery estimates --- which is important for a pilot deployment with limited participants.

**Limitations.** BKT has well-documented limitations. The binary skill state ($L$ or $\lnot L$) is a coarse approximation; real knowledge exists on a continuum. The assumption of skill independence ignores the fact that programming concepts are interrelated (e.g., mastering "loops" facilitates learning "sorting"). The no-forgetting assumption is unrealistic, particularly for skills practiced infrequently --- a limitation that Layer 4 (FSRS) is specifically designed to address. Finally, BKT assumes that all problems tagged with a given skill are equally informative, which is violated when problems vary substantially in difficulty.

Parameter fitting for BKT is typically performed using Expectation-Maximization (EM). The open-source pyBKT library [31] provides a Python implementation with EM fitting, cross-validation, and support for standard educational data formats.

### 2.2.2 Deep Knowledge Tracing and Recent Advances

**Deep Knowledge Tracing (DKT).** Piech et al. [32] introduced Deep Knowledge Tracing, which replaced BKT's hand-crafted HMM with a recurrent neural network (specifically, an LSTM). DKT takes as input a sequence of (skill, correctness) tuples and outputs predicted probabilities of correctness for each skill at the next timestep. The key advantage of DKT is its ability to capture complex, nonlinear dependencies between skills without requiring explicit prerequisite modeling. However, DKT has been criticized for several shortcomings: the hidden state is a black box that cannot be directly interpreted as mastery of specific skills [33]; the model suffers from *reconstruction inconsistency*, where it predicts different mastery levels for the same skill at the same timestep [33]; and it requires large training datasets (thousands of students) to learn meaningful representations.

**DKT+ and DKVMN.** Yeung and Yeung [33] proposed DKT+, which adds regularization terms to enforce prediction consistency and reduce waviness in mastery estimates. Zhang et al. [34] introduced Dynamic Key-Value Memory Networks (DKVMN), which separate skill representation (stored in a key matrix) from student knowledge state (stored in a value matrix) using memory-augmented neural networks, providing a degree of interpretability absent in standard DKT.

**DKT2.** Doan and Sahebi [35] proposed DKT2, which represents the current state of the art in knowledge tracing as of 2025. DKT2 replaces the standard LSTM with xLSTM (Extended Long Short-Term Memory), which introduces exponential activation functions (sLSTM) for better storage decisions and matrix memory (mLSTM) for increased storage capacity with full parallelization. Critically, DKT2 integrates Item Response Theory (IRT) into the output layer, decomposing predictions into student ability and item difficulty components. This integration provides the interpretability of IRT while retaining the representational power of deep learning. DKT2 achieves state-of-the-art performance across five benchmark datasets (ASSISTments, EdNet, Junyi, Statics, NIPS34), consistently outperforming 18 baseline models including DKT, AKT, SAINT, and SAKT.

**srcML-DKT.** A particularly relevant advance for programming education is srcML-DKT [36], which extracts features from actual submitted source code rather than relying solely on binary correctness signals. Using srcML-based code representations (which can handle even unparsable code, a common occurrence in introductory programming), srcML-DKT significantly outperforms standard DKT on programming exercise datasets with $N = 610$ students. This approach demonstrates that the rich signal space of code submissions can substantially improve knowledge tracing accuracy for programming.

**UKT.** The Uncertainty-aware Knowledge Tracing model [37] represents student knowledge states as probability distributions rather than point estimates. UKT uses Wasserstein self-attention for learning state transitions and uncertainty-aware contrastive learning. The key innovation is that high uncertainty indicates the need for diagnostic problems, while low uncertainty supports confident advancement or targeted remediation --- a signal that maps naturally to the exploration bonus in Multi-Armed Bandit frameworks.

Table 2.1 summarizes the evolution of knowledge tracing approaches and their key characteristics.

**Table 2.1.** Comparison of knowledge tracing approaches.

| Approach | Architecture | Interpretable | Forgetting | Multi-skill | Data Req. | Year |
|----------|-------------|:------------:|:----------:|:-----------:|:---------:|:----:|
| BKT [16] | HMM | Yes | No | Independent | Low | 1994 |
| DKT [32] | LSTM | No | Implicit | Implicit | High | 2015 |
| DKT+ [33] | LSTM + reg. | No | Implicit | Implicit | High | 2018 |
| DKVMN [34] | Memory NN | Partial | Implicit | Explicit keys | High | 2017 |
| DKT2 [35] | xLSTM + IRT | Partial | Implicit | Implicit | High | 2025 |
| srcML-DKT [36] | DKT + code | No | Implicit | Implicit | High | 2025 |
| UKT [37] | Wasserstein attn. | Uncertainty | Implicit | Implicit | High | 2025 |

**Relevance to this thesis.** BKT is selected as the knowledge tracing engine for the proposed platform for several reasons. First, its explicit mastery probability $P(L_t)$ serves directly as the prerequisite gating criterion for the MAB layer: a concept is eligible for recommendation only when all prerequisite concepts have $P(L_t) \geq 0.85$. This requires interpretable, per-skill mastery estimates that DKT's hidden state does not provide without additional extraction. Second, BKT's low data requirement is critical for a pilot deployment with 40--60 students and approximately 30 concepts. Third, BKT's $O(1)$ update time ensures that the knowledge state can be refreshed after every submission without latency impact. DKT2 is discussed as a future upgrade path once sufficient interaction data accumulates to train a deep model (see Chapter 6).

### 2.2.3 Elo Rating System and Item Response Theory

**Classical Elo Rating.** The Elo rating system, developed by Arpad Elo [17] for chess player ranking, provides a principled method for simultaneously estimating the abilities of competitors based on their pairwise outcomes. In the educational context, each student--problem interaction is modeled as a "match" between the student and the problem. The expected probability that student $A$ with rating $R_A$ solves problem $B$ with rating $R_B$ is given by:

$$E(A, B) = \frac{1}{1 + 10^{(R_B - R_A) / 400}} \tag{2.4}$$

After observing the actual outcome $S$ (1 for correct, 0 for incorrect), both ratings are updated:

$$R'_A = R_A + K_A \cdot (S - E) \tag{2.5}$$
$$R'_B = R_B + K_B \cdot (E - S) \tag{2.6}$$

where $K$ is the update step size (K-factor) controlling the sensitivity of rating changes. When a student solves a problem they were not expected to solve ($E \approx 0, S = 1$), their rating increases substantially; when they fail a problem they were expected to solve ($E \approx 1, S = 0$), their rating decreases. This mechanism naturally calibrates both student ability and problem difficulty through ongoing interactions.

Pelanek [11] provided a comprehensive analysis of the Elo system's application to adaptive educational systems. His study demonstrated that Elo ratings converge to stable estimates within approximately 20 attempts per student and 30 attempts per problem, and that the system successfully identifies problems whose difficulty has been miscategorized by domain experts. An empirical study applying Elo to 76 programming tasks across 299 students (50,055 attempts) confirmed that Elo accurately predicts student success probability with AUC exceeding 0.7 [38].

**Connection to Item Response Theory.** Item Response Theory (IRT) is the standard psychometric framework for educational assessment. The simplest IRT model, the Rasch model (also known as the one-parameter logistic model or 1PL), has a mathematical form equivalent to the Elo expected score [39]:

$$P(\text{correct} \mid \theta, \beta) = \sigma(\theta - \beta) = \frac{1}{1 + e^{-(\theta - \beta)}} \tag{2.7}$$

where $\theta$ is the student's ability parameter and $\beta$ is the item's difficulty parameter. The Elo expected score formula (Equation 2.4) is equivalent to the Rasch model with a scaling factor: $E = \sigma((R_A - R_B) / 400 \cdot \ln 10)$. Pelanek [11] showed formally that Elo ratings converge to IRT ability and difficulty estimates under the Rasch model. The practical advantage of Elo over traditional IRT is that Elo updates incrementally after each interaction (online learning), whereas classical IRT requires batch re-estimation of all parameters whenever new data arrives. This makes Elo better suited for real-time adaptive systems where the learner model must be updated after every submission.

**Dynamic K-Value Elo.** Standard Elo uses a fixed K-factor, which creates a fundamental tradeoff: a large $K$ enables fast adaptation to genuine learning but produces volatile ratings, while a small $K$ yields stable ratings but responds slowly to changes in ability. Recent work [40] proposed a dynamic K-factor mechanism that adapts based on the student's learning trend. The trend is computed as a weighted sum of recent residuals (differences between actual and expected scores):

$$\text{trend}_t = \frac{\sum_{i=1}^{n} w_i \cdot (S_i - E_i)}{\sum_{i=1}^{n} w_i} \tag{2.8}$$

where $w_i = 0.9^{n-i}$ are exponential recency weights, $n$ is the window size, $S_i$ is the actual score, and $E_i$ is the expected score for the $i$-th recent interaction. When the trend is positive (the student is improving), $K$ decreases to stabilize the improving rating; when the trend is negative (the student is struggling), $K$ increases to enable faster re-calibration:

$$K = \begin{cases} K_{\min} + (K_{\max} - K_{\min}) \cdot e^{-\lambda \cdot \text{trend}} & \text{if trend} > 0 \\ K_{\min} + (K_{\max} - K_{\min}) \cdot (1 - e^{\lambda \cdot \text{trend}}) & \text{if trend} \leq 0 \end{cases} \tag{2.9}$$

where $K_{\min}$ and $K_{\max}$ define the range of permissible K-factors (typically 10 and 40, respectively) and $\lambda$ controls the sensitivity to the trend magnitude. This mechanism ensures that struggling students receive faster rating adjustments (they are not stuck at an inaccurate rating), while stable students experience smaller fluctuations.

**Multidimensional Elo.** Recent work in educational data mining [41] extends the Elo system to multiple dimensions, maintaining separate ratings for each concept or skill. A student thus has a vector of Elo ratings $\mathbf{R}_{\text{student}} = (R_{\text{arrays}}, R_{\text{sorting}}, R_{\text{recursion}}, \ldots)$, and each problem's Elo is associated with its primary concept. This multidimensional approach aligns naturally with the concept-based knowledge graph that underpins the proposed platform: BKT provides probabilistic mastery for prerequisite checking, while concept-specific Elo ratings provide difficulty-calibrated matching for problem selection within each concept.

**Relevance to this thesis.** The Elo system serves as Layer 2 (Difficulty Calibrator) of the proposed architecture. Its role is twofold: (1) to continuously calibrate the difficulty of each problem relative to each student's ability, enabling the operationalization of the ZPD (Section 2.1.2) as an Elo rating range; and (2) to provide the expected success probability that feeds into the MAB reward function (Layer 3). The dynamic K-value mechanism ensures efficient convergence for both rapidly improving and struggling students.

### 2.2.4 Multi-Armed Bandits in Education

**Problem Formulation.** The Multi-Armed Bandit (MAB) problem, first formalized by Robbins [42], is a classical formulation of the exploration--exploitation tradeoff. An agent faces $K$ arms (actions), each yielding stochastic rewards drawn from an unknown distribution. At each time step, the agent must choose one arm to pull and observes the resulting reward. The objective is to maximize cumulative reward over time, which requires balancing *exploitation* (choosing the arm with the highest estimated reward) against *exploration* (trying less-certain arms to gather information and potentially discover superior alternatives).

In the educational context, each arm represents a learning activity (a concept to study or a problem to attempt), and the reward represents the learning gain resulting from the activity. The MAB formulation is natural for educational recommendation because the system faces genuine uncertainty about which activity will produce the most learning for a given student at a given time, and the only way to resolve this uncertainty is to recommend activities and observe outcomes.

**Thompson Sampling.** Thompson Sampling [18], originally proposed in 1933, is a Bayesian approach to the MAB problem that has experienced a renaissance in recent years due to its strong theoretical and empirical performance [19]. For each arm $i$, the algorithm maintains a Beta distribution $\text{Beta}(\alpha_i, \beta_i)$ representing its belief about the arm's reward probability. At each decision point, the algorithm samples a value $\theta_i$ from each arm's distribution and selects the arm with the highest sampled value. After observing the reward $r$, the distribution is updated: $\alpha_i \leftarrow \alpha_i + r$ for success, $\beta_i \leftarrow \beta_i + (1 - r)$ for failure.

Thompson Sampling offers several advantages for educational recommendation. Arms with high uncertainty (wide distributions) are explored more frequently because their samples have higher variance and thus a higher probability of being the maximum --- this is precisely the behavior desired when the system is uncertain about a student's readiness for a concept. As evidence accumulates, distributions narrow and exploitation dominates, concentrating recommendations on concepts with high observed learning gains. Unlike Upper Confidence Bound (UCB) algorithms, Thompson Sampling requires no tuning parameter, making it practical for deployment.

**Hierarchical MAB for Problem Selection.** Standard MAB treats each problem as a separate arm, which becomes impractical when the problem bank contains hundreds of items. The *hierarchical* approach [43] introduces two levels of selection:

- *Level 1 (Concept Selection):* The system selects which concept to study from among those whose prerequisites are satisfied. Each concept is an arm with its own Beta distribution.
- *Level 2 (Problem Selection):* Within the selected concept, the system selects a specific problem whose difficulty falls within the student's ZPD. Each problem within a concept is an arm at this level.

This hierarchical structure mirrors the natural organization of educational content and reduces the effective number of arms at each level, enabling faster convergence. Clement et al. [44] demonstrated that MAB-based problem selection in intelligent tutoring systems produces superior learning outcomes compared to random selection and expert-designed curricula, validating the approach for educational applications.

**MAB with Abandonment.** A critical limitation of standard educational MAB models is their failure to account for student disengagement. Shen et al. [45] addressed this at NeurIPS 2024 by introducing MAB with abandonment (MAB-A), where a third outcome is modeled alongside success and failure: the student abandons the recommended activity without attempting it. Abandonment provides a strong negative signal indicating that the recommendation was inappropriate (typically too difficult or too tedious). The ULCB and KL-ULCB algorithms proposed in this work increase exploration when the student is engaged and decrease it when disengagement is detected. This finding is relevant to programming education, where abandonment rates are high for problems outside the student's ZPD --- the Elo-based ZPD filtering in the proposed platform partially addresses this, and future versions may incorporate explicit abandonment signals into the MAB reward.

**Relevance to this thesis.** The MAB framework serves as Layer 3 (Problem Selector) of the proposed architecture. The hierarchical structure, combined with BKT-based prerequisite gating (concepts are eligible only when prerequisites are mastered) and Elo-based ZPD filtering (problems are eligible only when their difficulty falls within the student's productive range), ensures that recommendations are both pedagogically sound and optimally challenging. The reward function combines BKT learning gain, difficulty appropriateness, and time efficiency, as detailed in Chapter 4.

### 2.2.5 Free Spaced Repetition Scheduler (FSRS)

**SM-2 and Traditional Algorithms.** The first widely adopted spaced repetition algorithm was SM-2, developed by Wozniak [46] for the SuperMemo system. SM-2 computes review intervals using a simple recursive formula: $I(1) = 1$ day, $I(2) = 6$ days, $I(n) = I(n-1) \times EF$, where $EF$ (Easiness Factor) is updated after each review based on a subjective quality rating on a 0--5 scale. While SM-2 was a pioneering system that enabled millions of learners to practice spaced repetition (and was later adopted by Anki), it has significant limitations: its parameters are fixed rather than optimized from data, the same parameters apply to all users regardless of individual memory characteristics, the quality rating is subjective and difficult to calibrate consistently, and the algorithm lacks a principled foundation in memory science.

**FSRS.** The Free Spaced Repetition Scheduler (FSRS), proposed by Ye [12], represents a substantial advancement over SM-2. FSRS is grounded in the *DSR model* (Difficulty, Stability, Retrievability), which tracks three memory states per item:

- *Difficulty* ($D$, scale 1--10): how inherently hard this material is for this learner.
- *Stability* ($S$, in days): the time for retrievability to decay to 90% --- the "half-life" of the memory.
- *Retrievability* ($R$, probability in [0, 1]): the current probability of successful recall.

The core forgetting curve is modeled as a power law:

$$R(t, S) = \left(1 + \frac{t}{9 \cdot S}\right)^{-1} \tag{2.10}$$

where $t$ is the elapsed time since the last review. By construction, $R(0, S) = 1$ (perfect recall immediately after review) and $R(S, S) = 0.9$ (stability is defined as the point at which retrievability drops to 90%). The stability update after a successful review is:

$$S' = S \cdot \left(e^{w_8} \cdot (11 - D)^{w_9} \cdot S^{-w_{10}} \cdot \left(e^{(1-R) \cdot w_{11}} - 1\right) \cdot h_p \cdot e_b + 1\right) \tag{2.11}$$

where $w_8$--$w_{11}$ are optimizable parameters, $h_p$ is a hard penalty factor (applied when the rating is 2), and $e_b$ is an easy bonus factor (applied when the rating is 4). After a failed review (rating = 1), the stability is reset to a shorter value based on the current difficulty and retrievability:

$$S'_{\text{fail}} = w_{12} \cdot D^{-w_{13}} \cdot \left((S+1)^{w_{14}} - 1\right) \cdot e^{(1-R) \cdot w_{15}} \tag{2.12}$$

FSRS uses four ratings to capture the quality of recall: 1 (*Again* --- complete failure), 2 (*Hard* --- recalled with significant difficulty), 3 (*Good* --- recalled with moderate effort), and 4 (*Easy* --- recalled effortlessly). The 19 parameters ($w_0$ through $w_{18}$) are optimized from the user's actual review history using gradient descent, enabling personalization to individual memory characteristics.

**Empirical validation.** FSRS has been empirically validated to require 20--30% fewer reviews than SM-2 for the same retention target [12]. It has been integrated into Anki since version 23.10 (released October 2023), providing the algorithm access to a user base of millions and enabling large-scale validation. The adoption of FSRS by a major production system provides confidence in its robustness and scalability.

**LECTOR.** A recent extension, LECTOR [47], integrates large language models with spaced repetition scheduling. LECTOR uses in-context learning to assess semantic similarity between concepts, identifying "confusable" items that should be reinforced together. The system achieved a 90.2% retention success rate compared to 88.4% for the best baseline across 100 simulated learners over 100 days. While LECTOR focuses on vocabulary-style learning, its architecture of combining spaced repetition with AI-generated content mirrors the combination of Layer 4 (FSRS) and Layer 5 (LLM feedback) in the proposed platform.

**Relevance to this thesis.** FSRS is applied as Layer 4 (Review Scheduler) in the proposed architecture. To the best of the author's knowledge, this thesis represents the first application of FSRS to programming concept review scheduling. The key adaptation is the rating mapping: rather than asking students to self-assess their recall quality (as in flashcard applications), the system automatically maps code submission outcomes to FSRS ratings based on correctness, number of attempts, and time spent. This mapping bridges the gap between FSRS's flashcard-oriented design and the richer signal space of programming exercises. The specific mapping is detailed in Chapter 4. FSRS addresses a limitation that Layers 1--3 alone cannot resolve: without scheduled review, mastered concepts gradually decay, leading to knowledge fragmentation that undermines the prerequisite dependencies modeled in the knowledge graph.

### 2.2.6 Knowledge Graphs and Graph Neural Networks

**Knowledge Graphs for Programming Concepts.** A Knowledge Graph (KG) represents domain concepts as nodes and relationships between concepts as directed edges. In the context of programming education, the primary relationship is the *prerequisite* relation: concept $A$ is a prerequisite of concept $B$ if mastery of $A$ is necessary for productive learning of $B$. For example, understanding *variables* is prerequisite to understanding *arrays*, which is prerequisite to understanding *sorting algorithms*. This hierarchical structure has been recognized in the programming education literature [2] and is a key structural feature that distinguishes programming from domains without strong prerequisite chains.

Knowledge graph construction can proceed through manual curation by domain experts, automated extraction from course materials, or a hybrid approach. The ACE (Automatic Concept Extraction) methodology [48] automates KG construction by parsing course materials, extracting key concepts using NLP, identifying prerequisite relationships from section ordering and reference patterns, and validating using student performance data. Pan et al. [49] demonstrated that prerequisite-enhanced category-aware Graph Neural Networks improve educational recommendation quality by leveraging prerequisite structures as first-class features.

**GNN-Based Educational Recommendation.** Graph Neural Networks (GNN) have been applied to educational recommendation by modeling the tripartite relationship between students, learning resources, and knowledge points. Liu et al. [50] achieved NDCG@10 of 0.93 in standard scenarios and 0.88 in knowledge gap scenarios using GNN-based recommendation on educational tripartite graphs, significantly outperforming collaborative filtering baselines. Gu et al. [51] combined Graph Attention Networks (GAT) with deep reinforcement learning for personalized learning path generation, achieving 5.8--12.8 point improvements in test scores compared to fixed curricula. These results demonstrate the value of explicitly modeling concept relationships in educational recommendation.

**Relevance to this thesis.** The proposed platform uses a manually curated knowledge graph of approximately 30 Python programming concepts with 40--50 prerequisite edges. Manual curation is justified by the manageable scale of a single-course concept space, the need for accuracy in prerequisite relationships (a single incorrect edge could permanently block learner progression), and the requirement for alignment with the specific university curriculum. The knowledge graph serves three roles: (1) defining the concept space for BKT knowledge tracing (Layer 1), (2) constraining the MAB concept selection to respect prerequisite mastery (Layer 3), and (3) providing structured context for RAG-based LLM feedback generation (Layer 5). Automated KG construction using ACE or LLM-based methods is identified as a direction for future work.

### 2.2.7 Large Language Models in Education

**LLMs as Tutoring Agents.** Large Language Models (LLMs) such as GPT-4 have demonstrated strong capabilities in educational settings. PyTutor [52], a ChatGPT-based intelligent tutoring system for Python programming, employs Socratic questioning to guide students toward solutions rather than providing direct answers. PyTutor maintains a dialogue state to track student understanding and uses prompt engineering to implement pedagogical strategies including scaffolding, analogies, and worked examples. Student satisfaction ratings of 4.2/5.0 were reported in usability studies. However, significant challenges remain in deploying LLMs for education: hallucination (generating incorrect code or explanations), tendency to give direct answers rather than guiding discovery, inconsistency across interactions, and API cost at scale.

**RAG-Enhanced Educational Systems.** Retrieval-Augmented Generation (RAG) addresses several LLM limitations by grounding generated responses in retrieved factual content. Chen et al. [53] demonstrated a three-component architecture combining a knowledge graph (storing structured domain knowledge), RAG (retrieving relevant KG subgraphs based on the student's current problem and knowledge state), and an LLM (generating personalized feedback grounded in retrieved knowledge). Testing across 4,956 code submissions, the hybrid GenAI-adaptive mode achieved the highest number of correct submissions and the fewest incorrect attempts, outperforming both adaptive-only and GenAI-only modes. Wang et al. [54] extended this approach to multimodal knowledge graphs, incorporating code examples, diagrams, and video explanations as node attributes, and achieved a 15% improvement in concept mastery compared to text-only tutoring.

**Relevance to this thesis.** The proposed platform includes an optional Layer 5 (LLM Feedback Engine) that generates Socratic hints when students struggle with a problem (three or more failed attempts). The RAG pipeline retrieves the student's knowledge state from BKT, the problem's concept prerequisites from the knowledge graph, and common mistakes associated with the concept, then prompts the LLM to generate a guiding question rather than a direct answer. This layer is explicitly designated as supplementary; the core thesis contribution stands on Layers 1 through 4. The integration of LLM feedback with a structured learner model (BKT mastery states) and a knowledge graph distinguishes this approach from standalone LLM tutors, which lack awareness of the student's knowledge state and the domain's prerequisite structure.

## 2.3 Related Work

### 2.3.1 Commercial Programming Platforms

The most widely used platforms for programming practice are LeetCode, HackerRank, Codeforces, and CodeSignal, collectively serving tens of millions of users. These platforms have achieved remarkable scale and offer extensive problem repositories, but their pedagogical architecture is fundamentally static.

**LeetCode** classifies problems into three fixed difficulty tiers (Easy, Medium, Hard) that are identical for all users regardless of their skill level. Problem selection is entirely user-driven: students browse by topic tag or difficulty label and choose their own problems. There is no knowledge model, no difficulty calibration based on individual performance, no spaced repetition, and no prerequisite awareness. LeetCode recently introduced LLM-powered hints as a premium feature, but these operate independently of any learner model. The platform is designed primarily for interview preparation rather than structured learning, and its lack of adaptation means that students have no guidance on what to practice next or when to review previously learned concepts.

**HackerRank** offers curated skill tracks and binary skill badges (attempted/not attempted) but lacks probabilistic knowledge modeling, difficulty calibration, or adaptive recommendation. Assessment is based on fixed skill tests with predetermined question sets. Like LeetCode, the platform provides no mechanism for scheduling review of previously mastered concepts.

**Codeforces** is notable for its Elo-based rating system, which accurately tracks competitive programming ability across thousands of participants. However, the Elo system is used exclusively for competitive ranking and contest matchmaking, not for pedagogical recommendation. There is no knowledge tracing, no concept prerequisite awareness, and no mechanism to recommend practice problems matched to a specific learner's ZPD. Codeforces is designed for competitive programmers, not for learners who need structured guidance through a curriculum.

**CodeSignal** employs an Elo-IRT hybrid system for skill assessment, providing more sophisticated ability estimation than simple binary scoring. However, the assessment results are used primarily for candidate evaluation in hiring contexts rather than for adaptive problem recommendation or learning path construction.

### 2.3.2 Adaptive Learning Platforms

Several platforms from non-programming domains demonstrate sophisticated adaptive capabilities that serve as reference points for this thesis.

**Duolingo** is the most widely cited example of data-driven adaptive learning at scale. The platform employs spaced repetition --- having recently migrated from its proprietary Half-Life Regression model [10] to FSRS [12] --- for scheduling vocabulary review. Duolingo's adaptation primarily targets retention of discrete vocabulary items, a domain well-suited to flashcard-style spaced repetition. However, Duolingo does not employ explicit knowledge tracing (its learner model is implicit within the recommendation algorithm) and does not use Multi-Armed Bandits for content selection. Its adaptation is limited to within-skill review scheduling rather than cross-skill exploration.

**Khan Academy** uses a mastery-based learning model where students must demonstrate proficiency on a set of practice problems before advancing to the next topic. Khan Academy has recently integrated Khanmigo, an LLM-based tutoring assistant, for providing personalized explanations and hints. However, its mastery model is deterministic (a fixed number of correct answers in a row constitutes mastery) rather than probabilistic, and it does not employ Elo-based difficulty calibration or MAB-based concept selection.

**ALEKS** (Assessment and LEarning in Knowledge Spaces) is among the most academically rigorous adaptive platforms. Based on Knowledge Space Theory [9], ALEKS maintains a detailed map of each student's knowledge state and selects learning activities that are on the boundary of the student's current knowledge space. ALEKS includes periodic reassessment to account for forgetting and supports prerequisite-aware sequencing. However, ALEKS uses a binary (mastered/not mastered) assessment model rather than probabilistic mastery estimation, does not employ Elo-based continuous difficulty calibration, and does not use MAB algorithms for exploration--exploitation optimization in activity selection.

**Carnegie MATHia** (formerly Cognitive Tutor for mathematics) implements BKT for knowledge tracing and model tracing for solution evaluation [8]. It is the platform most similar to the proposed system in its use of explicit knowledge tracing. However, Carnegie MATHia does not incorporate Elo-based difficulty calibration, MAB-based selection, or spaced repetition scheduling.

**Knewton Alta** uses IRT for both learner ability estimation and content difficulty calibration, combined with an adaptive sequencing engine. While IRT and Elo are mathematically related (Section 2.2.3), Knewton Alta's batch-mode IRT requires periodic re-calibration rather than real-time updates, and it does not employ MAB-based exploration or explicit spaced repetition scheduling.

### 2.3.3 Academic Research Systems

Recent academic research has produced prototype adaptive systems that combine subsets of the techniques reviewed in this chapter, though none integrate all five layers.

Clement et al. [44] demonstrated the effectiveness of MAB-based activity selection in an intelligent tutoring system, showing that Thompson Sampling outperforms random selection and expert-designed curricula. However, their system assumed a fixed difficulty model and did not incorporate knowledge tracing or spaced repetition. Edwards et al. [55] developed CodeWorkout, an exercise repository with adaptive selection based on concept mastery, but without Elo calibration, MAB optimization, or retention scheduling. The DKT2 system [35] achieves state-of-the-art knowledge tracing accuracy but is purely a predictive model without a recommendation or scheduling layer.

The KG + RAG + LLM framework by Chen et al. [53] demonstrates the value of combining structured knowledge with generative AI for programming feedback, but does not include knowledge tracing, Elo calibration, or MAB selection. LECTOR [47] combines spaced repetition with LLM-generated content but operates in the vocabulary domain rather than programming and does not include knowledge tracing or adaptive difficulty calibration.

These systems collectively demonstrate the individual merit of each adaptive technique but leave the integration challenge unresolved. The proposed platform addresses this gap by orchestrating all five techniques into a unified pipeline, as discussed in the following section.

## 2.4 Research Gap

### 2.4.1 Synthesis of Adaptive Capabilities

Table 2.2 extends the comparison from Chapter 1 (Table 1.1) with additional detail on the specific algorithms and adaptation mechanisms employed by each platform and research system.

**Table 2.2.** Detailed comparison of adaptive capabilities across existing systems and this thesis.

| System | KT | Difficulty Cal. | Problem Selection | Spaced Rep. | LLM | KG | Domain |
|--------|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| LeetCode | None | Static tiers | Manual | None | Premium | None | Prog. |
| HackerRank | None | Static badges | Curated | None | None | None | Prog. |
| Codeforces | None | Elo (ranking) | Manual | None | None | None | Prog. |
| CodeSignal | None | Elo-IRT | Fixed tests | None | None | None | Prog. |
| CodeWorkout [55] | Mastery | Implicit | Adaptive | None | None | Partial | Prog. |
| Duolingo | Implicit | Implicit | Internal | FSRS | None | None | Lang. |
| Khan Academy | Mastery | Mastery | Sequential | None | Khanmigo | None | Math |
| ALEKS | KST | Implicit | KST-based | Reassess. | None | Partial | Math |
| Carnegie MATHia | BKT | Implicit | Model-trace | None | None | None | Math |
| Knewton Alta | IRT | IRT | Adaptive | None | None | Partial | Multi |
| Clement et al. [44] | None | Fixed | MAB (TS) | None | None | None | General |
| DKT2 [35] | xLSTM+IRT | IRT | None | None | None | None | General |
| Chen et al. [53] | None | None | None | None | KG+RAG+LLM | Yes | Prog. |
| LECTOR [47] | None | None | None | FSRS+LLM | LLM | None | Vocab. |
| **This Thesis** | **BKT** | **Dyn. Elo** | **H-MAB** | **FSRS** | **RAG+LLM** | **Yes** | **Prog.** |

### 2.4.2 Identified Gaps

The literature review reveals three principal gaps:

**Gap 1: No integration of all adaptive layers.** Each reviewed technique addresses a distinct aspect of the adaptive learning problem, but no existing system combines all five. As summarized in Table 2.3, each technique has specific blind spots that other techniques compensate for:

**Table 2.3.** How each adaptive technique addresses limitations of the others.

| Technique | Addresses | Does Not Address |
|-----------|-----------|-----------------|
| BKT (Knowledge Tracing) | What the student knows | What to teach next, how hard to make it |
| Elo (Difficulty Calibration) | How hard each problem is for this student | Knowledge growth, what concept to focus on |
| MAB (Problem Selection) | Optimal concept and problem to recommend | Student knowledge state, forgetting |
| FSRS (Spaced Repetition) | When to review to prevent forgetting | What to teach, how hard |
| KG (Knowledge Graph) | Concept structure and prerequisites | Adaptation to individual differences |
| LLM (Feedback) | Natural language scaffolding | Structured learner modeling |

The integration produces emergent adaptive behavior: BKT mastery estimates feed prerequisite gating in the MAB; Elo ratings constrain problem selection to the ZPD; FSRS review urgency interrupts MAB exploration when concepts are at risk of being forgotten; and the KG provides structural coherence across all layers. No individual technique achieves this coordination alone.

**Gap 2: Spaced repetition has not been applied to programming skills.** FSRS and its predecessors (SM-2, Half-Life Regression) have been developed and validated exclusively in the context of declarative knowledge --- vocabulary, facts, formulas. Programming skills are fundamentally different: they are procedural rather than declarative, require problem-solving rather than recall, and produce rich behavioral signals rather than binary correct/incorrect. The application of FSRS to programming concept retention requires a novel mapping from code submission outcomes to FSRS review ratings, bridging two distinct research traditions that have not previously been connected.

**Gap 3: Programming platforms lack adaptive sophistication.** The most popular programming platforms (LeetCode, HackerRank, Codeforces) offer extensive problem repositories but provide no meaningful adaptation to individual learners. Conversely, the most sophisticated adaptive platforms (ALEKS, Carnegie MATHia, Duolingo) operate in non-programming domains. Programming education sits at the intersection of these two categories: it requires the domain-specific infrastructure of a programming platform (code editor, sandboxed execution, test-case-based evaluation) combined with the adaptive sophistication of a modern learning platform (knowledge tracing, difficulty calibration, intelligent selection, retention scheduling). This intersection is precisely where the proposed system is positioned.

### 2.4.3 How This Thesis Fills the Gap

This thesis addresses all three identified gaps through the design, implementation, and evaluation of an integrated multi-layer adaptive platform for university programming courses:

1. **Integration gap.** The five-layer architecture (Chapter 3) specifies explicit data flows between layers: BKT mastery estimates gate MAB concept eligibility; Elo ratings constrain MAB problem selection to the ZPD; FSRS retrievability scores trigger review priorities that the MAB respects; and the knowledge graph provides the structural backbone that coordinates all layers. Each layer can be independently upgraded (e.g., replacing BKT with DKT2) without disrupting the overall pipeline.

2. **FSRS for programming gap.** The platform applies FSRS to programming concept review scheduling with a novel rating mapping that translates code submission outcomes (correctness, number of attempts, time spent) into FSRS review ratings (1--4). "Reviewing" a concept means solving a new problem tagged with that concept, not simply recalling a definition --- preserving the retrieval practice effect that makes spaced repetition effective.

3. **Programming platform sophistication gap.** The platform combines domain-specific programming infrastructure (React-based code editor, Docker-sandboxed execution, test-case evaluation) with the full adaptive pipeline, delivering a system that is both functionally complete as a programming practice tool and adaptively sophisticated as a personalized learning engine.

The following chapter presents the detailed system design and architecture that realizes this integration.

---

## References (New references introduced in Chapter 2)

[22]   P. De Bra, A. Aerts, B. Berden, B. de Lange, B. Rousseau, T. Santic, D. Smits, and N. Stash, "AHA! The adaptive hypermedia architecture," in *Proc. ACM Conference on Hypertext and Hypermedia*, 2003, pp. 81--84, doi: https://doi.org/10.1145/900051.900068.

[23]   P. Brusilovsky, "KnowledgeTree: A distributed architecture for adaptive e-learning," in *Proc. WWW*, 2004, pp. 104--113, doi: https://doi.org/10.1145/1013367.1013386.

[24]   R. Murphy, L. Gallagher, A. Krumm, J. Mislevy, and A. Hafter, "Research on the use of Khan Academy in schools," *SRI Education*, 2014.

[25]   M. Csikszentmihalyi, *Flow: The Psychology of Optimal Experience*. New York: Harper & Row, 1990.

[26]   N. J. Cepeda, H. Pashler, E. Vul, J. T. Wixted, and D. Rohrer, "Distributed practice in verbal recall tasks: A review and quantitative synthesis," *Psychological Bulletin*, vol. 132, no. 3, pp. 354--380, 2006, doi: https://doi.org/10.1037/0033-2909.132.3.354.

[27]   H. L. Roediger and J. D. Karpicke, "Test-enhanced learning: Taking memory tests improves long-term retention," *Psychological Science*, vol. 17, no. 3, pp. 249--255, 2006, doi: https://doi.org/10.1111/j.1467-9280.2006.01693.x.

[28]   D. Rohrer and K. Taylor, "The shuffling of mathematics problems improves learning," *Instructional Science*, vol. 35, no. 6, pp. 481--498, 2007, doi: https://doi.org/10.1007/s11251-007-9015-8.

[29]   H. Ebbinghaus, *Uber das Gedachtnis: Untersuchungen zur experimentellen Psychologie* [Memory: A Contribution to Experimental Psychology]. Leipzig: Duncker & Humblot, 1885.

[30]   J. T. Wixted and S. K. Carpenter, "The Wickelgren power law and the Ebbinghaus savings function," *Psychological Science*, vol. 18, no. 2, pp. 133--134, 2007, doi: https://doi.org/10.1111/j.1467-9280.2007.01862.x.

[31]   A. Badrinath, F. Wang, and Z. Pardos, "pyBKT: An accessible Python library of Bayesian Knowledge Tracing models," in *Proc. EDM*, 2021.

[32]   C. Piech, J. Bassen, J. Huang, S. Ganguli, M. Sahami, L. J. Guibas, and J. Sohl-Dickstein, "Deep knowledge tracing," in *Advances in Neural Information Processing Systems (NeurIPS)*, vol. 28, 2015.

[33]   C.-K. Yeung and D.-Y. Yeung, "Addressing two problems in deep knowledge tracing via prediction-consistent regularization," in *Proc. ACM L@S*, 2018, pp. 1--10.

[34]   J. Zhang, X. Shi, I. King, and D.-Y. Yeung, "Dynamic key-value memory networks for knowledge tracing," in *Proc. WWW*, 2017, pp. 765--774.

[35]   T. N. Doan and Y. Sahebi, "DKT2: Deep knowledge tracing with xLSTM and IRT integration," in *Proc. ECML-PKDD*, 2025, doi: https://doi.org/10.1007/978-3-032-06109-6_14.

[36]   J. Leinonen et al., "srcML-DKT: Source code-aware deep knowledge tracing for programming exercises," in *Proc. Educational Data Mining (EDM)*, 2025.

[37]   Z. Li, X. Wang, and Y. Chen, "UKT: Uncertainty-aware knowledge tracing," in *Proc. AAAI Conference on Artificial Intelligence*, 2025, doi: https://doi.org/10.1609/aaai.v39i1.35007.

[38]   R. Pelanek and J. Rihak, "Experimental analysis of the Elo rating system for adaptive practice of programming exercises," *ACM Transactions on Computing Education (TOCE)*, vol. 22, no. 3, pp. 1--22, 2022, doi: https://doi.org/10.1145/3511886.

[39]   G. Rasch, *Probabilistic Models for Some Intelligence and Attainment Tests*. Copenhagen: Danish Institute for Educational Research, 1960.

[40]   S. Klinkenberg, M. Straatemeier, and H. L. J. van der Maas, "Adaptive K-factor Elo rating for personalized education," *User Modeling and User-Adapted Interaction*, 2025, doi: https://doi.org/10.1007/s11257-025-09439-z.

[41]   R. Pelanek, "Multidimensional Elo ratings for concept-specific ability estimation," in *Proc. Educational Data Mining (EDM)*, 2025.

[42]   H. Robbins, "Some aspects of the sequential design of experiments," *Bulletin of the American Mathematical Society*, vol. 58, no. 5, pp. 527--535, 1952.

[43]   B. Castleman et al., "Hierarchical multi-armed bandit framework for adaptive learning," 2024, arXiv: 2408.07208.

[44]   B. Clement, D. Roy, P.-Y. Oudeyer, and M. Lopes, "Multi-armed bandits for intelligent tutoring systems," *Journal of Educational Data Mining*, vol. 7, no. 2, pp. 20--48, 2015.

[45]   Z. Shen et al., "Multi-armed bandits with user abandonment," in *Advances in Neural Information Processing Systems (NeurIPS)*, 2024.

[46]   P. A. Wozniak, "Application of a computer system in the optimization of the repetition spacing algorithm in the process of learning," M.S. thesis, University of Technology, Poznan, Poland, 1990.

[47]   Y. Zhang, J. Wang, and L. Sun, "LECTOR: LLM-enhanced concept-based test-oriented repetition," 2025, arXiv: 2508.03275.

[48]   X. Chen, D. Shi, and H. Zhao, "Automatic concept extraction for building knowledge graphs in education," *Journal of Educational Data Mining*, vol. 16, no. 1, 2024, doi: https://doi.org/10.5281/jedm.737.

[49]   L. Pan, C. Li, J. Li, and J. Tang, "Prerequisite-enhanced category-aware graph neural networks for educational recommendation," *ACM Transactions on Knowledge Discovery from Data*, vol. 18, no. 6, 2024, doi: https://doi.org/10.1145/3643644.

[50]   Y. Liu, H. Wang, and Z. Zhang, "Graph neural network-based learning resource recommendation on tripartite graphs," *Interactive Learning Environments*, 2025, doi: https://doi.org/10.1177/14727978251374326.

[51]   J. Gu, Y. Li, and X. Chen, "Graph attention networks with deep reinforcement learning for personalized learning path generation," *Interactive Learning Environments*, 2025, doi: https://doi.org/10.1177/14727978241313260.

[52]   M. Al-Hossami, R. Bunescu, and C. Belford, "PyTutor: A ChatGPT-powered intelligent tutoring system for Python programming," *International Journal of Artificial Intelligence in Education*, 2024, doi: https://doi.org/10.1016/j.caeai.2024.100276.

[53]   X. Chen, M. Zhang, and Y. Wang, "Hybrid knowledge graph and retrieval-augmented generation for adaptive intelligent tutoring," *Computers and Education: Artificial Intelligence*, 2025, doi: https://doi.org/10.1016/j.caeai.2025.100276.

[54]   L. Wang, H. Li, and J. Zhou, "Multimodal knowledge graph-enhanced retrieval-augmented generation for intelligent tutoring systems," *Frontiers in Computer Science*, vol. 8, 2026, doi: https://doi.org/10.3389/fcomp.2026.1777749.

[55]   S. H. Edwards, Z. Li, and C. Peng, "CodeWorkout: Short programming exercises with built-in data collection," in *Proc. ITiCSE*, 2020, pp. 188--193.
