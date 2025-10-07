<template>
  <div class="border-b border-gray-200">
    <nav class="-mb-px flex space-x-8 px-6">
      <button
        v-for="tab in tabs"
        :key="tab.key"
        @click="$emit('update:modelValue', tab.key)"
        :class="[
          'py-4 px-1 border-b-2 font-medium text-sm',
          modelValue === tab.key
            ? 'border-blue-500 text-blue-600'
            : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
        ]"
      >
        {{ tab.label }}
      </button>
    </nav>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  tabs: Array<{ key: string, label: string }>,
  modelValue: string
}>()
</script>