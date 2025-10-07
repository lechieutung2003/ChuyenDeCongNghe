<template>
  <div class="p-6">
    <!-- Header -->
    <div class="flex justify-between items-center mb-6">
      <button 
        @click="showCreateModal = true"
        class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg flex items-center gap-2"
      >
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"/>
        </svg>
        {{ $t('add_employee') }}
      </button>
    </div>

    <!-- Filters Component -->
    <EmployeeFilters
      :filters="filters"
      :areas="areas"
      @update:search="handleSearchUpdate"
      @update:area="updateFilters('area', $event)"
      @update:status="updateFilters('status', $event)"
      @reset="resetFilters"
    />

    <!-- Employee Table Component -->
    <EmployeeListTable
      :employees="employees"
      :loading="loading"
      @view="viewEmployee"
      @edit="editEmployee"
      @delete="confirmDeleteEmployee"
    />

    <!-- Pagination Component -->
    <Pagination
      :current-page="currentPage"
      :page-size="pageSize"
      :total-items="totalItems"
      :total-pages="totalPages"
      @page-change="goToPage"
    />

    <!-- Create Employee Modal Component -->
    <EmployeeCreateModal
      :show="showCreateModal"
      :new-employee="newEmployee"
      :available-areas="availableAreas"
      :loading="creating"
      @close="closeCreateModal"
      @create="handleCreateEmployee"
    />

    <!-- Delete Confirmation Modal Component -->
    <DeleteConfirmation
      :show="showDeleteModal"
      :employee="employeeToDelete"
      :loading="deleting"
      @close="closeDeleteModal"
      @confirm="handleDeleteEmployee"
    />
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useI18n } from 'vue-i18n'

// IMPORT: Components
import EmployeeFilters from '@/components/employee/EmployeeFilters.vue'
import EmployeeListTable from '@/components/employee/EmployeeListTable.vue'
import Pagination from '@/components/employee/Pagination.vue'
import EmployeeCreateModal from '@/components/employee/EmployeeCreateModal.vue'
import DeleteConfirmation from '@/components/employee/DeleteConfirmation.vue'

// IMPORT: Composables
import { useEmployeeManagement } from '@/composables/useEmployeeManagement'
import { useEmployeeCrud } from '@/composables/useEmployeeCRUD'

definePageMeta({
  layout: 'dss',
  middleware: 'auth'
})

const { t } = useI18n()

// USE: Employee Management Composable
const {
  employees,
  loading,
  areas,
  currentPage,
  pageSize,
  totalItems,
  totalPages,
  filters,
  availableAreas,
  loadEmployees,
  loadAllAreas,
  handleSearchUpdate,
  updateFilters,
  resetFilters,
  goToPage
} = useEmployeeManagement()

// USE: Employee CRUD Composable
const {
  showCreateModal,
  creating,
  showDeleteModal,
  employeeToDelete,
  deleting,
  newEmployee,
  viewEmployee,
  editEmployee,
  confirmDeleteEmployee,
  closeDeleteModal,
  deleteEmployee,
  closeCreateModal,
  createEmployee,
  initializeForm
} = useEmployeeCrud()

// HANDLERS: Success callbacks
const handleCreateEmployee = async (employeeData: any) => {
  await createEmployee(employeeData, () => {
    // Refresh data after create
    if (currentPage.value === 1) {
      loadEmployees()
    } else {
      currentPage.value = 1
      loadEmployees()
    }
    // Reload areas in case new area was added
    loadAllAreas()
  })
}

const handleDeleteEmployee = async () => {
  await deleteEmployee(() => {
    // Refresh current page
    loadEmployees()
    
    // If current page becomes empty and not page 1, go to previous page
    if (employees.value.length === 1 && currentPage.value > 1) {
      currentPage.value = currentPage.value - 1
      setTimeout(() => loadEmployees(), 100)
    }
  })
}

// LIFECYCLE
onMounted(() => {
  loadEmployees()
  loadAllAreas() // Load areas separately
  initializeForm() // Initialize form with current date
})
</script>