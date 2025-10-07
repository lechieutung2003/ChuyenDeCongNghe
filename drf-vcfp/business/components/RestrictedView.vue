<template>
  <slot v-if="allScopes && oauthStore.hasAllScopes(allScopes)"></slot>
  <slot v-else-if="oneOfScopes && oauthStore.hasOneOfScopes(oneOfScopes)"></slot>
   <!-- Hiển thị slot nếu là Employee -->
  <slot v-else-if="isEmployee"></slot>
</template>

<script setup lang="ts">
import { useOauthStore } from '@/stores/oauth';
const props = defineProps({
  allScopes: {
    type: [Array, null],
    default: null
  },
  oneOfScopes: {
    type: [Array, null],
    default: null
  },
});

const oauthStore = useOauthStore();

// Thêm computed kiểm tra role Employee (dựa vào scope hoặc roles)
const isEmployee = computed(() => {
  // Kiểm tra theo scope đặc trưng của Employee
  return oauthStore.hasOneOfScopes(['employees:view']);
});
</script>
