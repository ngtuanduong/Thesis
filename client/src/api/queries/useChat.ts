import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import api from '../axios';
import type {
  ChatMessageType,
  ChatSendResponse,
  ChatTokenUsageResponse,
} from '../../types';

export function useChatHistory() {
  return useQuery({
    queryKey: ['chat-history'],
    queryFn: async () => {
      const res = await api.get<ChatMessageType[]>('/chatbot/history', {
        params: { limit: 50 },
      });
      return res.data;
    },
  });
}

export function useSendChatMessage() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (message: string) => {
      const res = await api.post<ChatSendResponse>('/chatbot/send', {
        message,
      });
      return res.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['chat-history'] });
      queryClient.invalidateQueries({ queryKey: ['chat-token-usage'] });
    },
  });
}

export function useClearChatHistory() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async () => {
      const res = await api.delete('/chatbot/history');
      return res.data;
    },
    onSuccess: () => {
      queryClient.setQueryData(['chat-history'], []);
      queryClient.invalidateQueries({ queryKey: ['chat-token-usage'] });
    },
  });
}

export function useChatTokenUsage() {
  return useQuery({
    queryKey: ['chat-token-usage'],
    queryFn: async () => {
      const res = await api.get<ChatTokenUsageResponse>('/chatbot/token-usage');
      return res.data;
    },
  });
}
