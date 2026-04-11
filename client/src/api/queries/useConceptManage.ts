import { useMutation, useQueryClient } from '@tanstack/react-query';
import api from '../axios';
import type { Concept } from '../../types';

export { useConcepts, useKnowledgeGraph } from './useAdaptive';

interface CreateConceptData {
  name: string;
  displayName: string;
  description?: string;
  topicGroup?: string;
  difficultyTier?: number;
}

interface UpdateConceptData extends CreateConceptData {
  id: number;
}

interface CreateEdgeData {
  fromConceptId: number;
  toConceptId: number;
}

const INVALIDATE_KEYS = [['concepts'], ['knowledge-graph']];

export function useCreateConcept() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (data: CreateConceptData) => {
      const res = await api.post<Concept>('/concepts', data);
      return res.data;
    },
    onSuccess: () => {
      for (const key of INVALIDATE_KEYS) queryClient.invalidateQueries({ queryKey: key });
    },
  });
}

export function useUpdateConcept() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async ({ id, ...data }: UpdateConceptData) => {
      const res = await api.put<Concept>(`/concepts/${id}`, data);
      return res.data;
    },
    onSuccess: () => {
      for (const key of INVALIDATE_KEYS) queryClient.invalidateQueries({ queryKey: key });
    },
  });
}

export function useDeleteConcept() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (id: number) => {
      const res = await api.delete(`/concepts/${id}`);
      return res.data;
    },
    onSuccess: () => {
      for (const key of INVALIDATE_KEYS) queryClient.invalidateQueries({ queryKey: key });
    },
  });
}

export function useCreateEdge() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (data: CreateEdgeData) => {
      const res = await api.post('/concepts/edges', data);
      return res.data;
    },
    onSuccess: () => {
      for (const key of INVALIDATE_KEYS) queryClient.invalidateQueries({ queryKey: key });
    },
  });
}

export function useDeleteEdge() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (id: number) => {
      const res = await api.delete(`/concepts/edges/${id}`);
      return res.data;
    },
    onSuccess: () => {
      for (const key of INVALIDATE_KEYS) queryClient.invalidateQueries({ queryKey: key });
    },
  });
}
