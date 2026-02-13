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
