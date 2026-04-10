import { useQuery, useMutation } from '@tanstack/react-query';
import api from '../axios';
import type {
  AdaptiveRecommendationsResponse,
  KnowledgeStateResponse,
  ReviewQueueResponse,
  HintResponse,
  Concept,
} from '../../types';

export function useKnowledgeState(userId?: string) {
  return useQuery({
    queryKey: ['knowledge-state', userId],
    queryFn: async () => {
      const res = await api.get<KnowledgeStateResponse>(
        `/adaptive/knowledge-state/${userId}`,
      );
      return res.data;
    },
    enabled: !!userId,
  });
}

export function useAdaptiveRecommendations(userId?: string, limit = 5) {
  return useQuery({
    queryKey: ['adaptive-recommendations', userId, limit],
    queryFn: async () => {
      const res = await api.get<AdaptiveRecommendationsResponse>(
        `/adaptive/recommend/${userId}`,
        { params: { limit } },
      );
      return res.data;
    },
    enabled: !!userId,
  });
}

export function useReviewQueue(userId?: string) {
  return useQuery({
    queryKey: ['review-queue', userId],
    queryFn: async () => {
      const res = await api.get<ReviewQueueResponse>(
        `/adaptive/review-queue/${userId}`,
      );
      return res.data;
    },
    enabled: !!userId,
  });
}

export function useConcepts() {
  return useQuery({
    queryKey: ['concepts'],
    queryFn: async () => {
      const res = await api.get<Concept[]>('/concepts');
      return res.data;
    },
  });
}

export function useKnowledgeGraph() {
  return useQuery({
    queryKey: ['knowledge-graph'],
    queryFn: async () => {
      const res = await api.get<{
        concepts: Concept[];
        edges: { id: number; fromConceptId: number; toConceptId: number }[];
      }>('/concepts/graph');
      return res.data;
    },
  });
}

export function usePracticeForConcept() {
  return useMutation({
    mutationFn: async ({ userId, conceptId }: { userId: string; conceptId: number }) => {
      const res = await api.get<{ problem_id: string | null; title: string | null }>(
        `/adaptive/practice/${userId}/${conceptId}`,
      );
      return res.data;
    },
  });
}

export function useGenerateHint() {
  return useMutation({
    mutationFn: async (data: {
      studentId: string;
      problemId: string;
      code: string;
      errorMessage?: string;
      hintLevel?: number;
    }) => {
      const res = await api.post<HintResponse>('/adaptive/hints', data);
      return res.data;
    },
  });
}
