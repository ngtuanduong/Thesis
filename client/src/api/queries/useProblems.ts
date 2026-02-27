import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import api from '../axios';
import type { Problem } from '../../types';

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
