<template>
  <div class="space-y-6">
    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center items-center py-8">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
    </div>

    <!-- Employee Profile -->
    <div v-else-if="employee" class="space-y-6">
      <!-- Header Card -->
      <ProfileHeader
        :employee="employee"
        :is-edit-mode="isEditMode"
        :is-admin-view="isAdminView"
        :saving="saving"
        :get-status-badge-class="getStatusBadgeClass"
        :get-status-text="getStatusText"
        :get-current-time="getCurrentTime"
        @toggle-edit="toggleEditMode"
        @save="handleSave"
        @cancel="handleCancel"
      />

      <!-- Profile Information Tabs -->
      <div class="bg-white rounded-lg shadow">
        <!-- Tab Navigation -->
        <TabNavigation
          :tabs="tabs"
          :model-value="activeTab"
          @update:model-value="activeTab = $event"
        />

        <!-- Tab Content -->
        <div class="p-6">
          <!-- Personal Information -->
          <PersonalInfoTab
            v-if="activeTab === 'personal'"
            :employee="editableEmployee"
            :is-edit-mode="isEditMode"
            :is-admin-view="isAdminView"
          />

          <!-- Work Information -->
          <WorkInfoTab
            v-if="activeTab === 'work'"
            :employee="editableEmployee"
            :is-edit-mode="isEditMode"
            :is-admin-view="isAdminView"
            :skills-list="skillsList"
            :skills-loading="skillsLoading"
            :show-skill-dropdown="showSkillDropdown"
            :toggle-skill-dropdown="toggleSkillDropdown"
            :select-skill="selectSkill"
            :get-status-card-class="getStatusCardClass"
            :get-status-text-class="getStatusTextClass"
            :get-status-icon-class="getStatusIconClass"
            :get-status-text="getStatusText"
            :get-status-description="getStatusDescription"
            @set-day-off="setDayOff"
            @validate-working-hours="validateWorkingHours"
          />

          <!-- Performance -->
          <PerformanceTab
            v-if="activeTab === 'performance'"
            :employee="employee"
            :calculate-average-hours-per-order="calculateAverageHoursPerOrder"
          />
        </div>
      </div>
    </div>

    <!-- Error State -->
    <div v-else class="text-center py-8">
      <h3 class="text-lg font-medium text-gray-900">
        {{ isAdminView ? $t('employee_not_found') : $t('profile_not_found') }}
      </h3>
      <p class="text-gray-500">
        {{ isAdminView ? $t('employee_not_found_description') : $t('cannot_load_profile') }}
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router' 
import { useI18n } from 'vue-i18n'
import SkillService from '@/services/dss/users/skill'
import ProfileHeader from './profile/ProfileHeader.vue'
import TabNavigation from './profile/TabNavigation.vue'
import PersonalInfoTab from './profile/PersonalInfoTab.vue'
import WorkInfoTab from './profile/WorkInfoTab.vue'
import PerformanceTab from './profile/PerformanceTab.vue'
import EmployeeService from '@/services/dss/users/employees'

const { t } = useI18n()

interface Props {
  employee?: any
  loading?: boolean
  saving?: boolean
  isAdminView?: boolean
  editMode?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  employee: null,
  loading: false,
  saving: false,
  isAdminView: false,
  editMode: false
})

const emit = defineEmits<{
  save: [data: any]
  cancel: []
  'update:editMode': [value: boolean]
}>()

const editableEmployee = ref({})
const isEditMode = ref(props.editMode)
const activeTab = ref('personal')
const skillsList = ref([])
const skillsLoading = ref(false)
const showSkillDropdown = ref(false)
const loading = ref(false)
const employee = ref(null)
const route = useRoute()

const currentTime = ref(new Date())
let timeInterval: NodeJS.Timeout | null = null

const tabs = computed(() => [
  { key: 'personal', label: t('personal_information') },
  { key: 'work', label: t('work_information') },
  { key: 'performance', label: t('performance') }
])

watch(() => props.employee, (newEmployee) => {
  if (newEmployee) {
    editableEmployee.value = { ...newEmployee }
    if (!Array.isArray(editableEmployee.value.skills)) {
      editableEmployee.value.skills = []
    }
  }
}, { immediate: true })

watch(() => props.editMode, (newValue) => {
  isEditMode.value = newValue
})

watch(() => isEditMode.value, (newValue) => {
  if (newValue && props.isAdminView) {
    loadSkills()
  }
})

const loadSkills = async () => {
  try {
    const response = await SkillService.getSkills()
    skillsList.value = response.results || []
  } catch (error) {
    skillsList.value = []
  }
}

const loadEmployee = async (employeeId: string) => {
  loading.value = true
  try {
    const response = await EmployeeService.getEmployee(employeeId)
    employee.value = response
    console.log('Thông tin chi tiết employee:', response)
  } catch (error) {
    employee.value = null
    console.error('Lỗi lấy thông tin employee:', error)
  } finally {
    loading.value = false
  }
}



const toggleSkillDropdown = () => {
  showSkillDropdown.value = !showSkillDropdown.value
}

const selectSkill = async (skillName: string) => {
  if (!Array.isArray(editableEmployee.value.skills)) {
    editableEmployee.value.skills = []
  }
  const index = editableEmployee.value.skills.indexOf(skillName)
  if (index > -1) {
    editableEmployee.value.skills.splice(index, 1)
  } else {
    editableEmployee.value.skills.push(skillName)
  }
  
  // Update realtime to EmployeeSkill table
  try {
    await EmployeeService.updateEmployee(props.employee.id, { skills: editableEmployee.value.skills })
    // Optional: Show success message or handle response
  } catch (error) {
    console.error('Error updating skills:', error)
    // Optional: Revert local change if API fails
    if (index > -1) {
      editableEmployee.value.skills.push(skillName)
    } else {
      editableEmployee.value.skills.splice(editableEmployee.value.skills.indexOf(skillName), 1)
    }
  }
}

