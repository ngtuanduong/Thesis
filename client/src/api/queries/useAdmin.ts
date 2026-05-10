import { useQuery, useMutation, useQueryClient, keepPreviousData } from '@tanstack/react-query';
import api from '../axios';
import type { PaginatedResponse } from '../../types';

interface AdminStats {
  totalUsers: number;
  totalSubmissions: number;
  totalProblems: number;
  totalCourses: number;
  activeUsersToday: number;
}

interface AdminUser {
  id: string;
  email: string;
  name: string;
  role: string;
  createdAt: string;
  _count: { submissions: number };
  experimentGroup: { groupName: string; assignedAt: string } | null;
}

interface ExperimentStats {
  groups: { groupName: string; count: number }[];
  totalAssigned: number;
  totalUnassigned: number;
}

interface ExportEventsResponse {
  events: unknown[];
}

export function useAdminStats() {
  return useQuery({
    queryKey: ['admin-stats'],
    queryFn: async () => {
      const res = await api.get<AdminStats>('/admin/stats');
      return res.data;
    },
  });
}

export function useAdminUsers(params: {
  page: number;
  pageSize: number;
  search?: string;
  role?: string[];
}) {
  return useQuery({
    queryKey: ['admin-users', params],
    queryFn: async () => {
      const query: Record<string, string> = {
        page: String(params.page),
        pageSize: String(params.pageSize),
      };
      if (params.search) query.search = params.search;
      if (params.role?.length) query.role = params.role.join(',');
      const res = await api.get<PaginatedResponse<AdminUser>>('/admin/users', { params: query });
      return res.data;
    },
    placeholderData: keepPreviousData,
  });
}

export function useAssignGroup() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ userId, groupName }: { userId: string; groupName: string }) => {
      const res = await api.post(`/admin/users/${userId}/assign-group`, { groupName });
      return res.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['admin-users'] });
    },
  });
}

export function useExperimentStats() {
  return useQuery({
    queryKey: ['admin-experiment'],
    queryFn: async () => {
      const res = await api.get<ExperimentStats>('/admin/experiment');
      return res.data;
    },
  });
}

export function useExportEvents(event?: string) {
  return useQuery({
    queryKey: ['admin-export-events', event],
    queryFn: async () => {
      const url = event ? `/admin/export/events?event=${event}` : '/admin/export/events';
      const res = await api.get<ExportEventsResponse>(url);
      return res.data;
    },
    enabled: !!event,
  });
}
