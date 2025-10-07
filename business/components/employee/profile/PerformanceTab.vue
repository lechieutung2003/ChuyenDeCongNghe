<template>
  <div class="space-y-4">
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
      <div class="bg-blue-50 p-4 rounded-lg">
        <div class="text-2xl font-bold text-blue-600">{{ employee.completed_orders_count || 0 }}</div>
        <div class="text-sm text-gray-600">{{ $t('completed_orders') }}</div>
      </div>
      <div class="bg-green-50 p-4 rounded-lg">
        <div class="text-2xl font-bold text-green-600">{{ employee.total_hours_worked || 0 }}h</div>
        <div class="text-sm text-gray-600">{{ $t('total_hours_worked') }}</div>
      </div>
      <div class="bg-purple-50 p-4 rounded-lg">
        <div class="text-2xl font-bold text-purple-600">
          {{ calculateAverageHoursPerOrder() }}h
        </div>
        <div class="text-sm text-gray-600">{{ $t('avg_hours_per_order') }}</div>
      </div>
    </div>
    <div class="mt-6 p-6 border-2 border-dashed border-gray-300 rounded-lg text-center">
      <p class="text-gray-500">{{ $t('performance_charts_coming_soon') }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'
const { t } = useI18n()
defineProps<{
  employee: any,
  calculateAverageHoursPerOrder: () => string | number
}>()
</script>