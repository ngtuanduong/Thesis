import { useQuery, useMutation, useQueryClient, keepPreviousData } from '@tanstack/react-query';
import api from '../axios';
import type { Problem, PaginatedResponse } from '../../types';

export function useProblems(courseId?: string) {
  return useQuery({
    queryKey: ['problems', courseId],
    queryFn: async () => {
      const params = courseId ? { courseId } : {};
      const res = await api.get<Problem[]>('/problems', { params });
      return res.data;
    },
  });
}

export function useProblemsPaginated(params: {
  page: number;
  pageSize: number;
  search?: string;
  difficulty?: string[];
  concepts?: number[];
  courseId?: string;
}) {
  return useQuery({
    queryKey: ['problems-paginated', params],
    queryFn: async () => {
      const query: Record<string, string> = {
        page: String(params.page),
        pageSize: String(params.pageSize),
      };
      if (params.search) query.search = params.search;
      if (params.difficulty?.length) query.difficulty = params.difficulty.join(',');
      if (params.concepts?.length) query.concepts = params.concepts.join(',');
      if (params.courseId) query.courseId = params.courseId;
      const res = await api.get<PaginatedResponse<Problem>>('/problems/paginated', { params: query });
      return res.data;
    },
    placeholderData: keepPreviousData,
  });
}

export function useProblem(id: string) {
  return useQuery({
    queryKey: ['problems', id],
    queryFn: async () => {
      const res = await api.get<Problem>(`/problems/${id}`);
      return res.data;
    },
    enabled: !!id,
  });
}

export function useSubmitCode() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (data: { problemId: string; code: string; language: string }) => {
      const res = await api.post('/submissions', data);
      return res.data;
    },
    onSuccess: (_data, variables) => {
      queryClient.invalidateQueries({ queryKey: ['submissions', variables.problemId] });
    },
  });
}
