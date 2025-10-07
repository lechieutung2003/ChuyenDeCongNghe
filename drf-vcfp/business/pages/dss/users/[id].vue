<template>
  <div class="p-6 mt-7">
    <!-- Back Button -->
    <div class="mb-15">
      <BackButton @click="$router.push('/dss/users')" />
    </div>

    <div class="mt-10">
    <!-- Employee Profile Component -->
    <EmployeeProfile
      :employee="employee"
      :loading="loading"
      :saving="saving"
      :is-admin-view="true"
      v-model:edit-mode="isEditMode"
      @save="saveEmployee"
      @cancel="cancelEdit"
    />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import EmployeeService from '@/services/dss/users/employees'
import BackButton from '@/components/BackButton.vue'
import EmployeeProfile from '~/components/employee/EmployeeProfile.vue'

definePageMeta({
  layout: 'dss',
  middleware: 'auth'
})

const { t } = useI18n()
const route = useRoute()
const router = useRouter()

// Reactive data
const employee = ref(null)
const loading = ref(false)
const saving = ref(false)
const isEditMode = ref(false)

// Methods
const loadEmployee = async () => {
  loading.value = true
  try {
    const response = await EmployeeService.getEmployee(route.params.id)
    employee.value = response
    
    // Check if edit mode from query
    if (route.query.edit === 'true') {
      isEditMode.value = true
    }
  } catch (error) {
    console.error('Error loading employee:', error)
  } finally {
    loading.value = false
  }
}

const saveEmployee = async (data: any) => {
  saving.value = true
  try {
    const response = await EmployeeService.updateEmployee(route.params.id, data)
    employee.value = response
    isEditMode.value = false
    alert(t('employee_updated_successfully'))
  } catch (error) {
    console.error('Error saving employee:', error)
    alert(t('error_saving_employee'))
  } finally {
    saving.value = false
  }
}

const cancelEdit = () => {
  isEditMode.value = false
}

// Lifecycle
onMounted(() => {
  loadEmployee()
})
</script>