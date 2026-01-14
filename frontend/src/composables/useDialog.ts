import { ref, reactive, readonly } from 'vue'
import { useI18n } from 'vue-i18n'

// Dialog state
interface DialogState {
  title: string
  content: string
  confirmText: string
  cancelText: string
  confirmType: 'primary' | 'danger'
  onConfirm?: () => void | Promise<void>
  onCancel?: () => void
}

// Global state
const dialogVisible = ref(false)
const dialogConfig = reactive<DialogState>({
  title: '',
  content: '',
  confirmText: '',
  cancelText: '',
  confirmType: 'primary',
  onConfirm: undefined,
  onCancel: undefined
})

export function useDialog() {
  const { t } = useI18n()

  // Handle confirm
  const handleConfirm = async () => {
    if (dialogConfig.onConfirm) {
      await dialogConfig.onConfirm()
    }
    dialogVisible.value = false
  }

  // Handle cancel
  const handleCancel = () => {
    if (dialogConfig.onCancel) {
      dialogConfig.onCancel()
    }
    dialogVisible.value = false
  }

  // Show general confirm dialog
  const showConfirmDialog = (options: {
    title: string
    content: string
    confirmText?: string
    cancelText?: string
    confirmType?: 'primary' | 'danger'
    onConfirm?: () => void | Promise<void>
    onCancel?: () => void
  }) => {
    Object.assign(dialogConfig, {
      title: options.title,
      content: options.content,
      confirmText: options.confirmText || t('Confirm'),
      cancelText: options.cancelText || t('Cancel'),
      confirmType: options.confirmType || 'primary',
      onConfirm: options.onConfirm,
      onCancel: options.onCancel
    })
    dialogVisible.value = true
  }

  // Show delete session dialog
  const showDeleteSessionDialog = (onConfirm?: () => void | Promise<void>) => {
    showConfirmDialog({
      title: t('Are you sure you want to delete this session?'),
      content: t('The chat history of this session cannot be recovered after deletion.'),
      confirmText: t('Delete'),
      cancelText: t('Cancel'),
      confirmType: 'danger',
      onConfirm
    })
  }

  return {
    dialogVisible: readonly(dialogVisible),
    dialogConfig: readonly(dialogConfig),
    handleConfirm,
    handleCancel,
    showConfirmDialog,
    showDeleteSessionDialog
  }
} 