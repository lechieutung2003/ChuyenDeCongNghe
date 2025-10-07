<template>
  <div class="space-y-3 max-h-[calc(100vh-450px)] overflow-y-auto">
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div>
        <label class="block text-sm font-medium text-gray-700">{{ $t('area') }}</label>
        <input
          v-model="employee.area"
          :disabled="!isEditMode"
          type="text"
          class="mt-1 w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-50"
          :placeholder="$t('enter_work_area')"
        >
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700">{{ $t('salary') }}</label>
        <input
          v-model="employee.salary"
          :disabled="!isEditMode || !isAdminView"
          type="number"
          step="0.01"
          :class="[
            'mt-1 w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
            (!isEditMode || !isAdminView) ? 'bg-gray-50 text-gray-500' : ''
          ]"
        >
        <p v-if="!isAdminView" class="text-xs text-gray-500 mt-1">{{ $t('salary_managed_by_admin') }}</p>
      </div>
      <div v-if="isAdminView" class="relative">
        <label class="block text-sm font-medium text-gray-700">{{ $t('skills') }}</label>
        <div
          class="flex items-center justify-between border px-3 py-2 rounded-md cursor-pointer"
          :class="[
            'mt-1 w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
            (!isEditMode || !isAdminView) ? 'bg-gray-50 text-gray-500 cursor-not-allowed' : 'bg-white'
          ]"
          @click="isEditMode && toggleSkillDropdown()"
        >
          <span :class="{ 'text-gray-500': !isEditMode || !isAdminView }">
            <template v-if="employee.skills && employee.skills.length">
              {{ employee.skills.join(', ') }}
            </template>
            <template v-else>
              {{ $t('select_skills') }}
            </template>
          </span>
          <svg v-if="isEditMode" class="w-4 h-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
          </svg>
        </div>
        <div
          v-if="showSkillDropdown && isEditMode"
          class="absolute z-10 mt-1 w-full bg-white border rounded-md shadow-lg max-h-60 overflow-auto"
          @click.stop
        >
          <div v-if="skillsLoading" class="p-2 text-gray-500">{{ $t('loading') }}</div>
          <div
            v-for="skill in skillsList"
            :key="skill.id"
            class="px-3 py-2 hover:bg-blue-50 cursor-pointer flex items-center"
            @click="selectSkill(skill.name)"
          >
            <input
              type="checkbox"
              :checked="employee.skills.includes(skill.name)"
              @change="selectSkill(skill.name)"
              class="mr-2"
            />
            {{ skill.name }}
          </div>
        </div>
        <!-- Hiển thị kỹ năng thực tế của nhân viên -->
        <!-- <div v-if="employee.skills && employee.skills.length" class="mt-2 flex flex-wrap gap-2">
          <label class="block text-sm font-medium text-gray-700 mb-1">{{ $t('skills') }}</label>
          <span
            v-for="skill in employee.skills"
            :key="skill"
            class="inline-block bg-green-100 text-green-700 px-2 py-1 rounded text-xs"
          >
            {{ skill }}
          </span>
        </div> -->
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700">{{ $t('working_start_time') }}</label>
        <input
          v-model="employee.working_start_time"
          :disabled="!isEditMode"
          type="time"
          class="mt-1 w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-50"
          @change="$emit('validate-working-hours')"
        >
        <p class="text-xs text-gray-500 mt-1">{{ $t('status_auto_calculated') }}</p>
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700">{{ $t('working_end_time') }}</label>
        <input
          v-model="employee.working_end_time"
          :disabled="!isEditMode"
          type="time"
          class="mt-1 w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-50"
          @change="$emit('validate-working-hours')"
        >
        <p class="text-xs text-gray-500 mt-1">{{ $t('status_auto_calculated') }}</p>
      </div>
    </div>
    <div class="col-span-1 md:col-span-2 flex justify-end">
      <button
        v-if="isEditMode"
        @click="$emit('set-day-off')"
        class="flex items-center gap-2 bg-yellow-500 hover:bg-yellow-600 text-white px-6 py-2 rounded-lg shadow transition-all duration-150 mt-2"
      >
        <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4"></path>
        </svg>
        {{ $t('set_day_off') }}
      </button>
    </div>
    <div class="mt-6 p-4 rounded-lg" :class="getStatusCardClass()">
      <div class="flex items-center justify-between">
        <div>
          <h4 class="font-medium" :class="getStatusTextClass()">
            {{ $t('working_status') }}
          </h4>
          <p class="text-sm" :class="getStatusTextClass()">
            {{ getStatusText() }}
          </p>
          <p class="text-xs mt-1" :class="getStatusTextClass()">
            {{ getStatusDescription() }}
          </p>
        </div>
        <div class="flex items-center">
          <div :class="getStatusIconClass()"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import EmployeeService from '@/services/dss/users/employees'

const { t } = useI18n()
defineProps<{
  employee: any,
  isEditMode: boolean,
  isAdminView: boolean,
  skillsList: any[],
  skillsLoading: boolean,
  showSkillDropdown: boolean,
  toggleSkillDropdown: () => void,
  selectSkill: (skillName: string) => void,
  getStatusCardClass: () => string,
  getStatusTextClass: () => string,
  getStatusIconClass: () => string,
  getStatusText: () => string,
  getStatusDescription: () => string
}>()
</script>