<template>
  <div
    v-if="show"
    class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50"
    @click="$emit('close')"
  >
    <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white" @click.stop>
      <div class="mt-3 text-center">
        <div class="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-red-100">
          <svg class="h-6 w-6 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.732-.833-2.5 0L4.268 15.5c-.77.833.192 2.5 1.732 2.5z" />
          </svg>
        </div>
        <h3 class="text-lg font-medium text-gray-900 mt-2">{{ $t('confirm_delete') }}</h3>
        <div class="mt-2 px-7 py-3">
          <p class="text-sm text-gray-500">
            {{ $t('confirm_delete_employee_message', { 
              name: `${employee?.first_name} ${employee?.last_name}` 
            }) }}
          </p>
          <p class="text-xs text-red-500 mt-2">
            {{ $t('this_action_cannot_be_undone') }}
          </p>
        </div>
        <div class="items-center px-4 py-3">
          <div class="flex space-x-3">
            <button
              @click="$emit('confirm')"
              :disabled="loading"
              class="w-full px-4 py-2 bg-red-600 text-white text-base font-medium rounded-md shadow-sm hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 disabled:opacity-50"
            >
              {{ loading ? $t('deleting') : $t('delete') }}
            </button>
            <button
              @click="$emit('close')"
              :disabled="loading"
              class="w-full px-4 py-2 bg-gray-300 text-gray-700 text-base font-medium rounded-md shadow-sm hover:bg-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-500 disabled:opacity-50"
            >
              {{ $t('cancel') }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

interface Props {
  show: boolean
  employee: any
  loading: boolean
}

defineProps<Props>()

defineEmits<{
  close: []
  confirm: []
}>()
</script>