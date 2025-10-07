import ApiService from "@/services/api";

/**
 * Service class for managing employees and recommendations
 */
class EmployeeService {
  constructor() {
    this.baseUrl = "http://127.0.0.1:8008/api/v1/employees";
  }

  /**
   * Get all employees
   * @param {Object} params - Query parameters for filtering
   * @returns {Promise} API response with employees list
   */
  getEmployees(params = {}) {
    return ApiService.get(this.baseUrl, { params });
  }

  /**
   * Get a specific employee by ID
   * @param {string|number} id - Employee ID
   * @returns {Promise} API response with employee details
   */
  getEmployee(id) {
    return ApiService.get(`${this.baseUrl}/${id}`);
  }

  /**
   * Get recommended employees for a specific order
   * @param {string|number} orderId - Order ID
   * @returns {Promise} API response with employee recommendations
   */
  getRecommendations(orderId) {
    return ApiService.get(`http://127.0.0.1:8008/api/v1/orders/${orderId}/recommendations`);
  }

  /**
   * Get employee availability
   * @param {string|number} employeeId - Employee ID
   * @param {Object} params - Date range parameters
   * @returns {Promise} API response with employee availability
   */
  getAvailability(employeeId, params = {}) {
    return ApiService.get(`${this.baseUrl}/${employeeId}/availability`, { params });
  }

  /**
   * Create a new employee
   * @param {Object} data - Employee data
   * @returns {Promise} API response
   */
  createEmployee(data) {
    return ApiService.post(this.baseUrl, data, {
      headers: { "Content-Type": "application/json" },
    });
  }

  /**
   * Update an existing employee
   * @param {string|number} id - Employee ID
   * @param {Object} data - Updated employee data
   * @returns {Promise} API response
   */
  updateEmployee(id, data) {
    return ApiService.put(`${this.baseUrl}/${id}`, data, {
      headers: { "Content-Type": "application/json" },
    });
  }

  /**
   * Delete an employee
   * @param {string|number} id - Employee ID
   * @returns {Promise} API response
   */
  deleteEmployee(id) {
    return ApiService.delete(`${this.baseUrl}/${id}`);
  }

  /**
   * Get employee skills
   * @param {string|number} id - Employee ID
   * @returns {Promise} API response with skills
   */
  getSkills(id) {
    return ApiService.get(`${this.baseUrl}/${id}/skills`);
  }

  /**
   * Update employee skills
   * @param {string|number} id - Employee ID
   * @param {Array} skills - Array of skill objects
   * @returns {Promise} API response
   */
  updateSkills(id, skills) {
    return ApiService.put(`${this.baseUrl}/${id}/skills`, { skills }, {
      headers: { "Content-Type": "application/json" },
    });
  }

  /**
   * Get employee work schedule
   * @param {string|number} id - Employee ID
   * @param {Object} params - Date range parameters
   * @returns {Promise} API response with work schedule
   */
  getSchedule(id, params = {}) {
    return ApiService.get(`${this.baseUrl}/${id}/schedule`, { params });
  }
}

// Export a singleton instance
export default new EmployeeService();