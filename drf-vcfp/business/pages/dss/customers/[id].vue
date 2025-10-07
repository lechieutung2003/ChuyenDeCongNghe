<template>
  <div class="customer-detail-container p-4 pt-20">
    <div class="mb-4 flex justify-between items-center">
      <h1 class="text-xl font-bold">Chi tiết khách hàng</h1>
      <el-button type="primary" @click="enableEdit">
        <el-icon class="mr-1"><Edit /></el-icon>Chỉnh sửa
      </el-button>
    </div>

    <el-form
      ref="formRef"
      :model="form"
      :rules="rules"
      label-width="120px"
      class="max-w-2xl"
      :disabled="!isEditing"
    >
      <el-form-item label="Tên khách hàng" prop="name">
        <el-input v-model="form.name" />
      </el-form-item>

      <el-form-item label="Email" prop="email">
        <el-input v-model="form.email" type="email" />
      </el-form-item>

      <el-form-item label="Số điện thoại" prop="phone">
        <el-input v-model="form.phone" />
      </el-form-item>

      <el-form-item label="Địa chỉ" prop="address">
        <el-input v-model="form.address" type="textarea" />
      </el-form-item>

      <el-form-item label="Khu vực" prop="area">
        <el-select v-model="form.area">
          <el-option label="Nội thành" value="urban" />
          <el-option label="Ngoại thành" value="suburban" />
        </el-select>
      </el-form-item>

      <el-form-item v-if="isEditing">
        <el-button type="primary" @click="handleSubmit">Lưu</el-button>
        <el-button @click="cancelEdit">Hủy</el-button>
      </el-form-item>
    </el-form>

    <!-- Lịch sử đơn hàng -->
    <div class="mt-8">
      <h2 class="text-lg font-bold mb-4">Lịch sử đơn hàng</h2>
      <el-table
        v-loading="loadingOrders"
        :data="customerOrders"
        stripe
        class="w-full"
        size="small"
      >
        <el-table-column label="Mã đơn" prop="id" width="220" />
        <el-table-column label="Dịch vụ" min-width="150">
          <template #default="{ row }">
            {{ row.service_details?.name }}
          </template>
        </el-table-column>
        <el-table-column label="Thời gian" min-width="200">
          <template #default="{ row }">
            {{ formatDateTime(row.preferred_start_time) }}
          </template>
        </el-table-column>
        <el-table-column label="Trạng thái" width="120">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">
              {{ getStatusLabel(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="Thao tác" width="100" fixed="right">
          <template #default="{ row }">
            <el-button
              size="small"
              @click="router.push(`/dss/orders/${row.id}`)"
            >
              Chi tiết
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { ElMessage } from "element-plus";
import { Edit } from "@element-plus/icons-vue";
import customerService from "@/services/dss/customerService";

definePageMeta({
  layout: "dss",
  middleware: ["auth"],
});

const route = useRoute();
const router = useRouter();
const formRef = ref();
const isEditing = ref(false);
const loadingOrders = ref(false);
const customerOrders = ref([]);

const form = reactive({
  name: "",
  email: "",
  phone: "",
  address: "",
  area: "urban",
});

const rules = {
  name: [
    {
      required: true,
      message: "Vui lòng nhập tên khách hàng",
      trigger: "blur",
    },
  ],
  email: [
    { required: true, message: "Vui lòng nhập email", trigger: "blur" },
    { type: "email", message: "Email không hợp lệ", trigger: "blur" },
  ],
  phone: [
    { required: true, message: "Vui lòng nhập số điện thoại", trigger: "blur" },
  ],
  address: [
    { required: true, message: "Vui lòng nhập địa chỉ", trigger: "blur" },
  ],
  area: [
    { required: true, message: "Vui lòng chọn khu vực", trigger: "change" },
  ],
};

const fetchCustomer = async () => {
  try {
    const customer = await customerService.getCustomer(route.params.id);
    Object.assign(form, customer);
  } catch (error) {
    console.error(error);
    ElMessage.error("Lấy thông tin khách hàng thất bại");
    router.push("/dss/customers");
  }
};

const fetchCustomerOrders = async () => {
  loadingOrders.value = true;
  try {
    customerOrders.value = await customerService.getCustomerOrders(
      route.params.id
    );
  } catch (error) {
    console.error(error);
    ElMessage.error("Lấy lịch sử đơn hàng thất bại");
  } finally {
    loadingOrders.value = false;
  }
};

const enableEdit = () => {
  isEditing.value = true;
};

const cancelEdit = () => {
  isEditing.value = false;
  fetchCustomer();
};

const handleSubmit = async () => {
  if (!formRef.value) return;

  try {
    await formRef.value.validate();

    await customerService.updateCustomer(route.params.id, form);
    ElMessage.success("Cập nhật thông tin thành công");
    isEditing.value = false;
  } catch (error) {
    console.error(error);
    ElMessage.error("Cập nhật thông tin thất bại");
  }
};

const formatDateTime = (datetime) => {
  return new Date(datetime).toLocaleString("vi-VN");
};

const getStatusLabel = (status) => {
  const map = {
    pending: "Chờ xử lý",
    confirmed: "Đã xác nhận",
    completed: "Hoàn thành",
    cancelled: "Đã hủy",
  };
  return map[status] || status;
};

const getStatusType = (status) => {
  const map = {
    pending: "warning",
    confirmed: "primary",
    completed: "success",
    cancelled: "danger",
  };
  return map[status] || "info";
};

onMounted(() => {
  fetchCustomer();
  fetchCustomerOrders();
});
</script>
