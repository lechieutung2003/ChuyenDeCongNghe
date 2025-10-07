<template>
  <tr class="hover:bg-gray-50">
    <!-- Employee Info -->
    <td class="px-6 py-4 whitespace-nowrap">
      <div class="flex items-center">
        <div class="flex-shrink-0 h-10 w-10">
          <img
            v-if="employee.avatar"
            :src="employee.avatar"
            :alt="employee.first_name"
            class="h-10 w-10 rounded-full object-cover"
          >
          <div
            v-else
            class="h-10 w-10 rounded-full bg-gray-300 flex items-center justify-center"
          >
            <span class="text-gray-600 font-medium">
              {{ getInitials(employee.first_name, employee.last_name) }}
            </span>
          </div>
        </div>
        <div class="ml-4">
          <div class="text-sm font-medium text-gray-900">
            {{ employee.first_name }} {{ employee.last_name }}
          </div>
          <div class="text-sm text-gray-500 flex items-center">
            ID:
            <span
              class="ml-1 truncate"
              :title="employee.id"
              style="max-width: 100px; display: inline-block; white-space: nowrap;" 
            >
              {{ employee.id }}
            </span>
          </div>
        </div>
      </div>
    </td>

    <!-- Contact Info -->
    <td class="px-6 py-4 whitespace-nowrap">
      <div class="text-sm text-gray-900">{{ employee.work_mail }}</div>
      <div class="text-sm text-gray-500">{{ employee.phone }}</div>
    </td>

    <!-- Work Info -->
    <td class="px-6 py-4 whitespace-nowrap">
      <div class="text-sm text-gray-900">{{ employee.area || 'N/A' }}</div>
      <div class="text-sm text-gray-500">
        {{ formatWorkingHours(employee.working_start_time, employee.working_end_time) }}
      </div>
      <div class="text-sm text-gray-500">
        {{ $t('salary') }}: {{ formatCurrency(employee.salary) }}
      </div>
    </td>

    <!-- Performance -->
    <td class="px-6 py-4 whitespace-nowrap">
      <div class="text-sm text-gray-900">
        {{ $t('completed_orders') }}: {{ employee.completed_orders_count || 0 }}
      </div>
      <div class="text-sm text-gray-500">
        {{ $t('total_hours') }}: {{ employee.total_hours_worked || 0 }}h
      </div>
    </td>

    <!-- Status -->
    <td class="px-6 py-4 whitespace-nowrap">
      <span :class="getStatusBadgeClass(employee)">
        {{ getStatusText(employee) }}
      </span>
    </td>

    <!-- Actions -->
    <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
      <div class="flex space-x-2">
        <button
          @click="$emit('view', employee)"
          class="text-blue-600 hover:text-blue-900"
        >
          {{ $t('view') }}
        </button>
        <button
          @click="$emit('edit', employee)"
          class="text-green-600 hover:text-green-900"
        >
          {{ $t('edit') }}
        </button>
        <button
          @click="$emit('delete', employee)"
          class="text-red-600 hover:text-red-900"
        >
          {{ $t('delete') }}
        </button>
      </div>
    </td>
  </tr>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

interface Props {
  employee: any
}

defineProps<Props>()

defineEmits<{
  view: [employee: any]
  edit: [employee: any]
  delete: [employee: any]
}>()

// Helper functions
const getInitials = (firstName: string, lastName: string) => {
  const first = firstName?.trim()?.charAt(0)?.toUpperCase() || ''
  const last = lastName?.trim()?.charAt(0)?.toUpperCase() || ''
  return (first + last) || 'N/A'
}

const formatWorkingHours = (startTime: string, endTime: string) => {
  if (!startTime || !endTime) return 'N/A'
  return `${startTime} - ${endTime}`
}

const formatCurrency = (amount: number) => {
  if (!amount) return 'N/A'
  return new Intl.NumberFormat('vi-VN', {
    style: 'currency',
    currency: 'VND',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  }).format(amount)
}

const getActualStatus = (employee: any) => {
  if (!employee?.working_start_time || !employee?.working_end_time) {
    return 0
  }
  return employee.computed_status ?? employee.status ?? 1
}

const getStatusBadgeClass = (employee: any) => {
  const actualStatus = getActualStatus(employee)
  const baseClass = 'inline-flex px-2 py-1 text-xs font-semibold rounded-full'
  
  switch (actualStatus) {
    case 0: return `${baseClass} bg-yellow-100 text-yellow-800`
    case 1: return `${baseClass} bg-green-100 text-green-800`
    case 2: return `${baseClass} bg-red-100 text-red-800`
    default: return `${baseClass} bg-gray-100 text-gray-800`
  }
}

const getStatusText = (employee: any) => {
  if (employee?.status_text) {
    return employee.status_text
  }
  
  const actualStatus = getActualStatus(employee)
  switch (actualStatus) {
    case 0: return t('no_working_hours_set')
    case 1: return t('active')
    case 2: return t('inactive')
    default: return t('unknown')
  }
}
</script>