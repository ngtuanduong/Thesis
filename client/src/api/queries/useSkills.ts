import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import api from '../axios';

interface Skill {
  id: string;
  userId: string;
  skillName: string;
  score: number;
  updatedAt: string;
}

export function useMySkills() {
  return useQuery({
    queryKey: ['skills', 'me'],
    queryFn: async () => {
      const res = await api.get<Skill[]>('/skills/me');
      return res.data;
    },
  });
}

export function useComputeSkills() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async () => {
      const res = await api.post('/skills/compute');
      return res.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['skills'] });
    },
  });
}
