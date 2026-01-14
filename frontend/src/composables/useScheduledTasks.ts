import { ref, computed } from 'vue';
import {
  getScheduledTasks,
  createScheduledTask,
  updateScheduledTask,
  deleteScheduledTask,
  pauseScheduledTask,
  resumeScheduledTask,
  runScheduledTaskNow,
  getTaskExecutions,
  type ScheduledTask,
  type ScheduledTaskExecution,
  type CreateScheduledTaskRequest,
  type UpdateScheduledTaskRequest,
} from '../api/scheduledTask';

const tasks = ref<ScheduledTask[]>([]);
const isLoading = ref(false);
const error = ref<string | null>(null);

export function useScheduledTasks() {
  const loadTasks = async () => {
    isLoading.value = true;
    error.value = null;
    try {
      tasks.value = await getScheduledTasks();
    } catch (e: any) {
      error.value = e.message || 'Failed to load tasks';
      throw e;
    } finally {
      isLoading.value = false;
    }
  };

  const create = async (data: CreateScheduledTaskRequest): Promise<ScheduledTask> => {
    const task = await createScheduledTask(data);
    tasks.value.unshift(task);
    return task;
  };

  const update = async (taskId: string, data: UpdateScheduledTaskRequest): Promise<ScheduledTask> => {
    const updated = await updateScheduledTask(taskId, data);
    const index = tasks.value.findIndex(t => t.id === taskId);
    if (index >= 0) {
      tasks.value[index] = updated;
    }
    return updated;
  };

  const remove = async (taskId: string): Promise<void> => {
    await deleteScheduledTask(taskId);
    tasks.value = tasks.value.filter(t => t.id !== taskId);
  };

  const pause = async (taskId: string): Promise<ScheduledTask> => {
    const updated = await pauseScheduledTask(taskId);
    const index = tasks.value.findIndex(t => t.id === taskId);
    if (index >= 0) {
      tasks.value[index] = updated;
    }
    return updated;
  };

  const resume = async (taskId: string): Promise<ScheduledTask> => {
    const updated = await resumeScheduledTask(taskId);
    const index = tasks.value.findIndex(t => t.id === taskId);
    if (index >= 0) {
      tasks.value[index] = updated;
    }
    return updated;
  };

  const runNow = async (taskId: string): Promise<ScheduledTaskExecution> => {
    return await runScheduledTaskNow(taskId);
  };

  const getExecutions = async (taskId: string, limit = 20): Promise<ScheduledTaskExecution[]> => {
    return await getTaskExecutions(taskId, limit);
  };

  // Computed
  const activeTasks = computed(() => tasks.value.filter(t => t.status === 'active'));
  const pausedTasks = computed(() => tasks.value.filter(t => t.status === 'paused'));

  return {
    tasks: computed(() => tasks.value),
    activeTasks,
    pausedTasks,
    isLoading: computed(() => isLoading.value),
    error: computed(() => error.value),
    loadTasks,
    create,
    update,
    remove,
    pause,
    resume,
    runNow,
    getExecutions,
  };
}
