<template>
  <div
    v-if="show"
    class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50"
    @click="$emit('close')"
  >
    <div class="relative top-10 mx-auto p-5 border w-full max-w-4xl shadow-lg rounded-md bg-white" @click.stop>
      <div class="mt-3">
        <!-- Modal Header -->
        <div class="flex items-center justify-between pb-4 border-b">
          <h3 class="text-lg font-medium text-gray-900">{{ $t('add_new_employee') }}</h3>
          <button
            @click="$emit('close')"
            class="text-gray-400 hover:text-gray-600"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>

        <!-- Modal Body -->
        <div class="py-4 max-h-[500px] overflow-y-auto">
          <EmployeeForm
            :employee="newEmployee"
            :available-areas="availableAreas"
            :skills-list="skillsList"
            :loading="loading"
            :skills-loading="skillsLoading"
            @submit="$emit('create', $event)"
            @cancel="$emit('close')"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import SkillService from '@/services/dss/users/skill'

const { t } = useI18n()
const skillsList = ref<any[]>([])
const skillsLoading = ref(false)

onMounted(async () => {
  skillsLoading.value = true
  try {
    const result = await SkillService.getSkills()
    console.log('[EmployeeCreateModal] SkillService.getSkills result:', result)
    skillsList.value = Array.isArray(result.results) ? result.results : (Array.isArray(result) ? result : [])
    console.log('[EmployeeCreateModal] skillsList.value:', skillsList.value)
  } catch (e) {
    console.error('[EmployeeCreateModal] Error loading skills:', e)
    skillsList.value = []
  }
  skillsLoading.value = false
})

interface Props {
  show: boolean
  newEmployee: any
  availableAreas: any[]
  loading: boolean
}

defineProps<Props>()

defineEmits<{
  close: []
  create: [data: any]
}>()
</script>