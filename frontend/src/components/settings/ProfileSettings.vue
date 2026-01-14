<template>
    <div class="flex flex-col items-start self-stretch flex-1 overflow-hidden">
        <div class="flex flex-col items-center relative w-full max-sm:px-4 max-sm:pb-4 px-4 pt-4 pb-4 md:px-6 md:pt-4">
            <div class="flex items-center gap-6 w-full p5-4 pb-8">
                <div
                    class="flex-shrink-0 rounded-full overflow-hidden border border-[var(--border-main)]">
                    <div class="relative flex items-center justify-center font-bold flex-shrink-0"
                        style="width: 80px; height: 80px; font-size: 40px; color: rgba(255, 255, 255, 0.9); background-color: rgb(59, 130, 246);">
                        {{ avatarLetter }}</div>
                </div>
                <div class="flex flex-col gap-[6px]"><span
                        class="text-[var(--text-secondary)] text-sm leading-[22px]">{{ t('Name') }}</span>
                    <div
                        class="group rounded-[10px] overflow-hidden text-sm leading-[22px] text-[var(--text-primary)] placeholder:text-[var(--text-disable)] h-10 flex items-center gap-[10px] bg-[var(--fill-tsp-white-main)] pt-2 pr-3 pb-2 pl-4 focus-within:ring-[1.5px] focus-within:ring-[var(--border-dark)] w-full sm:w-[300px]">
                        <input 
                            maxlength="20"
                            class="h-full min-w-1 flex-1 bg-transparent disabled:cursor-not-allowed placeholder:text-[var(--text-disable)]"
                            v-model="localFullname"
                            @blur="handleFullnameSubmit"
                            @keyup.enter="handleFullnameSubmit"
                            :placeholder="t('Unknown User')" />
                        <ClearIcon 
                            :size="16" 
                            class="cursor-pointer opacity-0 hover:opacity-90 group-hover:opacity-100 group-focus-within:opacity-100" 
                            @click="clearFullname"
                        />
                    </div>
                </div>
            </div>
            <div class="w-full flex flex-col">
                <div class="w-full py-3 border-b border-[var(--border-light)]">
                    <div class="flex items-center justify-between gap-3 max-sm:flex-col max-sm:items-stretch">
                        <div class="flex flex-col gap-1">
                            <div class="flex items-center justify-start gap-[6px] text-[var(--text-primary)]"><span
                                    class="text-[var(--text-primary)] text-sm leading-[22px]">{{ t('Email') }}</span></div>
                            <div class="text-[var(--text-tertiary)] text-xs">{{ currentUser?.email || t('No email') }}</div>
                        </div>
                    </div>
                </div>
                <div class="w-full py-3 border-b border-[var(--border-light)]">
                    <div class="flex items-center justify-between gap-3 max-sm:flex-col max-sm:items-stretch">
                        <div class="flex flex-col gap-1">
                            <div class="flex items-center justify-start gap-[6px] text-[var(--text-primary)]"><span
                                    class="text-[var(--text-primary)] text-sm leading-[22px]">{{ t('Password') }}</span></div>
                            <div class="text-[var(--text-tertiary)] text-xs">
                                <div class="inline-flex items-center gap-[4px]"><span
                                        class="rounded-[50%] w-[8px] h-[8px] bg-[var(--icon-tertiary)]"></span><span
                                        class="rounded-[50%] w-[8px] h-[8px] bg-[var(--icon-tertiary)]"></span><span
                                        class="rounded-[50%] w-[8px] h-[8px] bg-[var(--icon-tertiary)]"></span><span
                                        class="rounded-[50%] w-[8px] h-[8px] bg-[var(--icon-tertiary)]"></span><span
                                        class="rounded-[50%] w-[8px] h-[8px] bg-[var(--icon-tertiary)]"></span><span
                                        class="rounded-[50%] w-[8px] h-[8px] bg-[var(--icon-tertiary)]"></span><span
                                        class="rounded-[50%] w-[8px] h-[8px] bg-[var(--icon-tertiary)]"></span><span
                                        class="rounded-[50%] w-[8px] h-[8px] bg-[var(--icon-tertiary)]"></span><span
                                        class="rounded-[50%] w-[8px] h-[8px] bg-[var(--icon-tertiary)]"></span><span
                                        class="rounded-[50%] w-[8px] h-[8px] bg-[var(--icon-tertiary)]"></span></div>
                            </div>
                        </div>
                        <div class="flex gap-[6px] max-sm:justify-end"><button
                                class="inline-flex items-center justify-center whitespace-nowrap font-medium transition-colors hover:opacity-90 active:opacity-80 px-[12px] rounded-[10px] gap-[6px] text-sm min-w-16 outline outline-1 -outline-offset-1 hover:bg-[var(--fill-tsp-white-light)] text-[var(--text-primary)] outline-[var(--border-btn-main)] bg-transparent h-[32px] focus:outline focus:outline-1 focus:-outline-offset-1 focus:outline-[var(--border-btn-main)]"
                                @click="openChangePasswordDialog">{{ t('Update Password') }}</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Change Password Dialog -->
    <ChangePasswordDialog ref="changePasswordDialogRef" />
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue';
import { useI18n } from 'vue-i18n';
import { useAuth } from '../../composables/useAuth';
import { changeFullname } from '../../api/auth';
import { showSuccessToast, showErrorToast } from '../../utils/toast';
import ClearIcon from '../icons/ClearIcon.vue';
import ChangePasswordDialog from './ChangePasswordDialog.vue';

const { t } = useI18n();
const { currentUser, loadCurrentUser } = useAuth();

// Dialog refs
const changePasswordDialogRef = ref<InstanceType<typeof ChangePasswordDialog>>();

// Local fullname state
const localFullname = ref(currentUser.value?.fullname || '');

// Watch for currentUser changes to sync localFullname
watch(currentUser, (newUser) => {
  if (newUser) {
    localFullname.value = newUser.fullname || '';
  }
}, { immediate: true });



// Update fullname function
const updateFullname = async (newFullname: string) => {
  // Skip if empty or same as current
  if (!newFullname.trim() || newFullname === currentUser.value?.fullname) {
    return;
  }

  try {
    await changeFullname({ fullname: newFullname.trim() });
    // Refresh current user data to get updated info
    await loadCurrentUser();
    showSuccessToast(t('Full name updated successfully'));
  } catch (error: any) {
    console.error('Failed to update fullname:', error);
    // Reset local state to original value
    localFullname.value = currentUser.value?.fullname || '';
    
    // Show error message
    const errorMessage = error?.response?.data?.message || error?.message || t('Failed to update full name');
    showErrorToast(errorMessage);
  }
};

// Handle input change on blur or Enter
const handleFullnameSubmit = () => {
  updateFullname(localFullname.value);
};

// Clear fullname input
const clearFullname = () => {
  localFullname.value = '';
};

// Get first letter of user's fullname for avatar display
const avatarLetter = computed(() => {
  return currentUser.value?.fullname?.charAt(0)?.toUpperCase() || 'M';
});

// Open change password dialog
const openChangePasswordDialog = () => {
  changePasswordDialogRef.value?.open();
};
</script>
