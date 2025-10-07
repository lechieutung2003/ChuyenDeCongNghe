<template>
  <div class="h-screen w-full flex justify-center items-center bg-gray-50">
    <div class="form drop-shadow-md">
      <div class="form-header">
        <h1 class="form-title">{{ $t('Change Your Password') }}</h1>
      </div>
      <form @submit.prevent="changePassword">
        <div class="flex-column">
          <label for="currentPassword">{{ $t('Current Password') }}</label>
        </div>
        <div class="inputForm" :class="{ 'error-border': currentPasswordError }">
          <svg height="20" viewBox="0 0 32 32" width="20">
            <g><path d="M16 2C8.268 2 2 8.268 2 16s6.268 14 14 14 14-6.268 14-14S23.732 2 16 2zm0 26C9.383 28 4 22.617 4 16S9.383 4 16 4s12 5.383 12 12-5.383 12-12 12zm0-18a2 2 0 100 4 2 2 0 000-4zm1 6h-2v8h2v-8z"/></g>
          </svg>
          <input
            id="currentPassword"
            v-model="form.currentPassword"
            type="password"
            class="input"
            :placeholder="$t('Current Password')"
            @blur="validateCurrentPassword"
            @input="validateCurrentPassword"
            required
          />
        </div>
        <div v-if="currentPasswordError" class="error-text">{{ currentPasswordError }}</div>

        <div class="flex-column">
          <label for="newPassword">{{ $t('New Password') }}</label>
        </div>
        <div class="inputForm" :class="{ 'error-border': newPasswordError }">
          <svg height="20" viewBox="0 0 32 32" width="20">
            <g><path d="M16 2C8.268 2 2 8.268 2 16s6.268 14 14 14 14-6.268 14-14S23.732 2 16 2zm0 26C9.383 28 4 22.617 4 16S9.383 4 16 4s12 5.383 12 12-5.383 12-12 12zm0-18a2 2 0 100 4 2 2 0 000-4zm1 6h-2v8h2v-8z"/></g>
          </svg>
          <input
            id="newPassword"
            v-model="form.newPassword"
            type="password"
            class="input"
            :placeholder="$t('New Password')"
            @blur="validateNewPassword"
            @input="validateNewPassword"
            required
          />
        </div>
        <div v-if="newPasswordError" class="error-text">{{ newPasswordError }}</div>

        <div class="flex-column">
          <label for="confirmNewPassword">{{ $t('Confirm New Password') }}</label>
        </div>
        <div class="inputForm" :class="{ 'error-border': confirmNewPasswordError }">
          <svg height="20" viewBox="0 0 32 32" width="20">
            <g><path d="M16 2C8.268 2 2 8.268 2 16s6.268 14 14 14 14-6.268 14-14S23.732 2 16 2zm0 26C9.383 28 4 22.617 4 16S9.383 4 16 4s12 5.383 12 12-5.383 12-12 12zm0-18a2 2 0 100 4 2 2 0 000-4zm1 6h-2v8h2v-8z"/></g>
          </svg>
          <input
            id="confirmNewPassword"
            v-model="form.confirmNewPassword"
            type="password"
            class="input"
            :placeholder="$t('Confirm New Password')"
            @blur="validateConfirmNewPassword"
            @input="validateConfirmNewPassword"
            required
          />
        </div>
        <div v-if="confirmNewPasswordError" class="error-text">{{ confirmNewPasswordError }}</div>

        <div class="flex-row mt-4">
          <NuxtLink to="/" class="span">
            {{ $t('Back to login') }}
          </NuxtLink>
        </div>
        <button
          type="submit"
          class="button-submit"
          :disabled="isLoading || !isFormValid"
        >
          <span v-if="isLoading">{{ $t('Changing...') }}</span>
          <span v-else>{{ $t('Change Password') }}</span>
        </button>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ElNotification } from 'element-plus'
import { ref, watch } from 'vue'
import '@/assets/css/form.css'

const form = ref({
  currentPassword: '',
  newPassword: '',
  confirmNewPassword: ''
})

const isLoading = ref(false)
const isFormValid = ref(false)
const currentPasswordError = ref('')
const newPasswordError = ref('')
const confirmNewPasswordError = ref('')

function validateCurrentPassword() {
  currentPasswordError.value = form.value.currentPassword ? '' : 'Please enter your current password'
  checkFormValid()
}
function validateNewPassword() {
  if (!form.value.newPassword) {
    newPasswordError.value = 'Please enter your new password'
  } else if (form.value.newPassword.length < 6) {
    newPasswordError.value = 'The new password must be at least 6 characters long'
  } else {
    newPasswordError.value = ''
  }
  checkFormValid()
}
function validateConfirmNewPassword() {
  if (!form.value.confirmNewPassword) {
    confirmNewPasswordError.value = 'Please confirm your new password'
  } else if (form.value.confirmNewPassword !== form.value.newPassword) {
    confirmNewPasswordError.value = 'Passwords do not match'
  } else {
    confirmNewPasswordError.value = ''
  }
  checkFormValid()
}
function checkFormValid() {
  isFormValid.value =
    !currentPasswordError.value &&
    !newPasswordError.value &&
    !confirmNewPasswordError.value &&
    form.value.currentPassword &&
    form.value.newPassword &&
    form.value.confirmNewPassword
}

watch(() => form.value.currentPassword, validateCurrentPassword)
watch(() => form.value.newPassword, validateNewPassword)
watch(() => form.value.confirmNewPassword, validateConfirmNewPassword)

const changePassword = async () => {
  validateCurrentPassword()
  validateNewPassword()
  validateConfirmNewPassword()
  if (!isFormValid.value) return
  isLoading.value = true
  try {
    // Thực hiện thao tác thay đổi mật khẩu ở đây nếu cần
    ElNotification({
      title: 'Success',
      message: 'Your password has been changed successfully',
      type: 'success',
      duration: 5000
    })
  } catch (error) {
    ElNotification({
      title: 'Error',
      message: 'There was an error changing your password',
      type: 'error',
      duration: 5000
    })
  } finally {
    isLoading.value = false
  }
}
</script>