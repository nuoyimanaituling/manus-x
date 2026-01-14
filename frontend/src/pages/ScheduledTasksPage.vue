<template>
  <div class="flex flex-col h-full w-full">
    <!-- Top Navigation -->
    <div class="w-full pt-4 pb-4 px-5 bg-[var(--background-gray-main)] sticky top-0 z-10">
      <div class="flex justify-between items-center w-full">
        <div class="h-8 relative z-20 overflow-hidden flex gap-2 items-center flex-shrink-0">
          <div class="relative flex items-center">
            <div @click="toggleLeftPanel" v-if="!isLeftPanelShow"
              class="flex h-7 w-7 items-center justify-center cursor-pointer rounded-md hover:bg-[var(--fill-tsp-gray-main)]">
              <PanelLeft class="size-5 text-[var(--icon-secondary)]" />
            </div>
          </div>
          <router-link to="/" class="flex items-center">
            <ManusIcon :size="30" />
            <ManusLogoTextIcon />
          </router-link>
        </div>
        <div class="flex items-center gap-2">
          <router-link to="/"
            class="items-center justify-center whitespace-nowrap font-medium transition-colors hover:opacity-90 active:opacity-80 px-[12px] gap-[6px] text-sm min-w-16 outline outline-1 -outline-offset-1 hover:bg-[var(--fill-tsp-white-light)] text-[var(--text-primary)] outline-[var(--border-btn-main)] bg-transparent clickable hidden sm:flex rounded-[100px] relative h-[32px]">
            <Home class="size-[18px]" />
            首页
          </router-link>
        </div>
      </div>
    </div>

    <!-- Content -->
    <div class="flex-1 max-w-5xl mx-auto px-6 py-8 w-full">
    <!-- Header -->
    <div class="flex justify-between items-center mb-6">
      <div>
        <h1 class="text-2xl font-semibold text-[var(--text-primary)]">
          定时任务
        </h1>
        <p class="text-sm text-[var(--text-tertiary)] mt-1">
          自动化执行AI任务
        </p>
      </div>
      <button
        @click="showCreateDialog = true"
        class="flex items-center gap-2 px-4 py-2 bg-[var(--Button-primary)] text-white rounded-lg hover:opacity-90">
        <Plus :size="18" />
        新建定时任务
      </button>
    </div>

    <!-- Task List -->
    <div v-if="isLoading" class="flex justify-center py-12">
      <div class="text-[var(--text-tertiary)]">加载中...</div>
    </div>

    <div v-else-if="tasks.length === 0" class="flex flex-col items-center py-12">
      <div class="text-[var(--text-secondary)] mb-4">还没有定时任务</div>
      <button
        @click="showCreateDialog = true"
        class="text-[var(--text-link)] hover:underline">
        创建第一个定时任务
      </button>
    </div>

    <div v-else class="space-y-4">
      <div
        v-for="task in tasks"
        :key="task.id"
        class="p-4 border border-[var(--border-secondary)] rounded-lg hover:border-[var(--border-primary)] transition-colors">
        <div class="flex justify-between items-start">
          <div class="flex-1">
            <h3 class="font-medium text-[var(--text-primary)]">{{ task.name }}</h3>
            <p v-if="task.description" class="text-sm text-[var(--text-secondary)] mt-1">{{ task.description }}</p>
            <div class="flex items-center gap-4 mt-2 text-sm text-[var(--text-tertiary)]">
              <span>{{ task.cron_expression }}</span>
              <span v-if="task.next_run_at">下次: {{ formatTime(task.next_run_at) }}</span>
              <span>执行次数: {{ task.run_count }}</span>
              <span :class="getStatusClass(task.status)">{{ getStatusText(task.status) }}</span>
            </div>
          </div>
          <div class="flex gap-2">
            <button
              v-if="task.status === 'active'"
              @click="handlePause(task)"
              class="px-3 py-1 text-sm text-[var(--text-secondary)] hover:text-[var(--text-primary)] border border-[var(--border-secondary)] rounded">
              暂停
            </button>
            <button
              v-else-if="task.status === 'paused'"
              @click="handleResume(task)"
              class="px-3 py-1 text-sm text-[var(--text-secondary)] hover:text-[var(--text-primary)] border border-[var(--border-secondary)] rounded">
              恢复
            </button>
            <button
              @click="handleRunNow(task)"
              class="px-3 py-1 text-sm text-[var(--text-secondary)] hover:text-[var(--text-primary)] border border-[var(--border-secondary)] rounded">
              立即执行
            </button>
            <button
              @click="confirmDelete(task)"
              class="px-3 py-1 text-sm text-red-500 hover:text-red-600 border border-red-300 rounded">
              删除
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Create Dialog (simplified) -->
    <div v-if="showCreateDialog" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" @click.self="showCreateDialog = false">
      <div class="bg-[var(--background-gray-main)] rounded-lg p-6 w-full max-w-md">
        <h2 class="text-xl font-semibold mb-4">新建定时任务</h2>
        <div class="space-y-4">
          <div>
            <label class="block text-sm mb-1">任务名称</label>
            <input v-model="formData.name" type="text" class="w-full px-3 py-2 border border-[var(--border-secondary)] rounded" placeholder="例如: 每日新闻摘要" />
          </div>
          <div>
            <label class="block text-sm mb-1">执行频率</label>
            <select v-model="formData.cron_expression" class="w-full px-3 py-2 border border-[var(--border-secondary)] rounded">
              <option value="0 8 * * *">每天早上8点</option>
              <option value="0 9 * * *">每天早上9点</option>
              <option value="0 * * * *">每小时</option>
              <option value="0 9 * * 1-5">工作日早上9点</option>
            </select>
          </div>
          <div>
            <label class="block text-sm mb-1">任务内容</label>
            <textarea v-model="formData.prompt" rows="4" class="w-full px-3 py-2 border border-[var(--border-secondary)] rounded" placeholder="输入要让AI执行的任务..."></textarea>
          </div>
          <div class="flex gap-2 justify-end">
            <button @click="showCreateDialog = false" class="px-4 py-2 border border-[var(--border-secondary)] rounded hover:bg-[var(--fill-tsp-gray-main)]">
              取消
            </button>
            <button @click="handleCreate" class="px-4 py-2 bg-[var(--Button-primary)] text-white rounded hover:opacity-90">
              创建
            </button>
          </div>
        </div>
      </div>
    </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { Plus, PanelLeft, Home } from 'lucide-vue-next';
