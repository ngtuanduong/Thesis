import { useQuery, keepPreviousData } from '@tanstack/react-query';
import api from '../axios';
import type { PaginatedResponse } from '../../types';

interface StrugglingStudent {
  id: string;
  email: string;
  name: string;
  averageMastery: number;
}

interface InstructorDashboardData {
  enrolledCount: number;
  totalSubmissions: number;
  averageMastery: number;
  strugglingStudents: StrugglingStudent[];
}

interface InstructorStudent {
  id: string;
  email: string;
  name: string;
  role: string;
  enrolledAt: string;
  submissionCount: number;
  averageMastery: number;
  latestEloRating: number;
}

interface ProblemConcept {
  id: number;
  name: string;
  displayName: string;
  isPrimary: boolean;
}

interface InstructorProblem {
  id: string;
  title: string;
  description: string;
  difficulty: 'EASY' | 'MEDIUM' | 'HARD';
  courseId: string;
  createdAt: string;
  submissionCount: number;
  acceptedCount: number;
  acceptanceRate: number;
  testCaseCount: number;
  concepts: ProblemConcept[];
}

interface CourseItem {
  id: string;
  title: string;
  description?: string;
  instructorId: string;
}

export function useInstructorDashboard(courseId: string) {
  return useQuery({
    queryKey: ['instructor-dashboard', courseId],
    queryFn: async () => {
      const res = await api.get<InstructorDashboardData>(
        `/instructor/dashboard/${courseId}`,
      );
      return res.data;
    },
    enabled: !!courseId,
  });
}

export function useInstructorStudents(courseId: string) {
  return useQuery({
    queryKey: ['instructor-students', courseId],
    queryFn: async () => {
      const res = await api.get<InstructorStudent[]>(
        `/instructor/students/${courseId}`,
      );
      return res.data;
    },
    enabled: !!courseId,
  });
}

export function useInstructorProblems(params: {
  page: number;
  pageSize: number;
  search?: string;
}) {
  return useQuery({
    queryKey: ['instructor-problems', params],
    queryFn: async () => {
      const query: Record<string, string> = {
        page: String(params.page),
        pageSize: String(params.pageSize),
      };
      if (params.search) query.search = params.search;
      const res = await api.get<PaginatedResponse<InstructorProblem>>(
        '/instructor/problems/manage',
        { params: query },
      );
      return res.data;
    },
    placeholderData: keepPreviousData,
  });
}

export function useCourses() {
  return useQuery({
    queryKey: ['courses'],
    queryFn: async () => {
      const res = await api.get<CourseItem[]>('/courses');
      return res.data;
    },
  });
}
