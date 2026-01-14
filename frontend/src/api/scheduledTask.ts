import { apiClient } from './client';

// Types
export interface ScheduledTask {
  id: string;
  name: string;
  description: string | null;
  cron_expression: string;
  timezone: string;
  status: 'active' | 'paused' | 'disabled';
  prompt: string;
  next_run_at: number | null;
  last_run_at: number | null;
  run_count: number;
  created_at: number;
}

export interface ScheduledTaskExecution {
  id: string;
  task_id: string;
  session_id: string | null;
  status: 'pending' | 'running' | 'completed' | 'failed' | 'cancelled';
  scheduled_at: number;
  started_at: number | null;
  completed_at: number | null;
  result_summary: string | null;
  error_message: string | null;
}

export interface CreateScheduledTaskRequest {
  name: string;
  cron_expression: string;
  prompt: string;
  timezone?: string;
  description?: string;
  save_result?: boolean;
  notification_type?: 'none' | 'email';
  notification_email?: string;
  attachments?: string[];
}

export interface UpdateScheduledTaskRequest {
  name?: string;
  cron_expression?: string;
  prompt?: string;
  timezone?: string;
  description?: string;
}

// API Functions
export async function createScheduledTask(data: CreateScheduledTaskRequest): Promise<ScheduledTask> {
  const response = await apiClient.post<ScheduledTask>('/scheduled-tasks', data);
  return response.data;
}

export async function getScheduledTasks(): Promise<ScheduledTask[]> {
  const response = await apiClient.get<ScheduledTask[]>('/scheduled-tasks');
  return response.data;
}

export async function getScheduledTask(taskId: string): Promise<ScheduledTask> {
  const response = await apiClient.get<ScheduledTask>(`/scheduled-tasks/${taskId}`);
  return response.data;
}

export async function updateScheduledTask(
  taskId: string,
  data: UpdateScheduledTaskRequest
): Promise<ScheduledTask> {
  const response = await apiClient.put<ScheduledTask>(`/scheduled-tasks/${taskId}`, data);
  return response.data;
}

export async function deleteScheduledTask(taskId: string): Promise<void> {
  await apiClient.delete(`/scheduled-tasks/${taskId}`);
}

export async function pauseScheduledTask(taskId: string): Promise<ScheduledTask> {
  const response = await apiClient.post<ScheduledTask>(`/scheduled-tasks/${taskId}/pause`);
  return response.data;
}

export async function resumeScheduledTask(taskId: string): Promise<ScheduledTask> {
  const response = await apiClient.post<ScheduledTask>(`/scheduled-tasks/${taskId}/resume`);
  return response.data;
}

export async function runScheduledTaskNow(taskId: string): Promise<ScheduledTaskExecution> {
  const response = await apiClient.post<ScheduledTaskExecution>(`/scheduled-tasks/${taskId}/run`);
  return response.data;
}

export async function getTaskExecutions(
  taskId: string,
  limit: number = 20
): Promise<ScheduledTaskExecution[]> {
  const response = await apiClient.get<ScheduledTaskExecution[]>(
    `/scheduled-tasks/${taskId}/executions`,
    { params: { limit } }
  );
  return response.data;
}