import ManusIcon from '../components/icons/ManusIcon.vue';
import ManusLogoTextIcon from '../components/icons/ManusLogoTextIcon.vue';
import { useLeftPanel } from '../composables/useLeftPanel';
import { useScheduledTasks } from '../composables/useScheduledTasks';
import type { ScheduledTask } from '../api/scheduledTask';
import { showSuccessToast, showErrorToast } from '../utils/toast';

const { tasks, isLoading, loadTasks, create, pause, resume, remove, runNow } = useScheduledTasks();
const { toggleLeftPanel, isLeftPanelShow } = useLeftPanel();

const showCreateDialog = ref(false);
const formData = ref({
  name: '',
  cron_expression: '0 9 * * *',
  prompt: '',
});

onMounted(() => {
  loadTasks();
});

const handleCreate = async () => {
  if (!formData.value.name || !formData.value.prompt) {
    showErrorToast('请填写完整信息');
    return;
  }
  try {
    await create(formData.value);
    showSuccessToast('定时任务创建成功');
    showCreateDialog.value = false;
    formData.value = { name: '', cron_expression: '0 9 * * *', prompt: '' };
  } catch (e: any) {
    showErrorToast(e.message || '创建失败');
  }
};

const handlePause = async (task: ScheduledTask) => {
  try {
    await pause(task.id);
    showSuccessToast('任务已暂停');
  } catch (e: any) {
    showErrorToast(e.message || '暂停失败');
  }
};

const handleResume = async (task: ScheduledTask) => {
  try {
    await resume(task.id);
    showSuccessToast('任务已恢复');
  } catch (e: any) {
    showErrorToast(e.message || '恢复失败');
  }
};

const handleRunNow = async (task: ScheduledTask) => {
  try {
    await runNow(task.id);
    showSuccessToast('任务开始执行');
  } catch (e: any) {
    showErrorToast(e.message || '执行失败');
  }
};

const confirmDelete = async (task: ScheduledTask) => {
  if (confirm(`确定删除定时任务 "${task.name}"？`)) {
    try {
      await remove(task.id);
      showSuccessToast('任务已删除');
    } catch (e: any) {
      showErrorToast(e.message || '删除失败');
    }
  }
};

const formatTime = (timestamp: number) => {
  const date = new Date(timestamp * 1000);
  return date.toLocaleString('zh-CN');
};

const getStatusClass = (status: string) => {
  const classes = {
    active: 'text-green-600',
    paused: 'text-yellow-600',
    disabled: 'text-gray-500',
  };
  return classes[status as keyof typeof classes] || '';
};

const getStatusText = (status: string) => {
  const texts = {
    active: '运行中',
    paused: '已暂停',
    disabled: '已禁用',
  };
  return texts[status as keyof typeof texts] || status;
};
</script>
