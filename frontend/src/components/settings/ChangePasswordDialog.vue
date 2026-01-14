<template>
  <Dialog v-model:open="open">
    <DialogContent class="bg-[var(--background-menu-white)] w-[480px]">
      <DialogHeader>
        <DialogTitle>
          {{ t('Update Password') }}
        </DialogTitle>
      </DialogHeader>
      <div class="pt-[12px] px-[24px] pb-[24px]">
        <form class="flex flex-col items-stretch gap-[4px]">
          <label class="flex flex-col gap-[8px]">
            <div class="text-[16px] text-[var(--text-secondary)] leading-[24px]">{{ t('Current Password') }}</div>
            <div class="relative w-full">
              <input v-model="currentPassword"
                class="rounded-[10px] overflow-hidden text-sm leading-[22px] text-[var(--text-primary)] h-10 w-full disabled:cursor-not-allowed placeholder:text-[var(--text-disable)] pt-1 pb-1 pl-3 focus:ring-[1.5px] focus:ring-[var(--border-dark)] min-h-[48px] bg-[var(--fill-tsp-white-dark)] pr-[48px]"
                :placeholder="t('Enter current password')" :type="showCurrentPassword ? 'text' : 'password'">
              <div @click="toggleCurrentPasswordVisibility"
                class="text-[var(--icon-tertiary)] absolute z-30 top-[50%] p-[6px] rounded-md transform -translate-y-1/2 cursor-pointer hover:text-[--icon-primary] active:opacity-90 transition-all right-[10px]">
                <!-- Eye closed icon (password is hidden) -->
                <svg v-if="!showCurrentPassword" width="20" height="20" viewBox="0 0 24 24" fill="none"
                  xmlns="http://www.w3.org/2000/svg">
                  <path fill-rule="evenodd" clip-rule="evenodd"
                    d="M2.29331 2.29289C2.68383 1.90237 3.317 1.90237 3.70752 2.29289L7.34625 5.93162C7.40455 5.97793 7.45837 6.03139 7.50637 6.09174L17.8974 16.4828C17.9652 16.5347 18.0272 16.5962 18.0813 16.6667L21.7075 20.2929C22.098 20.6834 22.098 21.3166 21.7075 21.7071C21.317 22.0976 20.6838 22.0976 20.2933 21.7071L17.1396 18.5534C15.6947 19.3988 13.972 20 12.0004 20C9.13874 20 6.80576 18.7353 5.07716 17.2926C3.35091 15.8518 2.16738 14.1857 1.57463 13.2472C1.5668 13.2348 1.55876 13.2221 1.55055 13.2092C1.43291 13.024 1.28018 12.7836 1.20298 12.4467C1.14065 12.1748 1.14067 11.825 1.20303 11.553C1.28028 11.2161 1.43344 10.9751 1.55139 10.7895C1.55967 10.7765 1.56777 10.7637 1.57567 10.7512C2.17804 9.79766 3.40132 8.07525 5.19576 6.60955L2.29331 3.70711C1.90278 3.31658 1.90278 2.68342 2.29331 2.29289ZM6.61828 8.03208C4.97911 9.32619 3.83406 10.921 3.26654 11.8194C3.23105 11.8755 3.20617 11.915 3.18537 11.9492C3.17149 11.9721 3.16235 11.9878 3.15625 11.9988C3.15625 11.9992 3.15625 11.9996 3.15625 12C3.15625 12.0004 3.15625 12.0008 3.15625 12.0012C3.16227 12.012 3.17127 12.0276 3.1849 12.05C3.20556 12.084 3.23029 12.1232 3.26563 12.1792C3.7983 13.0226 4.8524 14.4999 6.35869 15.7571C7.86263 17.0123 9.75708 18 12.0004 18C13.3533 18 14.5778 17.6414 15.6674 17.0812L14.0322 15.446C13.4368 15.7977 12.7418 16 12.0004 16C9.79128 16 8.00042 14.2091 8.00042 12C8.00042 11.2586 8.20271 10.5636 8.55438 9.96818L6.61828 8.03208ZM10.068 11.4818C10.0239 11.647 10.0004 11.8207 10.0004 12C10.0004 13.1046 10.8958 14 12.0004 14C12.1798 14 12.3534 13.9765 12.5186 13.9324L10.068 11.4818ZM12.0004 6C11.6186 6 11.2482 6.02849 10.8892 6.08156C10.3429 6.16234 9.83448 5.78492 9.7537 5.23858C9.67292 4.69223 10.0503 4.18385 10.5967 4.10307C11.0505 4.03597 11.5187 4 12.0004 4C14.8621 4 17.1951 5.26472 18.9237 6.70743C20.6499 8.14818 21.8335 9.81429 22.4262 10.7528C22.434 10.7652 22.4421 10.7779 22.4503 10.7908C22.5679 10.976 22.7207 11.2164 22.7979 11.5533C22.8602 11.8253 22.8602 12.1751 22.7978 12.4471C22.7205 12.7841 22.5671 13.0254 22.449 13.2113C22.4407 13.2243 22.4325 13.2371 22.4246 13.2497C22.1063 13.7536 21.6232 14.4581 20.9832 15.2224C20.6287 15.6459 19.998 15.7017 19.5745 15.3472C19.1511 14.9926 19.0952 14.3619 19.4498 13.9385C20.0211 13.2561 20.4524 12.6267 20.7338 12.1814C20.7694 12.1251 20.7943 12.0855 20.8152 12.0512C20.8292 12.0281 20.8384 12.0122 20.8446 12.0012C20.8446 12.0008 20.8446 12.0004 20.8446 12C20.8446 11.9996 20.8446 11.9992 20.8446 11.9988C20.8386 11.988 20.8296 11.9725 20.8159 11.95C20.7953 11.916 20.7705 11.8768 20.7352 11.8208C20.2025 10.9774 19.1484 9.50007 17.6421 8.24291C16.1382 6.9877 14.2437 6 12.0004 6Z"
                    fill="currentColor"></path>
                </svg>
                <!-- Eye open icon (password is visible) -->
                <svg v-else width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path
                    d="M12 4C7 4 2.73 7.11 1 12c1.73 4.89 6 8 11 8s9.27-3.11 11-8c-1.73-4.89-6-8-11-8zM12 17c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5zm0-8c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z"
                    fill="currentColor" />
                </svg>
              </div>
            </div>
            <div class="text-[13px] text-[var(--function-error)] leading-[18px] mt-[-2px] min-h-[18px]"></div>
          </label>
          <label class="flex flex-col gap-[8px]">
            <div class="text-[16px] text-[var(--text-secondary)] leading-[24px]">{{ t('New Password') }}</div>
            <div class="relative w-full">
              <input v-model="newPassword"
                class="rounded-[10px] overflow-hidden text-sm leading-[22px] text-[var(--text-primary)] h-10 w-full disabled:cursor-not-allowed placeholder:text-[var(--text-disable)] pt-1 pb-1 pl-3 focus:ring-[1.5px] focus:ring-[var(--border-dark)] min-h-[48px] bg-[var(--fill-tsp-white-dark)] pr-[48px]"
                :placeholder="t('Enter new password')" :type="showNewPassword ? 'text' : 'password'">
              <div @click="toggleNewPasswordVisibility"
                class="text-[var(--icon-tertiary)] absolute z-30 top-[50%] p-[6px] rounded-md transform -translate-y-1/2 cursor-pointer hover:text-[--icon-primary] active:opacity-90 transition-all right-[10px]">
                <!-- Eye closed icon (password is hidden) -->
                <svg v-if="!showNewPassword" width="20" height="20" viewBox="0 0 24 24" fill="none"
                  xmlns="http://www.w3.org/2000/svg">
                  <path fill-rule="evenodd" clip-rule="evenodd"
                    d="M2.29331 2.29289C2.68383 1.90237 3.317 1.90237 3.70752 2.29289L7.34625 5.93162C7.40455 5.97793 7.45837 6.03139 7.50637 6.09174L17.8974 16.4828C17.9652 16.5347 18.0272 16.5962 18.0813 16.6667L21.7075 20.2929C22.098 20.6834 22.098 21.3166 21.7075 21.7071C21.317 22.0976 20.6838 22.0976 20.2933 21.7071L17.1396 18.5534C15.6947 19.3988 13.972 20 12.0004 20C9.13874 20 6.80576 18.7353 5.07716 17.2926C3.35091 15.8518 2.16738 14.1857 1.57463 13.2472C1.5668 13.2348 1.55876 13.2221 1.55055 13.2092C1.43291 13.024 1.28018 12.7836 1.20298 12.4467C1.14065 12.1748 1.14067 11.825 1.20303 11.553C1.28028 11.2161 1.43344 10.9751 1.55139 10.7895C1.55967 10.7765 1.56777 10.7637 1.57567 10.7512C2.17804 9.79766 3.40132 8.07525 5.19576 6.60955L2.29331 3.70711C1.90278 3.31658 1.90278 2.68342 2.29331 2.29289ZM6.61828 8.03208C4.97911 9.32619 3.83406 10.921 3.26654 11.8194C3.23105 11.8755 3.20617 11.915 3.18537 11.9492C3.17149 11.9721 3.16235 11.9878 3.15625 11.9988C3.15625 11.9992 3.15625 11.9996 3.15625 12C3.15625 12.0004 3.15625 12.0008 3.15625 12.0012C3.16227 12.012 3.17127 12.0276 3.1849 12.05C3.20556 12.084 3.23029 12.1232 3.26563 12.1792C3.7983 13.0226 4.8524 14.4999 6.35869 15.7571C7.86263 17.0123 9.75708 18 12.0004 18C13.3533 18 14.5778 17.6414 15.6674 17.0812L14.0322 15.446C13.4368 15.7977 12.7418 16 12.0004 16C9.79128 16 8.00042 14.2091 8.00042 12C8.00042 11.2586 8.20271 10.5636 8.55438 9.96818L6.61828 8.03208ZM10.068 11.4818C10.0239 11.647 10.0004 11.8207 10.0004 12C10.0004 13.1046 10.8958 14 12.0004 14C12.1798 14 12.3534 13.9765 12.5186 13.9324L10.068 11.4818ZM12.0004 6C11.6186 6 11.2482 6.02849 10.8892 6.08156C10.3429 6.16234 9.83448 5.78492 9.7537 5.23858C9.67292 4.69223 10.0503 4.18385 10.5967 4.10307C11.0505 4.03597 11.5187 4 12.0004 4C14.8621 4 17.1951 5.26472 18.9237 6.70743C20.6499 8.14818 21.8335 9.81429 22.4262 10.7528C22.434 10.7652 22.4421 10.7779 22.4503 10.7908C22.5679 10.976 22.7207 11.2164 22.7979 11.5533C22.8602 11.8253 22.8602 12.1751 22.7978 12.4471C22.7205 12.7841 22.5671 13.0254 22.449 13.2113C22.4407 13.2243 22.4325 13.2371 22.4246 13.2497C22.1063 13.7536 21.6232 14.4581 20.9832 15.2224C20.6287 15.6459 19.998 15.7017 19.5745 15.3472C19.1511 14.9926 19.0952 14.3619 19.4498 13.9385C20.0211 13.2561 20.4524 12.6267 20.7338 12.1814C20.7694 12.1251 20.7943 12.0855 20.8152 12.0512C20.8292 12.0281 20.8384 12.0122 20.8446 12.0012C20.8446 12.0008 20.8446 12.0004 20.8446 12C20.8446 11.9996 20.8446 11.9992 20.8446 11.9988C20.8386 11.988 20.8296 11.9725 20.8159 11.95C20.7953 11.916 20.7705 11.8768 20.7352 11.8208C20.2025 10.9774 19.1484 9.50007 17.6421 8.24291C16.1382 6.9877 14.2437 6 12.0004 6Z"
                    fill="currentColor"></path>
                </svg>
                <!-- Eye open icon (password is visible) -->
                <svg v-else width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path
                    d="M12 4C7 4 2.73 7.11 1 12c1.73 4.89 6 8 11 8s9.27-3.11 11-8c-1.73-4.89-6-8-11-8zM12 17c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5zm0-8c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z"
                    fill="currentColor" />
                </svg>
              </div>
            </div>
            <div class="text-[13px] text-[var(--function-error)] leading-[18px] mt-[-2px] min-h-[18px]"></div>
          </label>
          <label class="flex flex-col gap-[8px]">
            <div class="text-[16px] text-[var(--text-secondary)] leading-[24px]">{{ t('Confirm New Password') }}</div>
            <div class="relative w-full">
              <input v-model="confirmPassword"
                class="rounded-[10px] overflow-hidden text-sm leading-[22px] text-[var(--text-primary)] h-10 w-full disabled:cursor-not-allowed placeholder:text-[var(--text-disable)] pt-1 pb-1 pl-3 focus:ring-[1.5px] focus:ring-[var(--border-dark)] min-h-[48px] bg-[var(--fill-tsp-white-dark)] pr-[48px]"
                :placeholder="t('Enter new password again')" :type="showConfirmPassword ? 'text' : 'password'">
              <div @click="toggleConfirmPasswordVisibility"
                class="text-[var(--icon-tertiary)] absolute z-30 top-[50%] p-[6px] rounded-md transform -translate-y-1/2 cursor-pointer hover:text-[--icon-primary] active:opacity-90 transition-all right-[10px]">
                <!-- Eye closed icon (password is hidden) -->
                <svg v-if="!showConfirmPassword" width="20" height="20" viewBox="0 0 24 24" fill="none"
                  xmlns="http://www.w3.org/2000/svg">
                  <path fill-rule="evenodd" clip-rule="evenodd"
                    d="M2.29331 2.29289C2.68383 1.90237 3.317 1.90237 3.70752 2.29289L7.34625 5.93162C7.40455 5.97793 7.45837 6.03139 7.50637 6.09174L17.8974 16.4828C17.9652 16.5347 18.0272 16.5962 18.0813 16.6667L21.7075 20.2929C22.098 20.6834 22.098 21.3166 21.7075 21.7071C21.317 22.0976 20.6838 22.0976 20.2933 21.7071L17.1396 18.5534C15.6947 19.3988 13.972 20 12.0004 20C9.13874 20 6.80576 18.7353 5.07716 17.2926C3.35091 15.8518 2.16738 14.1857 1.57463 13.2472C1.5668 13.2348 1.55876 13.2221 1.55055 13.2092C1.43291 13.024 1.28018 12.7836 1.20298 12.4467C1.14065 12.1748 1.14067 11.825 1.20303 11.553C1.28028 11.2161 1.43344 10.9751 1.55139 10.7895C1.55967 10.7765 1.56777 10.7637 1.57567 10.7512C2.17804 9.79766 3.40132 8.07525 5.19576 6.60955L2.29331 3.70711C1.90278 3.31658 1.90278 2.68342 2.29331 2.29289ZM6.61828 8.03208C4.97911 9.32619 3.83406 10.921 3.26654 11.8194C3.23105 11.8755 3.20617 11.915 3.18537 11.9492C3.17149 11.9721 3.16235 11.9878 3.15625 11.9988C3.15625 11.9992 3.15625 11.9996 3.15625 12C3.15625 12.0004 3.15625 12.0008 3.15625 12.0012C3.16227 12.012 3.17127 12.0276 3.1849 12.05C3.20556 12.084 3.23029 12.1232 3.26563 12.1792C3.7983 13.0226 4.8524 14.4999 6.35869 15.7571C7.86263 17.0123 9.75708 18 12.0004 18C13.3533 18 14.5778 17.6414 15.6674 17.0812L14.0322 15.446C13.4368 15.7977 12.7418 16 12.0004 16C9.79128 16 8.00042 14.2091 8.00042 12C8.00042 11.2586 8.20271 10.5636 8.55438 9.96818L6.61828 8.03208ZM10.068 11.4818C10.0239 11.647 10.0004 11.8207 10.0004 12C10.0004 13.1046 10.8958 14 12.0004 14C12.1798 14 12.3534 13.9765 12.5186 13.9324L10.068 11.4818ZM12.0004 6C11.6186 6 11.2482 6.02849 10.8892 6.08156C10.3429 6.16234 9.83448 5.78492 9.7537 5.23858C9.67292 4.69223 10.0503 4.18385 10.5967 4.10307C11.0505 4.03597 11.5187 4 12.0004 4C14.8621 4 17.1951 5.26472 18.9237 6.70743C20.6499 8.14818 21.8335 9.81429 22.4262 10.7528C22.434 10.7652 22.4421 10.7779 22.4503 10.7908C22.5679 10.976 22.7207 11.2164 22.7979 11.5533C22.8602 11.8253 22.8602 12.1751 22.7978 12.4471C22.7205 12.7841 22.5671 13.0254 22.449 13.2113C22.4407 13.2243 22.4325 13.2371 22.4246 13.2497C22.1063 13.7536 21.6232 14.4581 20.9832 15.2224C20.6287 15.6459 19.998 15.7017 19.5745 15.3472C19.1511 14.9926 19.0952 14.3619 19.4498 13.9385C20.0211 13.2561 20.4524 12.6267 20.7338 12.1814C20.7694 12.1251 20.7943 12.0855 20.8152 12.0512C20.8292 12.0281 20.8384 12.0122 20.8446 12.0012C20.8446 12.0008 20.8446 12.0004 20.8446 12C20.8446 11.9996 20.8446 11.9992 20.8446 11.9988C20.8386 11.988 20.8296 11.9725 20.8159 11.95C20.7953 11.916 20.7705 11.8768 20.7352 11.8208C20.2025 10.9774 19.1484 9.50007 17.6421 8.24291C16.1382 6.9877 14.2437 6 12.0004 6Z"
                    fill="currentColor"></path>
                </svg>
                <!-- Eye open icon (password is visible) -->
                <svg v-else width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path
                    d="M12 4C7 4 2.73 7.11 1 12c1.73 4.89 6 8 11 8s9.27-3.11 11-8c-1.73-4.89-6-8-11-8zM12 17c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5zm0-8c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z"
                    fill="currentColor" />
                </svg>
              </div>
            </div>
            <div class="text-[13px] text-[var(--function-error)] leading-[18px] mt-[-2px] min-h-[18px]"
              v-if="confirmPassword && newPassword !== confirmPassword">
              {{ t('Passwords do not match') }}
            </div>
            <div class="text-[13px] text-[var(--function-error)] leading-[18px] mt-[-2px] min-h-[18px]" v-else></div>
          </label>
        </form>
        <DialogFooter>
          <DialogClose as-child>
            <button
              class="inline-flex items-center justify-center whitespace-nowrap font-medium transition-colors hover:opacity-90 active:opacity-80 bg-[var(--Button-secondary-gray)] text-[var(--text-primary)] h-[36px] px-[12px] rounded-[10px] gap-[6px] text-sm min-w-[100px] min-h-[40px]"
              type="button">
              {{ t('Cancel') }}
            </button>
          </DialogClose>
          <button
            class="inline-flex items-center justify-center whitespace-nowrap font-medium transition-colors bg-[var(--Button-primary-black)] text-[var(--text-onblack)] h-[36px] px-[12px] rounded-[10px] gap-[6px] text-sm min-w-[100px] min-h-[40px]"
            :class="{ 'opacity-50 cursor-not-allowed hover:opacity-50 active:opacity-50': !isFormValid }"
            :disabled="!isFormValid" @click="handleSubmit" type="button">
            <div v-if="isLoading" class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin">
            </div>
            <span v-if="!isLoading">{{ t('Confirm') }}</span>
            <span v-else>{{ t('Processing...') }}</span>
          </button>
        </DialogFooter>
      </div>
    </DialogContent>
  </Dialog>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
  DialogClose
} from '@/components/ui/dialog'
import { changePassword } from '@/api/auth'
import { showSuccessToast, showErrorToast } from '@/utils/toast'

