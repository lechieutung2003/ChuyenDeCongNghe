<script setup>
definePageMeta({
  layout: "dss",
  middleware: ["auth", "role-based"],
});

import { ref, onMounted, computed } from "vue";
import { useOauthStore } from "@/stores/oauth";
import { useRouter } from "vue-router";
import serviceTypesApi from "@/services/dss/serviceTypes.js";

const router = useRouter();
const oauthStore = useOauthStore();
const isAdmin = computed(() =>
  oauthStore.hasAllScopes([
    "users:view",
    "users:edit",
    "roles:view",
    "roles:edit",
  ])
);
const services = ref([]);
const loading = ref(false);
const error = ref("");

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

const handleDelete = async (id) => {
  if (!confirm("Bạn có chắc chắn muốn xoá dịch vụ này?")) return;
  try {
    await serviceTypesApi.remove(id);
    services.value = services.value.filter((s) => s.id !== id);
  } catch (e) {
    alert("Xoá thất bại");
  }
};

onMounted(fetchServices);
</script>

<template>
  <main class="flex-1 p-6 bg-white">
    <h2 class="text-xl font-bold mb-4">Danh sách dịch vụ</h2>

    <!-- Nút tạo mới ngay trước bảng -->
    <div class="mb-4">
      <el-button type="primary" @click="router.push('/dss/services/create')">
        + Tạo mới
      </el-button>
    </div>

    <div v-if="error" class="text-red-600 mb-2">{{ error }}</div>

    <el-table :data="services" v-loading="loading" style="width: 100%">
      <!-- STT từ 1,2,3,... -->
      <el-table-column label="STT" width="60">
        <template #default="scope">
          {{ scope.$index + 1 }}
        </template>
      </el-table-column>

      <el-table-column prop="name" label="Tên dịch vụ" />
      <el-table-column prop="price_per_m2" label="Giá/m2" />
      <el-table-column prop="cleaning_rate_m2_per_h" label="Tốc độ (m2/h)" />

      <el-table-column label="Hành động" width="220">
        <template #default="scope">
          <el-button
            size="small"
            @click="router.push(`/dss/services/${scope.row.id}`)"
          >
            Xem
          </el-button>
          <template v-if="isAdmin">
            <el-button
              size="small"
              type="warning"
              @click="router.push(`/dss/services/${scope.row.id}/edit`)"
            >
              Sửa
            </el-button>
            <el-button
              size="small"
              type="danger"
              @click="handleDelete(scope.row.id)"
            >
              Xoá
            </el-button>
          </template>
        </template>
      </el-table-column>
    </el-table>

    <div
      v-if="!loading && services.length === 0"
      class="text-center text-gray-500 py-8"
    >
      Không có dữ liệu
    </div>
  </main>
</template>
