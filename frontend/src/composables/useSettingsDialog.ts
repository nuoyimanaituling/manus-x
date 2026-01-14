import { ref } from 'vue'

// Global state for settings dialog
const isSettingsDialogOpen = ref(false)
const defaultTab = ref<string>('settings')

export function useSettingsDialog() {
  const openSettingsDialog = (tabId?: string) => {
    if (tabId) {
      defaultTab.value = tabId
    }
    isSettingsDialogOpen.value = true
  }

  const closeSettingsDialog = () => {
    isSettingsDialogOpen.value = false
  }

  const toggleSettingsDialog = () => {
    isSettingsDialogOpen.value = !isSettingsDialogOpen.value
  }

  const setDefaultTab = (tabId: string) => {
    defaultTab.value = tabId
  }

  return {
    isSettingsDialogOpen,
    defaultTab,
    openSettingsDialog,
    closeSettingsDialog,
    toggleSettingsDialog,
    setDefaultTab
  }
}
