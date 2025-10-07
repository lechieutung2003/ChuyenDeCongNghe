import ApiService from "@/services/api";

/**
 * Service class for managing service types
 */
class ServiceTypeService {
  constructor() {
    this.baseUrl = "http://127.0.0.1:8008/api/v1/service-types";
  }

  /**
   * Create a new service type
   * @param {Object} data - Service type data
   * @returns {Promise} API response
   */
  create(data) {
    return ApiService.post(this.baseUrl, data, {
      headers: { "Content-Type": "application/json" },
    });
  }

  /**
   * Get all service types
   * @returns {Promise} API response with service types list
   */
  getServiceTypes() {
    return ApiService.get(this.baseUrl);
  }

  /**
   * Get a specific service type by ID
   * @param {string|number} id - Service type ID
   * @returns {Promise} API response with service type details
   */
  getServiceType(id) {
    return ApiService.get(`${this.baseUrl}/${id}`);
  }

  /**
   * Update an existing service type
   * @param {string|number} id - Service type ID
   * @param {Object} data - Updated service type data
   * @returns {Promise} API response
   */
  update(id, data) {
    return ApiService.put(`${this.baseUrl}/${id}`, data, {
      headers: { "Content-Type": "application/json" },
    });
  }

  /**
   * Delete a service type
   * @param {string|number} id - Service type ID
   * @returns {Promise} API response
   */
  delete(id) {
    return ApiService.delete(`${this.baseUrl}/${id}`);
  }
}

// Export a singleton instance
export default new ServiceTypeService();