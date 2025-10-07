<template>
    <Employee />
</template>

<script setup>
import Employee from './employee.vue'
definePageMeta({
  layout: 'dss',
  middleware: 'auth'
})
</script>