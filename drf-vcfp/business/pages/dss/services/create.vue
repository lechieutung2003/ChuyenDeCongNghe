<script setup>
definePageMeta({
  layout: "dss",
});

import { ref } from "vue";
import { useRouter } from "vue-router";
import serviceTypesApi from "@/services/dss/serviceTypes.js";

const router = useRouter();
const form = ref({
  name: "",
  price_per_m2: "",
  cleaning_rate_m2_per_h: "",
});
const loading = ref(false);

const handleSubmit = async () => {
  loading.value = true;
  try {
    await serviceTypesApi.create(form.value);
    router.push("/dss/services");
  } catch (e) {
    alert("Tạo mới thất bại");
  } finally {
    loading.value = false;
  }
};
</script>

<template>
  <main class="flex-1 p-6 bg-white">
    <h2 class="text-xl font-bold mb-4">Tạo dịch vụ mới</h2>

    <el-form :model="form" label-width="150px">
      <el-form-item label="Tên dịch vụ">
        <el-input v-model="form.name" />
      </el-form-item>
      <el-form-item label="Giá/m2">
        <el-input v-model="form.price_per_m2" type="number" />
      </el-form-item>
      <el-form-item label="Tốc độ (m2/h)">
        <el-input v-model="form.cleaning_rate_m2_per_h" type="number" />
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
