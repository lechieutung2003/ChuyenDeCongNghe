<template>
  <div class="p-6">
    <!-- Header -->
    <div class="mb-6">
      <h1 class="text-2xl font-bold text-gray-900">{{ $t('my_profile') }}</h1>
    </div>

    <!-- Employee Profile Component -->
    <EmployeeProfile
      :employee="employee"
      :loading="loading"
      :saving="saving"
      :is-admin-view="false"
      v-model:edit-mode="isEditMode"
      @save="saveProfile"
      @cancel="cancelEdit"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import EmployeeService from '@/services/dss/users/employees'
import EmployeeProfile from '~/components/employee/EmployeeProfile.vue'

definePageMeta({
  layout: 'dss',
  middleware: 'auth'
})

const { t } = useI18n()

// Reactive data
const employee = ref(null)
const loading = ref(false)
const saving = ref(false)
const isEditMode = ref(false)

// Methods
const loadMyProfile = async () => {
  loading.value = true
  try {
    const response = await EmployeeService.getMyProfile()
    console.log('My profile:', response)
    
    if (response) {
      employee.value = response
    } else {
      console.error('No profile data received')
    }
  } catch (error) {
    console.error('Error loading profile:', error)
    
    try {
      console.log('Trying fallback with employees list...')
      const employeesResponse = await EmployeeService.getEmployees()
      console.log('Employees response:', employeesResponse)
      
      if (employeesResponse.results && employeesResponse.results.length > 0) {
        employee.value = employeesResponse.results[0]
      }
    } catch (fallbackError) {
      console.error('Fallback also failed:', fallbackError)
    }
  } finally {
    loading.value = false
  }
}

const saveProfile = async (data: any) => {
  saving.value = true
  try {
    const response = await EmployeeService.updateMyProfile(data)
    employee.value = response
    isEditMode.value = false
    
    alert(t('profile_updated_successfully'))
  } catch (error) {
    console.error('Error saving profile:', error)
    alert(t('error_saving_profile'))
  } finally {
    saving.value = false
  }
}

const cancelEdit = () => {
  isEditMode.value = false
}

// Lifecycle
onMounted(() => {
  loadMyProfile()
})
</script>