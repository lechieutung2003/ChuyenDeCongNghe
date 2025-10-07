<template>
  <div v-if="totalPages > 1" class="bg-gray-50 px-6 py-3">
    <div class="flex items-center justify-between">
      <div class="text-sm text-gray-700">
        {{ $t('showing') }} {{ (currentPage - 1) * pageSize + 1 }} {{ $t('to') }} 
        {{ Math.min(currentPage * pageSize, totalItems) }} {{ $t('of') }} {{ totalItems }} {{ $t('results') }}
      </div>
      <div class="flex space-x-2">
        <button
          @click="$emit('page-change', currentPage - 1)"
          :disabled="currentPage === 1"
          class="px-3 py-1 border border-gray-300 rounded-md disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
        >
          {{ $t('previous') }}
        </button>
        <button
          v-for="page in visiblePages"
          :key="page"
          @click="$emit('page-change', page)"
          :class="[
            'px-3 py-1 border rounded-md',
            page === currentPage
              ? 'bg-blue-600 border-blue-600 text-white'
              : 'border-gray-300 hover:bg-gray-50'
          ]"
        >
          {{ page }}
        </button>
        <button
          @click="$emit('page-change', currentPage + 1)"
          :disabled="currentPage === totalPages"
          class="px-3 py-1 border border-gray-300 rounded-md disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
        >
          {{ $t('next') }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

interface Props {
  currentPage: number
  pageSize: number
  totalItems: number
  totalPages: number
}

const props = defineProps<Props>()

defineEmits<{
  'page-change': [page: number]
}>()

const visiblePages = computed(() => {
  const pages = []
  const start = Math.max(1, props.currentPage - 2)
  const end = Math.min(props.totalPages, props.currentPage + 2)
  
  for (let i = start; i <= end; i++) {
    pages.push(i)
  }
  return pages
})
</script>