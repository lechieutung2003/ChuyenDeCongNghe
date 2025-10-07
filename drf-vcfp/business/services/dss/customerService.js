import ApiService from '@/services/api';

const baseUrl = 'http://127.0.0.1:8008/api/v1/customers';

export default {
  async getCustomers(params) {
    try {
      const response = await ApiService.get(baseUrl, { params });
      return response;
    } catch (error) {
      console.error('Error fetching customers:', error);
      throw error;
    }
  },

  async getCustomer(id) {
    try {
      const response = await ApiService.get(`${baseUrl}/${id}`);
      return response;
    } catch (error) {
      console.error('Error fetching customer:', error);
      throw error;
    }
  },

  async createCustomer(data) {
    try {
      const response = await ApiService.post(baseUrl, data);
      return response;
    } catch (error) {
      console.error('Error creating customer:', error);
      throw error;
    }
  },

  async updateCustomer(id, data) {
    try {
      const response = await ApiService.put(`${baseUrl}/${id}`, data);
      return response;
    } catch (error) {
      console.error('Error updating customer:', error);
      throw error;
    }
  },

  async deleteCustomer(id) {
    try {
      const response = await ApiService.delete(`${baseUrl}/${id}`);
      return response;
    } catch (error) {
      console.error('Error deleting customer:', error);
      throw error;
    }
  },

  async getCustomerOrders(id) {
    try {
      const response = await ApiService.get(`${baseUrl}/${id}/orders`);
      return response;
    } catch (error) {
      console.error('Error fetching customer orders:', error);
      throw error;
    }
  }
};