import ApiService from "@/services/api";

const baseUrl = "http://127.0.0.1:8008/api/v1/customer";
const customerApi = {
	// Lấy thông tin chi tiết customer
	async getUser() {
		return ApiService.get(baseUrl + "/info");
	},

	// Lấy danh sách đơn hàng của customer
	async getOrders(params) {
		return ApiService.get(baseUrl + "/orders", { params });
	},

	// Lấy chi tiết một đơn hàng
	async getOrder(id) {
		return ApiService.get(`${baseUrl}/orders/${id}`);
	},

	// Tạo đơn hàng mới cho customer
	async createOrder(orderData) {
		return ApiService.post(`${baseUrl}/create-order`, orderData);
	},

	// Cập nhật đơn hàng (chỉ cho trạng thái pending)
	async updateOrder(orderId, orderData) {
		return ApiService.put(`${baseUrl}/orders/${orderId}`, orderData);
	},

	// Cập nhật feedback cho đơn hàng đã hoàn thành
	async updateOrderFeedback(orderId, feedback) {
		return ApiService.put(`${baseUrl}/orders/${orderId}/feedback`, {
			customer_feedback: feedback
		});
	},

};

export default customerApi;
