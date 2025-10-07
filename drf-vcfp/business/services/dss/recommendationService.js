import ApiService from '@/services/api';

class RecommendationService {
  constructor() {
    this.baseUrl = 'http://127.0.0.1:8008/api/v1';
  }

  getRecommendations(orderId) {
    // Sửa đường dẫn để khớp với endpoint backend đã hoạt động
    return ApiService.get(`${this.baseUrl}/recommendations/${orderId}/recommendations`);
  }
}

export default new RecommendationService();