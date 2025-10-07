<script setup>
definePageMeta({
  layout: "dss", // Sử dụng layout dss
});

import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import serviceTypesApi from "@/services/dss/serviceTypes.js";

const route = useRoute();
const router = useRouter();

const form = ref({
  name: "",
  price_per_m2: 0,
  cleaning_rate_m2_per_h: 0,
});

const loading = ref(false);

// Lấy dữ liệu dịch vụ từ API
const fetchService = async () => {
  loading.value = true;
  try {
    const res = await serviceTypesApi.getOne(route.params.id);
    const data = res.data ?? res; // tuỳ API có trả về res.data hay res trực tiếp
    form.value = {
      name: data.name,
      price_per_m2: data.price_per_m2,
      cleaning_rate_m2_per_h: data.cleaning_rate_m2_per_h,
    };
  } catch (e) {
    alert("Không thể tải dữ liệu");
    router.push("/dss/services"); // quay lại danh sách nếu lỗi
  } finally {
    loading.value = false;
  }
};

// Gửi dữ liệu cập nhật
const handleSubmit = async () => {
  loading.value = true;
  try {
    await serviceTypesApi.update(route.params.id, form.value);
    alert("Cập nhật thành công!");
    router.push("/dss/services");
  } catch (e) {
    alert("Cập nhật thất bại");
  } finally {
    loading.value = false;
  }
};

onMounted(fetchService);
</script>

<template>
  <main class="flex-1 p-6 bg-white">
    <h2 class="text-xl font-bold mb-4">Chỉnh sửa dịch vụ</h2>

    <el-form :model="form" label-width="150px" class="max-w-xl">
      <el-form-item label="Tên dịch vụ">
        <el-input v-model="form.name" placeholder="Nhập tên dịch vụ" />
      </el-form-item>

      <el-form-item label="Giá/m2">
        <el-input-number v-model="form.price_per_m2" :min="0" class="w-full" />
      </el-form-item>

      <el-form-item label="Tốc độ (m2/h)">
        <el-input-number
          v-model="form.cleaning_rate_m2_per_h"
          :min="0"
          class="w-full"
        />
      </el-form-item>

      <el-form-item>
        <el-button type="primary" :loading="loading" @click="handleSubmit">
          Lưu
        </el-button>
        <el-button @click="router.push('/dss/services')">Hủy</el-button>
      </el-form-item>
    </el-form>
  </main>
</template>
