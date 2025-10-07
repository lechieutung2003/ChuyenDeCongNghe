<template>
  <div class="customer-create-container p-4 pt-20">
    <div class="mb-4">
      <h1 class="text-xl font-bold">Thêm khách hàng mới</h1>
    </div>

    <el-form
      ref="formRef"
      :model="form"
      :rules="rules"
      label-width="120px"
      class="max-w-2xl"
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

      <el-form-item>
        <el-button type="primary" @click="handleSubmit">Tạo mới</el-button>
        <el-button @click="router.back()">Hủy</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup>
import { ref, reactive } from "vue";
import { useRouter } from "vue-router";
import { ElMessage } from "element-plus";
import customerService from "@/services/dss/customerService";

definePageMeta({
  layout: "dss",
  middleware: ["auth"],
});

const router = useRouter();
const formRef = ref();

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

const handleSubmit = async () => {
  if (!formRef.value) return;

  try {
    await formRef.value.validate();

    await customerService.createCustomer(form);
    ElMessage.success("Tạo khách hàng thành công");
    router.push("/dss/customers");
  } catch (error) {
    console.error(error);
    ElMessage.error("Tạo khách hàng thất bại");
  }
};
</script>
