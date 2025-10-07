import ApiService from "@/services/api";

const baseUrl = "http://127.0.0.1:8008/api/v1/customer-orders";

export default {
  async getOrders(params) {
    try {
      const response = await ApiService.get(baseUrl, { params });
      console.log('API Response:', response); // Debug log
      return response;
    } catch (error) {
      console.error('Error fetching customer orders:', error);
      throw error;
    }
  },
  async getOrder(id) {
    try {
      const response = await ApiService.get(`${baseUrl}/${id}`);
      return response;
    } catch (error) {
      console.error('Error fetching customer order:', error);
      throw error;
    }
  },
};
