import { useQuery } from '@tanstack/react-query';
import api from '../axios';

interface DashboardStats {
  problemsSolved: number;
  totalSubmissions: number;
  enrolledCourses: number;
  currentStreak: number;
}

interface Submission {
  id: string;
  problemId: string;
  status: string;
  runtime: number;
  createdAt: string;
  problem: {
    id: string;
    title: string;
    difficulty: string;
  };
}

interface Recommendation {
  id: string;
  title: string;
  difficulty: string;
  tags: string[];
}

export function useDashboardStats() {
  return useQuery({
    queryKey: ['dashboard-stats'],
    queryFn: async () => {
      // Fetch all required data
      const [submissions, courses] = await Promise.all([
        api.get<Submission[]>('/submissions/my'),
        api.get('/courses'),
      ]);

      // Calculate statistics
      const totalSubmissions = submissions.data.length;
      const problemsSolved = new Set(
        submissions.data
          .filter((s) => s.status === 'ACCEPTED')
          .map((s) => s.problemId)
      ).size;

      // Get enrolled courses (filter courses where user is enrolled)
      const enrolledCourses = courses.data.filter((c: any) =>
        c.enrollments?.some((e: any) => e.userId)
      ).length;

      // Calculate streak (simplified - days with at least one submission)
      const submissionDates = submissions.data.map((s) =>
        new Date(s.createdAt).toDateString()
      );
      const uniqueDates = new Set(submissionDates);
      const currentStreak = uniqueDates.size; // Simplified streak calculation

      return {
        problemsSolved,
        totalSubmissions,
        enrolledCourses,
        currentStreak,
      } as DashboardStats;
    },
  });
}

export function useRecentSubmissions(limit: number = 5) {
  return useQuery({
    queryKey: ['recent-submissions', limit],
    queryFn: async () => {
      const res = await api.get<Submission[]>('/submissions/my');
      return res.data.slice(0, limit);
    },
  });
}

export function useRecommendations(limit: number = 5) {
  return useQuery({
    queryKey: ['recommendations', limit],
    queryFn: async () => {
      const res = await api.get<Recommendation[]>('/recommendations', {
        params: { limit },
      });
      return res.data;
    },
  });
}
