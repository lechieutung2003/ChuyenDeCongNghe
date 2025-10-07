<template>
  <NuxtLoadingIndicator />
  <div class="h-screen w-full flex justify-center items-center bg-gray-50">
    <div class="form drop-shadow-md">
      <div class="form-header">
        <h1 class="form-title">{{ $t('Forgot your password?') }}</h1>
        <p class="form-subtitle" v-if="isSubmitted">
          {{ $t('Password reset link sent to', { email: forgotPasswordForm.email }) }}
        </p>
      </div>
      <form @submit.prevent="sendLink">
        <div class="flex-column">
          <label for="email">{{ $t('Email') }}</label>
        </div>
        <div class="inputForm" :class="{ 'error-border': emailError }">
          <svg height="20" viewBox="0 0 32 32" width="20" xmlns="http://www.w3.org/2000/svg">
            <g id="Layer_3" data-name="Layer 3">
              <path d="m30.853 13.87a15 15 0 0 0 -29.729 4.082 15.1 15.1 0 0 0 12.876 12.918 15.6 15.6 0 0 0 2.016.13 14.85 14.85 0 0 0 7.715-2.145 1 1 0 1 0 -1.031-1.711 13.007 13.007 0 1 1 5.458-6.529 2.149 2.149 0 0 1 -4.158-.759v-10.856a1 1 0 0 0 -2 0v1.726a8 8 0 1 0 .2 10.325 4.135 4.135 0 0 0 7.83.274 15.2 15.2 0 0 0 .823-7.455zm-14.853 8.13a6 6 0 1 1 6-6 6.006 6.006 0 0 1 -6 6z"></path>
            </g>
          </svg>
          <input
            id="email"
            v-model="forgotPasswordForm.email"
            type="email"
            class="input"
            :placeholder="$t('Email')"
            required
            @blur="validateEmail"
            @input="validateEmail"
          />
        </div>
        <div v-if="emailError" class="error-text">{{ emailError }}</div>
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
          <span v-if="isLoading">{{ $t('Sending...') }}</span>
          <span v-else>{{ $t('Send reset link') }}</span>
        </button>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import OAuthService from '@/services/oauth'
import { ElNotification } from 'element-plus'
import { ref, watch } from 'vue'
import '@/assets/css/form.css'

definePageMeta({
  layout: 'anonymous'
})

const forgotPasswordForm = ref({
  email: ''
})

const isSubmitted = ref(false)
const isLoading = ref(false)
const emailError = ref('')
const isFormValid = ref(false)

function validateEmail() {
  const email = forgotPasswordForm.value.email
  if (!email) {
    emailError.value = 'Please enter your email'
    isFormValid.value = false
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    emailError.value = 'Invalid email format'
    isFormValid.value = false
  } else {
    emailError.value = ''
    isFormValid.value = true
  }
}

watch(() => forgotPasswordForm.value.email, validateEmail)

const sendLink = async () => {
  validateEmail()
  if (!isFormValid.value) return
  isLoading.value = true
  try {
    await OAuthService.forgotPassword({ email: forgotPasswordForm.value.email })
    isSubmitted.value = true
    ElNotification({
      title: 'Success',
      message: 'Password reset link sent successfully',
      type: 'success',
      duration: 5000
    })
  } catch (error) {
    ElNotification({
      title: 'Error',
      message: 'Email does not exist or there was an error sending the reset link',
      type: 'error',
      duration: 5000
    })
  } finally {
    isLoading.value = false
  }
}
</script>