// Use i18n for translations
const { t } = useI18n()

// Dialog state
const open = ref(false)
const isLoading = ref(false)

// Form data
const currentPassword = ref('')
const newPassword = ref('')
const confirmPassword = ref('')

// Password visibility state
const showCurrentPassword = ref(false)
const showNewPassword = ref(false)
const showConfirmPassword = ref(false)

// Form validation
const isFormValid = computed(() => {
  return !isLoading.value &&
    currentPassword.value.trim() !== '' &&
    newPassword.value.trim() !== '' &&
    newPassword.value.length >= 6 &&
    confirmPassword.value.trim() !== '' &&
    newPassword.value === confirmPassword.value
})

// Toggle password visibility
const toggleCurrentPasswordVisibility = () => {
  showCurrentPassword.value = !showCurrentPassword.value
}

const toggleNewPasswordVisibility = () => {
  showNewPassword.value = !showNewPassword.value
}

const toggleConfirmPasswordVisibility = () => {
  showConfirmPassword.value = !showConfirmPassword.value
}



// Reset form when dialog closes
const resetForm = () => {
  currentPassword.value = ''
  newPassword.value = ''
  confirmPassword.value = ''
  showCurrentPassword.value = false
  showNewPassword.value = false
  showConfirmPassword.value = false
  isLoading.value = false
}

// Handle form submission
const handleSubmit = async () => {
  if (!isFormValid.value) {
    return
  }

  isLoading.value = true

  try {
    await changePassword({
      old_password: currentPassword.value,
      new_password: newPassword.value
    })

    showSuccessToast(t('Password change successful'))
    resetForm()
    open.value = false
  } catch (error: any) {
    console.error('Change password error:', error)

    // Extract error message from response
    let errorMessage = t('Password change failed')
    if (error?.response?.data?.message) {
      errorMessage = error.response.data.message
    } else if (error?.message) {
      errorMessage = error.message
    }

    showErrorToast(errorMessage)
  } finally {
    isLoading.value = false
  }
}

// Expose methods to parent component
defineExpose({
  open: () => {
    resetForm()
    open.value = true
  },
  close: () => {
    resetForm()
    open.value = false
  }
})
</script>