const getActualStatus = () => {
  const emp = props.employee || editableEmployee.value
  if (!emp?.working_start_time || !emp?.working_end_time) {
    return 0
  }
  return emp.computed_status ?? emp.status ?? 1
}

const getStatusBadgeClass = () => {
  const actualStatus = getActualStatus()
  const baseClass = 'inline-flex px-2 py-1 text-xs font-semibold rounded-full'
  switch (actualStatus) {
    case 0: return `${baseClass} bg-yellow-100 text-yellow-800`
    case 1: return `${baseClass} bg-green-100 text-green-800`
    case 2: return `${baseClass} bg-red-100 text-red-800`
    default: return `${baseClass} bg-gray-100 text-gray-800`
  }
}

const getStatusCardClass = () => {
  const actualStatus = getActualStatus()
  switch (actualStatus) {
    case 0: return 'border-yellow-200 bg-yellow-50'
    case 1: return 'border-green-200 bg-green-50'
    case 2: return 'border-red-200 bg-red-50'
    default: return 'border-gray-200 bg-gray-50'
  }
}

const getStatusTextClass = () => {
  const actualStatus = getActualStatus()
  switch (actualStatus) {
    case 0: return 'text-yellow-700'
    case 1: return 'text-green-700'
    case 2: return 'text-red-700'
    default: return 'text-gray-700'
  }
}

const getStatusIconClass = () => {
  const actualStatus = getActualStatus()
  const baseClass = 'w-4 h-4 rounded-full'
  switch (actualStatus) {
    case 0: return `${baseClass} bg-yellow-500`
    case 1: return `${baseClass} bg-green-500`
    case 2: return `${baseClass} bg-red-500`
    default: return `${baseClass} bg-gray-500`
  }
}

const getStatusText = () => {
  if (props.employee?.status_text) {
    return props.employee.status_text
  }
  const emp = props.employee || editableEmployee.value
  if (!emp?.working_start_time || !emp?.working_end_time) {
    return t('no_working_hours_set')
  }
  return t('status_will_be_calculated')
}

const getStatusDescription = () => {
  const emp = props.employee || editableEmployee.value
  if (!emp?.working_start_time || !emp?.working_end_time) {
    return t('please_set_working_hours')
  }
  return t('status_auto_updated_by_system')
}

const getCurrentTime = () => {
  const now = currentTime.value
  const options: Intl.DateTimeFormatOptions = {
    timeZone: 'Asia/Ho_Chi_Minh',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: false
  }
  return new Intl.DateTimeFormat('en-GB', options).format(now)
}

const updateCurrentTime = () => {
  currentTime.value = new Date()
}

const startTimeUpdate = () => {
  updateCurrentTime()
  timeInterval = setInterval(updateCurrentTime, 1000)
}

const stopTimeUpdate = () => {
  if (timeInterval) {
    clearInterval(timeInterval)
    timeInterval = null
  }
}

const toggleEditMode = () => {
  isEditMode.value = !isEditMode.value
  emit('update:editMode', isEditMode.value)
}

const handleSave = () => {
  if (!validateWorkingHours()) {
    return
  }
  let dataToSave = { ...editableEmployee.value }
  if (!props.isAdminView) {
    dataToSave = {
      first_name: editableEmployee.value.first_name,
      last_name: editableEmployee.value.last_name,
      personal_mail: editableEmployee.value.personal_mail,
      phone: editableEmployee.value.phone,
      gender: editableEmployee.value.gender,
      date_of_birth: editableEmployee.value.date_of_birth,
      area: editableEmployee.value.area,
      skills: editableEmployee.value.skills,
      working_start_time: editableEmployee.value.working_start_time,
      working_end_time: editableEmployee.value.working_end_time
    }
  }
  emit('save', dataToSave)
}

const handleCancel = () => {
  if (props.employee) {
    editableEmployee.value = { ...props.employee }
    if (!Array.isArray(editableEmployee.value.skills)) {
      editableEmployee.value.skills = []
    }
  }
  isEditMode.value = false
  emit('update:editMode', false)
  emit('cancel')
}

const validateWorkingHours = () => {
  const startTime = editableEmployee.value.working_start_time
  const endTime = editableEmployee.value.working_end_time
  if ((startTime && !endTime) || (!startTime && endTime)) {
    alert(t('both_start_end_time_required'))
    return false
  }
  if (startTime && endTime && startTime === endTime) {
    alert(t('start_end_time_cannot_be_same'))
    return false
  }
  return true
}

const setDayOff = () => {
  editableEmployee.value.working_start_time = null
  editableEmployee.value.working_end_time = null
}

const getInitials = (firstName: string, lastName: string) => {
  return `${firstName?.charAt(0) || ''}${lastName?.charAt(0) || ''}`.toUpperCase()
}

const calculateAverageHoursPerOrder = () => {
  if (!props.employee || props.employee.completed_orders_count === 0) return 0
  return (props.employee.total_hours_worked / props.employee.completed_orders_count).toFixed(1)
}

onMounted(() => {
  if (props.employee) {
    editableEmployee.value = { ...props.employee }
    if (!Array.isArray(editableEmployee.value.skills)) {
      editableEmployee.value.skills = []
    }
  }

  const employeeId = route.params.id // hoặc lấy từ nguồn khác
  if (employeeId) {
    loadEmployee(employeeId)
  }
  startTimeUpdate()
})

onUnmounted(() => {
  stopTimeUpdate()
})
</script>