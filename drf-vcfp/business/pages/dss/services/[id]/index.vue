<script setup>
definePageMeta({
  layout: "dss",
});

import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import serviceTypesApi from "@/services/dss/serviceTypes.js";

const route = useRoute();
const router = useRouter();
const service = ref(null);
const loading = ref(false);

const fetchService = async () => {
  loading.value = true;
  try {
    service.value = await serviceTypesApi.getOne(route.params.id);
  } catch (e) {
    alert("Không thể tải dữ liệu");
  } finally {
    loading.value = false;
  }
};

onMounted(fetchService);
</script>

<template>
  <main class="flex-1 p-6 bg-white">
    <h2 class="text-xl font-bold mb-4">Chi tiết dịch vụ</h2>

    <div v-if="loading">Đang tải...</div>
    <div v-else-if="service">
      <p><strong>ID:</strong> {{ service.id }}</p>
      <p><strong>Tên dịch vụ:</strong> {{ service.name }}</p>
      <p><strong>Giá/m2:</strong> {{ service.price_per_m2 }}</p>
      <p>
        <strong>Tốc độ (m2/h):</strong> {{ service.cleaning_rate_m2_per_h }}
      </p>
    </div>
    <div v-else>Không tìm thấy dữ liệu</div>

    <div class="mt-4">
      <el-button @click="router.push('/dss/services')">Quay lại</el-button>
    </div>
  </main>
</template>
