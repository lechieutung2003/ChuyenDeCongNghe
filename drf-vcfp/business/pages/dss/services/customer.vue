<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import serviceTypesApi from "@/services/dss/serviceTypes.js";
import '@/assets/css/customer.css'
const router = useRouter();
const services = ref([]);
const loading = ref(false);
const error = ref("");
definePageMeta({
  middleware: 'role-based'
})

const fetchServices = async () => {
  loading.value = true;
  error.value = "";
  try {
    const res = await serviceTypesApi.getAll();
    services.value = Array.isArray(res.results)
      ? res.results
      : Array.isArray(res)
      ? res
      : [];
  } catch (e) {
    error.value = "Không thể tải danh sách dịch vụ";
  } finally {
    loading.value = false;
  }
};

onMounted(fetchServices);
</script>

<template>
  <div class="about-page">
    <section class="stripe white">
      <div class="container">
        <div class="content-header">
          <h1 class="section-title">Danh sách dịch vụ hệ thống</h1>
          <p class="section-subtitle">Chọn dịch vụ để đặt đơn hàng</p>
        </div>
        <div v-if="error" style="color: #ef4444; text-align: center; padding: 15px; margin-bottom: 20px; background-color: #fef2f2; border-radius: 10px;">{{ error }}</div>
        <div class="services-grid-custom">
          <div v-for="service in services" :key="service.id" class="service-tile">
            <div class="service-bg">
              <img v-if="service.image_url" :src="service.image_url" alt="Hình dịch vụ" />
              <img v-else src="@/assets/images/deep.jpg" alt="Ảnh dịch vụ" />
            </div>
            <div class="service-overlay">
              <div class="service-tag">Hot</div>
              <div class="service-content">
                <h3>{{ service.name }}</h3>
                <p><strong>Giá/m²:</strong> {{ service.price_per_m2 }}</p>
                <p><strong>Tốc độ (m²/h):</strong> {{ service.cleaning_rate_m2_per_h }}</p>
                <p><strong>Mô tả:</strong> {{ service.description || 'Chưa có mô tả' }}</p>
                <div style="display: flex; gap: 10px; margin-top: 1rem; flex-wrap: wrap;">
                  <button class="featured-cta" @click="router.push('/dss/orders/create')" style="padding: 0.5rem 1rem; font-size: 0.9rem;">
                    Đặt dịch vụ này
                  </button>
                  <button class="btn" style="padding: 0.5rem 1rem; font-size: 0.9rem;">
                    Xem chi tiết
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div v-if="!loading && services.length === 0" style="text-align: center; color: var(--text-light); padding: 40px 20px;">
          Không có dữ liệu
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.services-grid-custom {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-bottom: 2rem;
}

.content-header {
  text-align: center;
  margin-bottom: 3rem;
}

@media (max-width: 768px) {
  .services-grid-custom {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
  
  .service-content h3 {
    font-size: 1.1rem;
  }
  
  .service-content p {
    font-size: 0.9rem;
  }
}
</style>
