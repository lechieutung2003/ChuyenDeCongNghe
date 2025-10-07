import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import EmployeeService from '@/services/dss/users/employees'

export const useEmployeeCrud = () => {
    const { t } = useI18n()
    const router = useRouter()

    // MODAL STATE
    const showCreateModal = ref(false)
    const creating = ref(false)
    const showDeleteModal = ref(false)
    const employeeToDelete = ref(null)
    const deleting = ref(false)

    // FORM STATE
    const newEmployee = ref({
        first_name: '',
        last_name: '',
        work_mail: '',
        personal_mail: '',
        phone: '',
        gender: '',
        date_of_birth: '',
        join_date: '',
        area: '',
        skills: [],
        salary: '',
        working_start_time: '',
        working_end_time: '',
        status: 1
    })

    // NAVIGATION HANDLERS
    const viewEmployee = (employee: any) => {
        router.push(`/dss/users/${employee.id}`)
    }

    const editEmployee = (employee: any) => {
        router.push(`/dss/users/${employee.id}?edit=true`)
    }

    // DELETE HANDLERS
    const confirmDeleteEmployee = (employee: any) => {
        employeeToDelete.value = employee
        showDeleteModal.value = true
    }

    const closeDeleteModal = () => {
        showDeleteModal.value = false
        employeeToDelete.value = null
        deleting.value = false
    }

    const deleteEmployee = async (onSuccess?: () => void) => {
        if (!employeeToDelete.value) return

        deleting.value = true
        try {
            await EmployeeService.deleteEmployee(employeeToDelete.value.id)

            alert(`Đã xóa nhân viên ${employeeToDelete.value.first_name} ${employeeToDelete.value.last_name} thành công!`)

            // Call success callback
            if (onSuccess) onSuccess()

        } catch (error) {
            console.error('Error deleting employee:', error)
            alert(`Có lỗi xảy ra khi xóa nhân viên: ${error.message || 'Vui lòng thử lại'}`)
        } finally {
            deleting.value = false
            closeDeleteModal()
        }
    }

    // CREATE HANDLERS
    const resetNewEmployee = () => {
        newEmployee.value = {
            first_name: '',
            last_name: '',
            work_mail: '',
            personal_mail: '',
            phone: '',
            gender: '',
            date_of_birth: '',
            join_date: new Date().toISOString().split('T')[0],
            area: '',
            salary: '',
            working_start_time: '',
            working_end_time: '',
            status: 1
        }
    }

    const closeCreateModal = () => {
        showCreateModal.value = false
        resetNewEmployee()
        creating.value = false
    }

    const createEmployee = async (employeeData: any, onSuccess?: () => void) => {
        creating.value = true
        try {
            if (!employeeData.first_name || !employeeData.last_name ||
                !employeeData.work_mail || !employeeData.phone) {
                alert(t('please_fill_required_fields'))
                return
            }

            const dataToSend = {
                first_name: employeeData.first_name?.trim(),
                last_name: employeeData.last_name?.trim(),
                work_mail: employeeData.work_mail?.trim(),
                phone: employeeData.phone?.trim(),
                ...(employeeData.personal_mail && { personal_mail: employeeData.personal_mail.trim() }),
                ...(employeeData.gender && { gender: employeeData.gender }),
                ...(employeeData.date_of_birth && { date_of_birth: employeeData.date_of_birth }),
                ...(employeeData.join_date && { join_date: employeeData.join_date }),
                ...(employeeData.area && { area: employeeData.area.trim() }),
                ...(employeeData.salary && { salary: parseFloat(employeeData.salary) }),
                ...(employeeData.working_start_time && { working_start_time: employeeData.working_start_time }),
                ...(employeeData.working_end_time && { working_end_time: employeeData.working_end_time }),
                ...(employeeData.skills && employeeData.skills.length > 0 && { skills: employeeData.skills }),
                status: 1
            }

            const response = await EmployeeService.createEmployee(dataToSend)

            alert(`Đã tạo nhân viên ${dataToSend.first_name} ${dataToSend.last_name} thành công!`)
            closeCreateModal()

            // Call success callback
            if (onSuccess) onSuccess()

        } catch (error) {
            console.error('Error creating employee:', error)
            let errorMessage = 'Có lỗi xảy ra khi tạo nhân viên'

            if (error.response?.status === 400) {
                errorMessage = 'Dữ liệu nhập vào không hợp lệ'
            } else if (error.response?.status === 409) {
                errorMessage = 'Email hoặc số điện thoại đã được sử dụng'
            } else if (error.message) {
                errorMessage = error.message
            }

            alert(errorMessage)
        } finally {
            creating.value = false
        }
    }

    // INITIALIZE
    const initializeForm = () => {
        resetNewEmployee()
    }

    return {
        // Modal State
        showCreateModal,
        creating,
        showDeleteModal,
        employeeToDelete,
        deleting,

        // Form State
        newEmployee,

        // Navigation
        viewEmployee,
        editEmployee,

        // Delete
        confirmDeleteEmployee,
        closeDeleteModal,
        deleteEmployee,

        // Create
        closeCreateModal,
        createEmployee,
        resetNewEmployee,
        initializeForm
    }
}