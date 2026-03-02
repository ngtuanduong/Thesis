export interface User {
  id: string;
  email: string;
  name: string;
  role: 'STUDENT' | 'INSTRUCTOR' | 'ADMIN';
}

export interface Course {
  id: string;
  title: string;
  description?: string;
  instructorId: string;
  instructor?: { id: string; name: string };
}

export interface Problem {
  id: string;
  title: string;
  description: string;
  difficulty: 'EASY' | 'MEDIUM' | 'HARD';
  tags: string[];
  courseId?: string;
  testCases?: TestCase[];
}

export interface TestCase {
  id: string;
  input: string;
  expected: string;
  isHidden: boolean;
}

export interface Submission {
  id: string;
  userId: string;
  problemId: string;
  code: string;
  language: string;
  status: 'PENDING' | 'RUNNING' | 'ACCEPTED' | 'WRONG_ANSWER' | 'TIME_LIMIT' | 'RUNTIME_ERROR' | 'COMPILATION_ERROR';
  output?: string;
  runtime?: number;
  memory?: number;
  createdAt: string;
}

export interface SkillEmbedding {
  id: string;
  userId: string;
  skillName: string;
  score: number;
}

// === Adaptive Learning Types ===

export interface ConceptState {
  concept_id: number;
  concept_name: string;
  display_name: string;
  topic_group: string;
  difficulty_tier: number;
  p_mastery: number;
  n_attempts: number;
  n_correct: number;
  status: 'not_started' | 'learning' | 'mastered';
  elo_rating?: number;
}

export interface KnowledgeGraphNode {
  id: number;
  name: string;
  display_name: string;
  topic_group: string;
  difficulty_tier: number;
  p_mastery: number;
  status: 'not_started' | 'learning' | 'mastered';
}

export interface KnowledgeGraphEdge {
  from_id: number;
  to_id: number;
}

export interface KnowledgeStateResponse {
  student_id: string;
  concepts: ConceptState[];
  knowledge_graph: {
    nodes: KnowledgeGraphNode[];
    edges: KnowledgeGraphEdge[];
  };
  summary: {
    total_concepts: number;
    mastered: number;
    learning: number;
    not_started: number;
    overall_mastery: number;
  };
}

export interface AdaptiveRecommendation {
  problem_id: string;
  title: string;
  difficulty: string;
  concept_name: string;
  concept_display_name: string;
  score: number;
  reason: string;
  elo_gap?: number;
}

export interface AdaptiveRecommendationsResponse {
  student_id: string;
  recommendations: AdaptiveRecommendation[];
  knowledge_summary: {
    overall_mastery: number;
    weakest_concepts: string[];
    strongest_concepts: string[];
  } | null;
}

export interface ReviewItem {
  concept_id: number;
  concept_name: string;
  display_name: string;
  retrievability: number;
  due_date: string;
  stability: number;
  difficulty: number;
  state: string;
}

export interface ReviewQueueResponse {
  student_id: string;
  due_now: ReviewItem[];
  upcoming: ReviewItem[];
}

export interface HintResponse {
  hint: string | null;
  hint_level: number;
  concepts_referenced: string[];
  error: string | null;
}

export interface Concept {
  id: number;
  name: string;
  displayName: string;
  description?: string;
  topicGroup?: string;
  difficultyTier: number;
  prerequisites?: { id: number; fromConceptId: number; toConceptId: number }[];
  dependents?: { id: number; fromConceptId: number; toConceptId: number }[];
  problemConcepts?: { problemId: string; isPrimary: boolean }[];
}
