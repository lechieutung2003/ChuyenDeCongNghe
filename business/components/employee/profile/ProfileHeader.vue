<template>
  <div class="bg-white rounded-lg shadow p-6">
    <div class="flex items-center justify-between">
      <div class="flex items-center space-x-4">
        <div class="flex-shrink-0">
          <img
            v-if="employee.avatar"
            :src="employee.avatar"
            :alt="employee.first_name"
            class="h-20 w-20 rounded-full object-cover"
          >
          <div v-else class="h-20 w-20 rounded-full bg-gray-300 flex items-center justify-center">
            <span class="text-gray-600 text-xl font-medium">
              {{ getInitials(employee.first_name, employee.last_name) }}
            </span>
          </div>
        </div>
        <div>
          <h2 class="text-2xl font-bold text-gray-900">
            {{ employee.first_name }} {{ employee.last_name }}
          </h2>
          <p class="text-gray-600">{{ employee.work_mail }}</p>
          <div class="flex items-center space-x-2 mt-2">
            <span :class="getStatusBadgeClass()">
              {{ getStatusText() }}
            </span>
            <div class="inline-flex items-center px-2 py-1 text-xs font-medium rounded bg-gray-100 text-gray-600 space-x-1">
              <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
              <span>{{ getCurrentTime() }}</span>
              <span class="text-gray-400">ICT</span>
            </div>
          </div>
        </div>
      </div>
      <div class="flex space-x-2">
        <button
          v-if="!isEditMode"
          @click="$emit('toggle-edit')"
          class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg"
        >
          {{ isAdminView ? $t('edit') : $t('edit_profile') }}
        </button>
        <template v-else>
          <button
            @click="$emit('save')"
            :disabled="saving"
            class="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg disabled:opacity-50"
          >
            {{ saving ? $t('saving') : $t('save') }}
          </button>
          <button
            @click="$emit('cancel')"
            class="bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded-lg"
          >
            {{ $t('cancel') }}
          </button>
        </template>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'
const { t } = useI18n()
defineProps<{
  employee: any,
  isEditMode: boolean,
  isAdminView: boolean,
  saving: boolean,
  getStatusBadgeClass: () => string,
  getStatusText: () => string,
  getCurrentTime: () => string
}>()
const getInitials = (firstName: string, lastName: string) =>
  `${firstName?.charAt(0) || ''}${lastName?.charAt(0) || ''}`.toUpperCase()
</script>