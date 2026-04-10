import { useMutation, useQueryClient } from '@tanstack/react-query';
import api from '../axios';
import type { Problem } from '../../types';

export { useProblemsPaginated } from './useProblems';
export { useConcepts } from './useAdaptive';

interface CreateProblemData {
  title: string;
  description: string;
  difficulty: 'EASY' | 'MEDIUM' | 'HARD';
  courseId?: string;
  conceptIds?: number[];
  starterCode?: string;
  testCases?: { input: string; expected: string; isHidden: boolean }[];
}

interface UpdateProblemData extends CreateProblemData {
  id: string;
}

export function useCreateProblem() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (data: CreateProblemData) => {
      const res = await api.post<Problem>('/problems', data);
      return res.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['problems'] });
      queryClient.invalidateQueries({ queryKey: ['problems-paginated'] });
      queryClient.invalidateQueries({ queryKey: ['instructor-problems'] });
    },
  });
}

export function useUpdateProblem() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ id, ...data }: UpdateProblemData) => {
      const res = await api.put<Problem>(`/problems/${id}`, data);
      return res.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['problems'] });
      queryClient.invalidateQueries({ queryKey: ['problems-paginated'] });
      queryClient.invalidateQueries({ queryKey: ['instructor-problems'] });
    },
  });
}

export function useDeleteProblem() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (id: string) => {
      const res = await api.delete(`/problems/${id}`);
      return res.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['problems'] });
      queryClient.invalidateQueries({ queryKey: ['problems-paginated'] });
      queryClient.invalidateQueries({ queryKey: ['instructor-problems'] });
    },
  });
}
