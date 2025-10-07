import { apiClient } from '@/services/api-client';
import { AxiosError } from 'axios';

export interface Customer {
  id: string;
  name: string;
  phone: string;
  email: string;
  address: string;
  area?: string;
}

class CustomerService {
  private baseUrl = '/customers';

  async getCustomerInfo(id: string): Promise<Customer> {
    try {
      const response = await apiClient.get<Customer>(`${this.baseUrl}/${id}/`);
      return response.data;
    } catch (error) {
      const axiosError = error as AxiosError;
      console.error('Error fetching customer info:', axiosError.response?.data || axiosError.message);
      throw error;
    }
  }

  async getCustomerProfile(): Promise<Customer> {
    try {
      const response = await apiClient.get<Customer>(`${this.baseUrl}/me/`);
      return response.data;
    } catch (error) {
      const axiosError = error as AxiosError;
      console.error('Error fetching customer profile:', axiosError.response?.data || axiosError.message);
      throw error;
    }
  }

  async updateCustomerProfile(data: Partial<Customer>): Promise<Customer> {
    try {
      const response = await apiClient.patch<Customer>(`${this.baseUrl}/me/`, data);
      return response.data;
    } catch (error) {
      const axiosError = error as AxiosError;
      console.error('Error updating customer profile:', axiosError.response?.data || axiosError.message);
      throw error;
    }
  }
}

export default new CustomerService();