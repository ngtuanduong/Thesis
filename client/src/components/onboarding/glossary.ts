export interface GlossaryEntry {
  short: string;
  detail: string;
}

export const GLOSSARY: Record<string, GlossaryEntry> = {
  mastery: {
    short: 'How well you know a concept',
    detail:
      'Estimated using a probabilistic model that updates after every submission. It accounts for lucky guesses and careless mistakes to give an accurate picture of your true understanding.',
  },
  retrievability: {
    short: 'How well you can recall this concept right now',
    detail:
      'A percentage (0–100%) that naturally decays over time. When it drops below a threshold, the system schedules a review to refresh your memory before you forget.',
  },
  stability: {
    short: 'How resistant this memory is to forgetting',
    detail:
      'Measured in days. Higher stability means the memory fades slower. Each successful review increases stability, so reviews become less frequent over time.',
  },
  elo_rating: {
    short: 'Your skill level score',
    detail:
      'Similar to chess Elo ratings — solving a hard problem raises your score, struggling with an easy one lowers it. Used to match you with appropriately challenging problems.',
  },
  difficulty_tier: {
    short: 'Concept complexity level (1 = basic, higher = advanced)',
    detail:
      'Concepts are organized into tiers based on prerequisite relationships. Master lower tiers before tackling higher ones for the best learning path.',
  },
  spaced_repetition: {
    short: 'Reviewing at optimal intervals to strengthen memory',
    detail:
      'The system schedules reviews just before you are likely to forget, making your study time more efficient. Intervals grow longer as your memory strengthens.',
  },
  review_queue: {
    short: 'Concepts that need practice to stay in memory',
    detail:
      'When your memory of a concept starts fading, it appears here. Regular reviews keep your knowledge strong and prevent forgetting.',
  },
  knowledge_map: {
    short: 'Visual graph of all concepts and how they connect',
    detail:
      'Each node is a concept, colored by topic and showing your mastery level. Arrows show prerequisites — master the basics before advancing to connected topics.',
  },
  adaptive_engine: {
    short: 'The AI that picks your next problem',
    detail:
      'Combines your mastery level, skill rating, and review schedule to recommend problems that are challenging but achievable — keeping you in the optimal learning zone.',
  },
};
