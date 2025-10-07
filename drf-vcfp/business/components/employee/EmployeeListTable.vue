<template>
  <div class="bg-white rounded-lg shadow overflow-hidden">
    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center items-center py-8">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
    </div>

    <!-- Table -->
    <div v-else class="overflow-x-auto">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              {{ $t('employee') }}
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              {{ $t('contact') }}
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              {{ $t('work_info') }}
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              {{ $t('performance') }}
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              {{ $t('status') }}
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              {{ $t('actions') }}
            </th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <EmployeeTableRow
            v-for="employee in employees"
            :key="employee.id"
            :employee="employee"
            @view="$emit('view', $event)"
            @edit="$emit('edit', $event)"
            @delete="$emit('delete', $event)"
          />
        </tbody>
      </table>

      <!-- Empty State -->
      <div v-if="!loading && employees.length === 0" class="text-center py-8">
        <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
        </svg>
        <h3 class="mt-2 text-sm font-medium text-gray-900">{{ $t('no_employees') }}</h3>
        <p class="mt-1 text-sm text-gray-500">{{ $t('no_employees_description') }}</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

interface Props {
  employees: any[]
  loading: boolean
}

defineProps<Props>()

defineEmits<{
  view: [employee: any]
  edit: [employee: any] 
  delete: [employee: any]
}>()
</script>