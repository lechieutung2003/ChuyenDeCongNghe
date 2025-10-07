import { ref, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { debounce } from 'lodash-es'
import EmployeeService from '@/services/dss/users/employees'

export const useEmployeeManagement = () => {
  const { t } = useI18n()

  // STATE MANAGEMENT
  const employees = ref([])
  const loading = ref(false)
  const areas = ref([])
  
  // PAGINATION STATE
  const currentPage = ref(1)
  const pageSize = ref(3)
  const totalItems = ref(0)
  const totalPages = computed(() => Math.ceil(totalItems.value / pageSize.value))

  // FILTER STATE
  const filters = ref({
    search: '',
    area: '',
    status: ''
  })

  // COMPUTED
  const availableAreas = computed(() => {
    return areas.value.map(area => ({ value: area, label: area }))
  })

  // ✅ FIX: SEARCH LOGIC with better error handling
  const loadEmployees = async () => {
    loading.value = true
    try {
      const params = {
        page: currentPage.value,
        page_size: pageSize.value,
      }
      
      if (filters.value.search?.trim()) {
        params.search = filters.value.search.trim()
      }
      
      if (filters.value.area) params.area = filters.value.area
      
      if (filters.value.status !== '') {
        switch (filters.value.status) {
          case 'active':
            params.computed_status = 1
            break
          case 'inactive':
            params.computed_status = 2
            break
          case 'no_hours':
            params.computed_status = 0
            break
        }
      }
      
      const response = await EmployeeService.getEmployees(params)
      
      // ✅ FIX: Ensure response structure
      if (response && typeof response === 'object') {
        employees.value = response.results || []
        totalItems.value = response.count || 0
      } else {
        console.warn('Unexpected response structure:', response)
        employees.value = []
        totalItems.value = 0
      }
      
    } catch (error) {
      console.error('Error loading employees:', error)
      employees.value = []
      totalItems.value = 0
    } finally {
      loading.value = false
    }
  }

  // ✅ FIX: Load all areas with better error handling
  const loadAllAreas = async () => {
    try {
      const response = await EmployeeService.getEmployees({ 
        page: 1, 
        page_size: 1000
      })
      
      // ✅ FIX: Ensure response structure
      if (response && response.results && Array.isArray(response.results)) {
        const allEmployees = response.results
        const uniqueAreas = [...new Set(allEmployees.map(emp => emp.area).filter(Boolean))]
        areas.value = uniqueAreas.sort()
      } else {
        console.warn('Unexpected areas response structure:', response)
        areas.value = []
      }
      
    } catch (error) {
      console.error('Error loading areas:', error)
      areas.value = []
    }
  }

  // SEARCH HANDLER - Debounced
  const handleSearchUpdate = debounce((value: string) => {
    filters.value.search = value
    currentPage.value = 1
    loadEmployees()
  }, 300)

  // FILTER HANDLERS
  const updateFilters = (key: string, value: any) => {
    filters.value[key] = value
    currentPage.value = 1
    loadEmployees()
  }

  const resetFilters = () => {
    filters.value = {
      search: '',
      area: '',
      status: ''
    }
    currentPage.value = 1
    loadEmployees()
  }

  // PAGINATION HANDLER
  const goToPage = (page: number) => {
    currentPage.value = page
    loadEmployees()
  }

  return {
    // State
    employees,
    loading,
    areas,
    currentPage,
    pageSize,
    totalItems,
    totalPages,
    filters,
    availableAreas,
    
    // Methods
    loadEmployees,
    loadAllAreas,
    handleSearchUpdate,
    updateFilters,
    resetFilters,
    goToPage
  }
}