<template>
  <form @submit.prevent="handleSubmit">
    <!-- Personal Information Section -->
    <div class="mb-6">
      <h4 class="text-md font-medium text-gray-900 mb-3">{{ $t('personal_information') }}</h4>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            {{ $t('first_name') }} <span class="text-red-500">*</span>
          </label>
          <input
            v-model="localEmployee.first_name"
            type="text"
            required
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            :placeholder="$t('enter_first_name')"
          >
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            {{ $t('last_name') }} <span class="text-red-500">*</span>
          </label>
          <input
            v-model="localEmployee.last_name"
            type="text"
            required
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            :placeholder="$t('enter_last_name')"
          >
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            {{ $t('work_email') }} <span class="text-red-500">*</span>
          </label>
          <input
            v-model="localEmployee.work_mail"
            type="email"
            required
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            :placeholder="$t('enter_work_email')"
          >
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            {{ $t('phone') }} <span class="text-red-500">*</span>
          </label>
          <input
            v-model="localEmployee.phone"
            type="tel"
            required
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            :placeholder="$t('enter_phone')"
          >
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">{{ $t('personal_email') }}</label>
          <input
            v-model="localEmployee.personal_mail"
            type="email"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            :placeholder="$t('enter_personal_email')"
          >
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">{{ $t('gender') }}</label>
          <select
            v-model="localEmployee.gender"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">{{ $t('select_gender') }}</option>
            <option value="male">{{ $t('male') }}</option>
            <option value="female">{{ $t('female') }}</option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">{{ $t('date_of_birth') }}</label>
          <input
            v-model="localEmployee.date_of_birth"
            type="date"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">{{ $t('join_date') }}</label>
          <input
            v-model="localEmployee.join_date"
            type="date"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
        </div>
      </div>
    </div>

    <!-- Work Information Section -->
    <div class="mb-6">
      <h4 class="text-md font-medium text-gray-900 mb-3">{{ $t('work_information') }}</h4>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 max-w-4xl">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">{{ $t('area') }}</label>
          <input
            v-model="localEmployee.area"
            type="text"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            :placeholder="$t('enter_area')"
          >
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">{{ $t('salary') }}</label>
          <input
            v-model="localEmployee.salary"
            type="number"
            step="0.01"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            :placeholder="$t('enter_salary')"
          >
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">{{ $t('working_start_time') }}</label>
          <input
            v-model="localEmployee.working_start_time"
            type="time"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">{{ $t('working_end_time') }}</label>
          <input
            v-model="localEmployee.working_end_time"
            type="time"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
        </div>
      </div>
       
      <!-- Skills Dropdown Multi-select -->
      <div class="relative mt-4">
        <label class="block text-sm font-medium text-gray-700 mb-1">{{ $t('skills') }}</label>
        <div
          class="flex items-center justify-between border px-3 py-2 rounded-md cursor-pointer"
          :class="['w-full', 'border-gray-300', 'focus:outline-none', 'focus:ring-2', 'focus:ring-blue-500', 'bg-white']"
          @click="showSkillDropdown = !showSkillDropdown"
        >
          <span>
            <template v-if="localEmployee.skills && localEmployee.skills.length">
              {{ localEmployee.skills.join(', ') }}
            </template>
            <template v-else>
              {{ $t('select_skills') }}
            </template>
          </span>
          <svg class="w-4 h-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
          </svg>
        </div>
        <div
          v-if="showSkillDropdown"
          class="absolute z-10 mt-1 w-full bg-white border rounded-md shadow-lg max-h-60 overflow-auto"
          @click.stop
        >
          <div
            v-for="skill in props.skillsList"
            :key="skill.id"
            class="px-3 py-2 hover:bg-blue-50 cursor-pointer flex items-center"
            @click="toggleSkill(skill.name)"
          >
            <input
              type="checkbox"
              :checked="localEmployee.skills.includes(skill.name)"
              @change="toggleSkill(skill.name)"
              class="mr-2"
            />
            {{ skill.name }}
          </div>
        </div>

        
      </div>
    </div>

    <!-- Modal Footer -->
    <div class="flex items-center justify-end pt-4 border-t space-x-3">
      <button
        type="button"
        @click="$emit('cancel')"
        :disabled="loading"
        class="px-4 py-2 bg-gray-300 text-gray-700 text-base font-medium rounded-md shadow-sm hover:bg-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-500 disabled:opacity-50"
      >
        {{ $t('cancel') }}
      </button>
      <button
        type="submit"
        :disabled="loading"
        class="px-4 py-2 bg-blue-600 text-white text-base font-medium rounded-md shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
      >
        {{ loading ? $t('creating') : $t('create_employee') }}
      </button>
    </div>
  </form>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import EmployeeService from '@/services/dss/users/employees'


const { t } = useI18n()

interface Props {
  employee: any
  availableAreas: any[]
  loading: boolean
  skillsList: any[]
  skillsLoading: boolean
}

const props = defineProps<Props>()

const emit = defineEmits<{
  submit: [data: any]
  cancel: []
}>()

const localEmployee = ref({
  ...props.employee,
  skills: props.employee?.skills ? [...props.employee.skills] : []
})


watch(() => props.employee, (newEmployee) => {
  localEmployee.value = {
    ...newEmployee,
    skills: newEmployee?.skills ? [...newEmployee.skills] : []
  }
}, { deep: true })

console.log('[EmployeeForm] props.skillsList:', props.skillsList)

const handleSubmit = () => {
  const payload = {
    ...localEmployee.value,
    skills: Array.isArray(localEmployee.value.skills) ? localEmployee.value.skills : []
  }
    console.log('Payload gửi lên backend:', payload) 
  emit('submit', payload)
}

const showSkillDropdown = ref(false)

function toggleSkill(skillName: string) {
  // Đảm bảo luôn có mảng skills
  if (!Array.isArray(localEmployee.value.skills)) {
    localEmployee.value.skills = []
  }
  const idx = localEmployee.value.skills.indexOf(skillName)
  if (idx === -1) {
    localEmployee.value.skills.push(skillName)
  } else {
    localEmployee.value.skills.splice(idx, 1)
  }
  // Nếu đã có employeeId (edit), thì update realtime
  if (localEmployee.value.id) {
    EmployeeService.updateEmployee(localEmployee.value.id, { skills: localEmployee.value.skills })
      .then(() => {})
      .catch((error) => {
        console.error('Error updating skills:', error)
      })
  }
}
</script>