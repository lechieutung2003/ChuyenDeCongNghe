<template>
  <div class="space-y-4">
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div>
        <label class="block text-sm font-medium text-gray-700">{{ $t('first_name') }}</label>
        <input
          v-model="employee.first_name"
          :disabled="!isEditMode"
          type="text"
          class="mt-1 w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-50"
        >
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700">{{ $t('last_name') }}</label>
        <input
          v-model="employee.last_name"
          :disabled="!isEditMode"
          type="text"
          class="mt-1 w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-50"
        >
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700">{{ $t('work_email') }}</label>
        <input
          v-model="employee.work_mail"
          :disabled="!isEditMode || !isAdminView"
          type="email"
          :class="[
            'mt-1 w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
            (!isEditMode || !isAdminView) ? 'bg-gray-50 text-gray-500' : ''
          ]"
        >
        <p v-if="!isAdminView" class="text-xs text-gray-500 mt-1">{{ $t('work_email_cannot_be_changed') }}</p>
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700">{{ $t('personal_email') }}</label>
        <input
          v-model="employee.personal_mail"
          :disabled="!isEditMode"
          type="email"
          class="mt-1 w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-50"
        >
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700">{{ $t('phone') }}</label>
        <input
          v-model="employee.phone"
          :disabled="!isEditMode"
          type="text"
          class="mt-1 w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-50"
        >
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700">{{ $t('gender') }}</label>
        <select
          v-model="employee.gender"
          :disabled="!isEditMode"
          class="mt-1 w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-50"
        >
          <option value="">{{ $t('select_gender') }}</option>
          <option value="male">{{ $t('male') }}</option>
          <option value="female">{{ $t('female') }}</option>
        </select>
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700">{{ $t('date_of_birth') }}</label>
        <input
          v-model="employee.date_of_birth"
          :disabled="!isEditMode"
          type="date"
          class="mt-1 w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-50"
        >
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700">{{ $t('join_date') }}</label>
        <input
          v-model="employee.join_date"
          :disabled="!isEditMode || !isAdminView"
          type="date"
          :class="[
            'mt-1 w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
            (!isEditMode || !isAdminView) ? 'bg-gray-50 text-gray-500' : ''
          ]"
        >
        <p v-if="!isAdminView" class="text-xs text-gray-500 mt-1">{{ $t('join_date_cannot_be_changed') }}</p>
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
  isAdminView: boolean
}>()
</script>