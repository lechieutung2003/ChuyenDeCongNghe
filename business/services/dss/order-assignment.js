import ApiService from "@/services/api";

/**
 * Service class for managing employee assignments to orders
 */
class AssignmentService {
  constructor() {
    this.baseUrl = "http://127.0.0.1:8008/api/v1/assignments";
  }

  /**
   * Get assignments for a specific order
   * @param {string|number} orderId - Order ID
   * @returns {Promise} API response with assignments list
   */
  getAssignments(orderId) {
    return ApiService.get(`http://127.0.0.1:8008/api/v1/orders/${orderId}/assignments`);
  }

  /**
   * Create assignments for an order
   * @param {string|number} orderId - Order ID
   * @param {Array} assignments - Array of assignment objects
   * @returns {Promise} API response
   */
  createAssignments(orderId, assignments) {
    return ApiService.post(`http://127.0.0.1:8008/api/v1/orders/${orderId}/assignments`, assignments, {
      headers: { "Content-Type": "application/json" },
    });
  }

  /**
   * Update an existing assignment
   * @param {string|number} id - Assignment ID
   * @param {Object} data - Updated assignment data
   * @returns {Promise} API response
   */
  updateAssignment(id, data) {
    return ApiService.put(`${this.baseUrl}/${id}`, data, {
      headers: { "Content-Type": "application/json" },
    });
  }

  /**
   * Delete an assignment
   * @param {string|number} id - Assignment ID
   * @returns {Promise} API response
   */
  deleteAssignment(id) {
    console.log("Deleting assignment with ID:", id);
    return ApiService.delete(`${this.baseUrl}/${id}`);
  }

  /**
   * Get all assignments (for admin purposes)
   * @param {Object} params - Query parameters for filtering
   * @returns {Promise} API response with all assignments
   */
  getAllAssignments(params = {}) {
    return ApiService.get(this.baseUrl, { params });
  }

  /**
   * Get assignments for a specific employee
   * @param {string|number} employeeId - Employee ID
   * @returns {Promise} API response with employee's assignments
   */
  getEmployeeAssignments(employeeId) {
    return ApiService.get(`http://127.0.0.1:8008/api/v1/employees/${employeeId}/assignments`);
  }
}

// Export a singleton instance
export default new AssignmentService();