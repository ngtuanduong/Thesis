import { useQuery } from '@tanstack/react-query';
import api from '../axios';
import type { Submission } from '../../types';

export function useProblemSubmissions(problemId: string) {
  return useQuery({
    queryKey: ['submissions', 'problem', problemId],
    queryFn: async () => {
      const res = await api.get<Submission[]>(`/submissions/problem/${problemId}`);
      return res.data;
    },
    enabled: !!problemId,
  });
}

export function useSubmission(
  id: string | undefined,
  options?: { refetchInterval?: number | false },
) {
  return useQuery({
    queryKey: ['submissions', id],
    queryFn: async () => {
      const res = await api.get<Submission>(`/submissions/${id}`);
      return res.data;
    },
    enabled: !!id,
    refetchInterval: options?.refetchInterval,
  });
}
