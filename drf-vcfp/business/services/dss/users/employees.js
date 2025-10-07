import BaseService from '../../base'

class EmployeeService extends BaseService {
  get entity() {
    return 'employees';
  }

  // Thêm method cleanEmployeeData để tái sử dụng trong các hàm update
  cleanEmployeeData(data) {
    const cleanData = { ...data }

    // Remove computed/readonly fields
    delete cleanData.computed_status
    delete cleanData.status_text
    delete cleanData.id // Don't send ID in body
    delete cleanData.created_at
    delete cleanData.updated_at
    delete cleanData.completed_orders_count
    delete cleanData.total_hours_worked

    // Remove null fields that cause validation errors
    if (cleanData.user === null || cleanData.user === undefined) {
      delete cleanData.user
    }

    if (cleanData.office_id === null || cleanData.office_id === undefined) {
      delete cleanData.office_id
    }

    console.log('Cleaned employee data:', cleanData)
    return cleanData
  }

  async getSkills() {
    try {
      const response = await this.request().get('skills') // Endpoint API để lấy danh sách kỹ năng
      console.log('Skills fetched successfully:', response)
      return response.data || response
    } catch (error) {
      console.error('Error fetching skills:', error)
      throw error
    }
  }

  async getEmployees(params = {}) {
    // Lọc bỏ empty parameters và search
    const cleanParams = {}

    Object.entries(params).forEach(([key, value]) => {
      // Bỏ qua search parameter và empty values
      if (key === 'search') {
        if (value && value.trim() !== '') {
          cleanParams[key] = value.trim()
        }
        return
      }

      if (key === 'computed_status') {
        // Only exclude null/undefined, allow 0, 1, 2
        if (value !== null && value !== undefined && value !== '') {
          cleanParams[key] = value
        }
        return
      }

      if (value !== null && value !== undefined && value !== '' && value !== 0) {
        cleanParams[key] = value
      }
    })

    // Nếu không có params nào thì gọi không có params
    if (Object.keys(cleanParams).length === 0) {
      return this.gets()
    }

    return this.gets(cleanParams)
  }

  async searchEmployees(searchTerm, params = {}) {
    // Tạo method riêng cho search 
    const searchParams = {
      ...params,
      first_name__icontains: searchTerm, // field search phù hợp
    }
    return this.gets(searchParams)
  }

  async getEmployee(id) {
    try {
      const response = await this.get(id)
      console.log('Employee fetched successfully:', response)
      return response
    } catch (error) {
      console.error('Error fetching employee:', error)
      throw error
    }
  }

  async createEmployee(data) {
    console.log('Creating employee:', data)
    try {
      const response = await this.create(data)
      console.log('Employee created successfully:', response)
      return response
    } catch (error) {
      console.error('Error creating employee:', error)
      throw error
    }
  }

  // Add updateEmployee method
  async updateEmployee(id, data) {

    try {
      const cleanData = this.cleanEmployeeData(data)

      // ✅ Debug HTTP client
      const httpClient = this.request()

      if (typeof httpClient.patch !== 'function') {
        throw new Error('HTTP client does not have patch method')
      }

      // ✅ Sử dụng admin-update endpoint
      const response = await httpClient.patch(`${this.entity}/${id}/admin-update`, cleanData)

      return response.data || response

    } catch (error) {
      console.error('Error updating employee:', error)
      console.error('Error response:', error.response?.data)
      console.error('Error status:', error.response?.status)

      if (error.response?.data) {
        console.error('Backend validation errors:', error.response.data)
      }

      throw error
    }
  }

  async deleteEmployee(id) {
    console.log('Deleting employee with ID:', id)
    try {
      const response = await this.delete(id)
      console.log('Employee deleted successfully:', response)
      return response
    } catch (error) {
      console.error('Error deleting employee:', error)
      throw error
    }
  }

  async updateEmployeeStatus(id, status) {
    console.log('Updating employee status:', { id, status })
    try {
      const response = await this.request().patch(`${this.entity}/${id}/`, { status })
      console.log('Employee status updated successfully:', response)
      return response.data || response
    } catch (error) {
      console.error('Error updating employee status:', error)
      throw error
    }
  }

  async getMyProfile() {
    console.log('Getting my profile')
    try {
      const response = await this.request().get(`${this.entity}/my-profile`)
      // console.log('Profile fetched successfully:', response)
      return response.data || response
    } catch (error) {
      console.error('Error fetching profile:', error)
      throw error
    }
  }

  async updateMyProfile(data) {
    console.log('Updating my profile:', data)

    try {
      const cleanData = this.cleanEmployeeData(data)
      console.log('Clean profile data:', cleanData)

      // Sử dụng PATCH method như backend expect
      const response = await this.request().patch(`${this.entity}/update-my-profile`, cleanData)
      console.log("response:", response)

      console.log('Profile updated successfully:', response)
      return response.data || response

    } catch (error) {
      console.error('Error updating profile:', error)
      console.error('Profile error response:', error.response?.data)

      // ✅ Thêm better error handling
      if (error.response?.status === 404) {
        throw new Error('Employee profile not found')
      } else if (error.response?.status === 403) {
        throw new Error('You do not have permission to update this profile')
      } else if (error.response?.data) {
        // Backend trả về validation errors
        throw error
      }

      throw error
    }
  }

}

export default new EmployeeService()