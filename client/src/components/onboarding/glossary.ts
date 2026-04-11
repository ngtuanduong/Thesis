export interface ScaleStop {
  value: number;
  label: string;
  color: string;
}

export interface GlossaryEntry {
  short: string;
  detail: string;
  category: 'memory' | 'skill' | 'system' | 'learning';
  examples?: string[];
  whereYouSeeIt?: string[];
  relatedTerms?: string[];
  scale?: {
    unit: string;
    stops: ScaleStop[];
  };
}

export const CATEGORY_LABELS: Record<string, { label: string; color: string }> = {
  memory: { label: 'Memory & Retention', color: '#1890ff' },
  skill: { label: 'Skill & Difficulty', color: '#52c41a' },
  system: { label: 'System & AI', color: '#722ed1' },
  learning: { label: 'Learning Progress', color: '#fa8c16' },
};

export const GLOSSARY: Record<string, GlossaryEntry> = {
  mastery: {
    short: 'How well you know a concept',
    detail:
      'Mastery is a probability (0\u2013100%) estimated by a Bayesian Knowledge Tracing (BKT) model. It updates after every submission, accounting for lucky guesses and careless mistakes. A mastery of 85%+ means the system considers the concept learned. Below 10% means you haven\'t started yet.',
    category: 'learning',
    examples: [
      '12% \u2014 You\'ve just begun this concept. Keep practicing.',
      '55% \u2014 Making progress but not yet solid. A few more successful attempts should push you higher.',
      '85%+ \u2014 Mastered! The system is confident you understand this concept.',
    ],
    scale: {
      unit: '%',
      stops: [
        { value: 0, label: 'Not Started', color: '#d9d9d9' },
        { value: 10, label: 'Beginner', color: '#f5222d' },
        { value: 55, label: 'Learning', color: '#fa8c16' },
        { value: 85, label: 'Mastered', color: '#52c41a' },
        { value: 100, label: 'Perfect', color: '#237804' },
      ],
    },
    whereYouSeeIt: [
      'Dashboard \u203a Knowledge Mastery card',
      'Knowledge Map \u203a node fill opacity',
      'Profile \u203a concept mastery list',
      'Review Queue \u203a All Concepts tab',
    ],
    relatedTerms: ['retrievability', 'bkt', 'knowledge_map'],
  },
  retrievability: {
    short: 'How well you can recall this concept right now',
    detail:
      'Retrievability (R) is a percentage (0\u2013100%) that represents the probability you can successfully recall a concept at this moment. It starts at 100% right after a review and naturally decays over time following a power-law forgetting curve: R(t) = (1 + t/(9\u00d7S))\u207b\u00b9, where t is elapsed days and S is stability. When R drops below 90%, the system schedules a review.',
    category: 'memory',
    examples: [
      '95% \u2014 Strong memory. Reviewed recently, no action needed.',
      '75% \u2014 Fading. You can probably still recall it, but a review soon would help.',
      '45% \u2014 Critical. High chance of forgetting. Review immediately.',
    ],
    scale: {
      unit: '%',
      stops: [
        { value: 0, label: 'Forgotten', color: '#434343' },
        { value: 50, label: 'Critical', color: '#f5222d' },
        { value: 70, label: 'Fading', color: '#fa8c16' },
        { value: 90, label: 'Good', color: '#1890ff' },
        { value: 100, label: 'Strong', color: '#52c41a' },
      ],
    },
    whereYouSeeIt: [
      'Review Queue \u203a Memory column & circular indicator',
      'Review Queue \u203a Due Now list (urgency)',
      'Knowledge Map \u203a node opacity on hover info',
    ],
    relatedTerms: ['stability', 'memory_status', 'spaced_repetition'],
  },
  stability: {
    short: 'How resistant this memory is to forgetting (in days)',
    detail:
      'Stability (S) is measured in days and represents how slowly your memory of a concept fades. Technically, it is the number of days after which retrievability drops to approximately 90%. A higher stability means you can go longer between reviews. Each successful review increases stability, so over time, reviews become less frequent.',
    category: 'memory',
    examples: [
      '0.4d \u2014 Very fragile. You\'ll need to review again within hours.',
      '1.2d \u2014 Just learned. Memory lasts about a day before fading below 90%.',
      '5.0d \u2014 Moderate retention. You can wait about 5 days before needing a review.',
      '15.5d \u2014 Strong retention. The concept is well-consolidated. Next review in ~2 weeks.',
      '60.0d \u2014 Very stable. This knowledge is deeply embedded. Reviews every 2 months.',
    ],
    scale: {
      unit: 'days',
      stops: [
        { value: 0, label: '< 1d Fragile', color: '#f5222d' },
        { value: 15, label: '1d New', color: '#fa8c16' },
        { value: 35, label: '5d Moderate', color: '#1890ff' },
        { value: 65, label: '15d Strong', color: '#52c41a' },
        { value: 100, label: '60d+ Deep', color: '#237804' },
      ],
    },
    whereYouSeeIt: [
      'Review Queue \u203a Stability column (e.g. "5.2d")',
      'Review Queue \u203a All Concepts tab',
    ],
    relatedTerms: ['retrievability', 'difficulty_fsrs', 'spaced_repetition'],
  },
  difficulty_fsrs: {
    short: 'How hard this concept is for you personally (FSRS)',
    detail:
      'FSRS difficulty is a value from 1.0 to 10.0, personalized per student per concept. It represents how challenging the concept is for you specifically, not an absolute difficulty. Lower values mean the concept is easier for you (stability grows faster); higher values mean it\'s harder (more reviews needed). It adjusts after every review based on your performance.',
    category: 'memory',
    examples: [
      '2.5 \u2014 Relatively easy for you. Stability grows quickly with each review.',
      '5.0 \u2014 Average difficulty. Standard review schedule.',
      '8.0 \u2014 This concept is challenging for you. Expect more frequent reviews.',
    ],
    scale: {
      unit: '',
      stops: [
        { value: 0, label: '1.0 Easy', color: '#52c41a' },
        { value: 25, label: '3.0', color: '#a0d911' },
        { value: 50, label: '5.0 Avg', color: '#fa8c16' },
        { value: 75, label: '7.0', color: '#fa541c' },
        { value: 100, label: '10.0 Hard', color: '#f5222d' },
      ],
    },
    whereYouSeeIt: [
      'Review Queue \u203a All Concepts tab (internal metric)',
    ],
    relatedTerms: ['stability', 'spaced_repetition'],
  },
  elo_rating: {
    short: 'Your skill level score, like chess ratings',
    detail:
      'Your Elo rating starts at 1200 and adjusts after each submission. Solving a problem correctly raises your rating; failing lowers it. The amount of change depends on the difficulty gap\u2014beating a hard problem earns more points than an easy one. Problems also have Elo ratings, so the system can match you with challenges at the right level.',
    category: 'skill',
    examples: [
      '1050 \u2014 Below average. You\'re tackling foundational problems.',
      '1200 \u2014 Starting point. Average difficulty level.',
      '1400 \u2014 Above average. You\'re comfortable with medium-hard problems.',
      '1600+ \u2014 Advanced. You can handle most hard problems successfully.',
    ],
    scale: {
      unit: 'rating',
      stops: [
        { value: 0, label: '800 Beginner', color: '#d9d9d9' },
        { value: 25, label: '1050', color: '#fa8c16' },
        { value: 50, label: '1200 Avg', color: '#1890ff' },
        { value: 75, label: '1400', color: '#52c41a' },
        { value: 100, label: '1600+ Pro', color: '#237804' },
      ],
    },
    whereYouSeeIt: [
      'Profile \u203a Skill Rating card',
      'Dashboard \u203a Elo trajectory chart',
    ],
    relatedTerms: ['difficulty_tier', 'adaptive_engine'],
  },
  difficulty_tier: {
    short: 'Concept complexity level (1 = basic, higher = advanced)',
    detail:
      'Concepts are organized into tiers based on prerequisite relationships in the knowledge graph. Tier 1 concepts (e.g., variables, basic I/O) have no prerequisites. Higher tiers build on lower ones. The system recommends mastering lower tiers before advancing, ensuring a solid foundation.',
    category: 'skill',
    examples: [
      'Tier 1 \u2014 Foundations: Variables, Basic I/O, Data Types',
      'Tier 2 \u2014 Control Flow: Conditions, Loops, Functions',
      'Tier 3 \u2014 Data Structures: Arrays, Strings, Recursion',
      'Tier 4+ \u2014 Advanced: Sorting, Dynamic Programming, Graphs',
    ],
    whereYouSeeIt: [
      'Knowledge Map \u203a vertical layout (top = Tier 1, bottom = higher tiers)',
      'Problems \u203a concept tags on each problem',
    ],
    relatedTerms: ['elo_rating', 'knowledge_map'],
  },
  spaced_repetition: {
    short: 'Reviewing at optimal intervals to strengthen memory',
    detail:
      'Spaced repetition is a scientifically-proven learning technique where reviews are scheduled just before you\'re likely to forget. This platform uses the FSRS-5 algorithm (Free Spaced Repetition Scheduler) with 19 optimized parameters to calculate the ideal review time for each concept. After each successful review, the interval grows longer; after a lapse, it shortens.',
    category: 'memory',
    examples: [
      'Day 1: Learn "Loops" \u2192 First review scheduled for tomorrow (stability = 1d)',
      'Day 2: Review successfully \u2192 Next review in 3 days (stability grew to 3d)',
      'Day 5: Review successfully \u2192 Next review in 8 days (stability grew to 8d)',
      'Day 13: Forgot (lapse) \u2192 Stability resets to ~1d, card enters "Relearning" state',
    ],
    whereYouSeeIt: [
      'Review Queue \u203a entire page is driven by spaced repetition',
      'Review Queue \u203a Upcoming Reviews section',
    ],
    relatedTerms: ['stability', 'retrievability', 'fsrs_state', 'review_queue'],
  },
  review_queue: {
    short: 'Concepts that need practice to stay in memory',
    detail:
      'The review queue shows all concepts where your memory has faded enough to need reinforcement. "Due Now" items have retrievability below 90%\u2014the sooner you review them, the less effort it takes to restore your memory. "Upcoming" items are due within 3 days.',
    category: 'memory',
    whereYouSeeIt: [
      'Sidebar \u203a Review Queue page',
      'Dashboard \u203a Reviews Due card',
    ],
    relatedTerms: ['spaced_repetition', 'retrievability', 'memory_status'],
  },
  fsrs_state: {
    short: 'The current learning phase of a concept in FSRS',
    detail:
      'Each concept card goes through lifecycle states that determine how the FSRS algorithm schedules reviews. The state changes based on your performance during reviews.',
    category: 'memory',
    examples: [
      'NEW \u2014 Never reviewed. The card is waiting for your first attempt.',
      'LEARNING \u2014 First encounter. You rated it "Hard" or "Again" on initial review. Short intervals.',
      'REVIEW \u2014 Normal spaced repetition. Intervals grow with each success.',
      'RELEARNING \u2014 You forgot (lapsed). The card re-enters short intervals until you recall it again.',
    ],
    whereYouSeeIt: [
      'Review Queue \u203a State column tag (LEARNING / REVIEW / RELEARNING)',
      'Review Queue \u203a All Concepts tab \u203a State filter',
    ],
    relatedTerms: ['spaced_repetition', 'lapses', 'reps'],
  },
  memory_status: {
    short: 'Visual indicator of how strong your memory is right now',
    detail:
      'Memory status is derived from your current retrievability and uses color-coded labels to help you prioritize reviews at a glance.',
    category: 'memory',
    examples: [
      'Strong (green, \u226590%) \u2014 You remember this well. No review needed yet.',
      'Good (blue, 70\u201389%) \u2014 Solid but starting to fade. Review within a few days.',
      'Fading (orange, 50\u201369%) \u2014 Memory is weakening noticeably. Review soon.',
      'Critical (red, <50%) \u2014 High risk of forgetting. Review immediately.',
    ],
    whereYouSeeIt: [
      'Review Queue \u203a Memory column color tag',
      'Review Queue \u203a All Concepts tab \u203a Memory filter',
    ],
    relatedTerms: ['retrievability'],
  },
  knowledge_map: {
    short: 'Visual graph of all concepts and how they connect',
    detail:
      'The knowledge map displays concepts as nodes in a directed acyclic graph (DAG). Arrows indicate prerequisite relationships\u2014you should master a prerequisite before moving to dependent concepts. Node colors represent topic groups, and the fill opacity reflects your mastery level. Hover over a node to see its connections.',
    category: 'learning',
    whereYouSeeIt: [
      'Sidebar \u203a Knowledge Map page',
    ],
    relatedTerms: ['mastery', 'difficulty_tier'],
  },
  adaptive_engine: {
    short: 'The AI that picks your next problem',
    detail:
      'The adaptive engine is a 4-layer system that works together to personalize your learning experience. Layer 1 (BKT) tracks concept mastery. Layer 2 (Elo) matches problem difficulty to your skill. Layer 3 (MAB/Thompson Sampling) explores which concepts benefit you most. Layer 4 (FSRS) schedules reviews at optimal times.',
    category: 'system',
    examples: [
      'Layer 1 \u2014 BKT: "You have 72% mastery on Loops"',
      'Layer 2 \u2014 Elo: "Your rating is 1350, this problem is rated 1400\u2014a good challenge"',
      'Layer 3 \u2014 MAB: "Practicing Recursion gave the best learning gains recently"',
      'Layer 4 \u2014 FSRS: "Variables is due for review in 2 days"',
    ],
    whereYouSeeIt: [
      'Problems \u203a Recommended For You section',
      'Dashboard \u203a Recommended Problems card',
    ],
    relatedTerms: ['bkt', 'elo_rating', 'thompson_sampling', 'spaced_repetition'],
  },
  bkt: {
    short: 'Bayesian Knowledge Tracing \u2014 the mastery estimation model',
    detail:
      'BKT is a Hidden Markov Model that estimates the probability you\'ve truly learned a concept. It uses four parameters per concept: P(L\u2080) initial learning probability, P(T) transition probability per attempt, P(G) guess probability, and P(S) slip probability. After each submission, it updates P(mastery) using Bayesian inference.',
    category: 'system',
    whereYouSeeIt: [
      'Indirectly via the mastery percentage shown throughout the app',
    ],
    relatedTerms: ['mastery', 'adaptive_engine'],
  },
  thompson_sampling: {
    short: 'Algorithm that balances exploring new concepts vs. exploiting known ones',
    detail:
      'Thompson Sampling is a Multi-Armed Bandit strategy used to decide which concept to recommend for practice. It maintains a Beta distribution for each concept, modeling the expected learning reward. It naturally balances "exploration" (trying less-practiced concepts) with "exploitation" (focusing on concepts that give the best learning gains).',
    category: 'system',
    whereYouSeeIt: [
      'Indirectly via the Recommended For You section on Problems page',
    ],
    relatedTerms: ['adaptive_engine'],
  },
  reps: {
    short: 'Total number of reviews for a concept',
    detail:
      'The "reps" counter increments each time you review a concept (regardless of outcome). It helps track how much effort you\'ve invested in retaining each concept. More reps combined with high stability indicates deep, durable knowledge.',
    category: 'learning',
    whereYouSeeIt: [
      'Review Queue \u203a All Concepts tab \u203a Reviews column',
    ],
    relatedTerms: ['lapses', 'spaced_repetition'],
  },
  lapses: {
    short: 'Number of times you forgot a concept during review',
    detail:
      'A lapse occurs when you fail to recall a concept during a scheduled review (rated "Again" in FSRS). The card enters the "Relearning" state and the stability is significantly reduced. Frequent lapses on a concept suggest it may need a different learning approach or more foundational prerequisite work.',
    category: 'learning',
    examples: [
      '0 lapses \u2014 Perfect retention history. You\'ve never forgotten this concept.',
      '1\u20132 lapses \u2014 Normal. Some concepts take a couple of tries to stick.',
      '3+ lapses \u2014 This concept is a "leech." Consider reviewing prerequisites or trying different practice problems.',
    ],
    whereYouSeeIt: [
      'Review Queue \u203a All Concepts tab \u203a Lapses column (red if > 0)',
    ],
    relatedTerms: ['reps', 'fsrs_state', 'spaced_repetition'],
  },
};
