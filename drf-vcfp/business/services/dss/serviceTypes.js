import ApiService from "@/services/api";

const baseUrl = "http://127.0.0.1:8008/api/v1/service-types";

export default {
  create(data) {
    return ApiService.post(baseUrl, data, {
      headers: { "Content-Type": "application/json" },
    });
  },
  getAll() {
    return ApiService.get(baseUrl);
  },
  getOne(id) {
  return ApiService.get(`${baseUrl}/${id}`);
},
  update(id, data) {
    return ApiService.put(`${baseUrl}/${id}`, data, {
      headers: { "Content-Type": "application/json" },
    });
  },
  remove(id) {
  return ApiService.delete(`${baseUrl}/${id}`);
}
};