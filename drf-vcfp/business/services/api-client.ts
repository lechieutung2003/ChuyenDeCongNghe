import axios from 'axios';

// Tạo instance axios với config mặc định
export const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Thêm interceptor để xử lý token
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Thêm interceptor để xử lý response
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response) {
      // Xử lý lỗi 401 (Unauthorized)
      if (error.response.status === 401) {
        // Có thể thêm logic refresh token ở đây
        localStorage.removeItem('access_token');
        window.location.href = '/login';
      }
      // Xử lý lỗi 403 (Forbidden)
      if (error.response.status === 403) {
        console.error('Access forbidden');
      }
    }
    return Promise.reject(error);
  }
);