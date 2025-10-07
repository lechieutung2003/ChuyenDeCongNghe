<template>
  <div class="employee-order-detail-container p-4">
    <!-- Tiêu đề trang -->
    <div class="mb-6 flex justify-between items-center">
      <h1 class="text-2xl font-bold">
        Chi tiết đơn hàng #{{ $route.params.id }}
      </h1>
      <div class="flex gap-2">
        <el-button
          type="warning"
          :loading="updateLoading"
          @click="showStatusDialog = true"
          :disabled="!canEditStatus"
        >
          <i class="el-icon-edit mr-1"></i> Cập nhật trạng thái
        </el-button>
        <el-button type="primary" @click="handlePrintOrder">
          <i class="el-icon-printer mr-1"></i> In đơn hàng
        </el-button>
        <el-button @click="navigateBack">
          <i class="el-icon-back mr-1"></i> Quay lại
        </el-button>
      </div>
    </div>

    <!-- Thông tin đơn hàng -->
    <div v-if="loading" class="text-center">
      <el-loading></el-loading>
    </div>

    <div v-else-if="order" class="order-details">
      <!-- Thông tin cơ bản -->
      <el-card class="mb-4">
        <template #header>
          <h3>Thông tin đơn hàng</h3>
        </template>
        <el-row :gutter="20">
          <el-col :span="12">
            <div class="info-item"><strong>Mã đơn:</strong> {{ order.id }}</div>
            <div class="info-item">
              <strong>Ngày tạo:</strong> {{ formatDate(order.created_at) }}
            </div>
            <div class="info-item">
              <strong>Trạng thái:</strong>
              <el-tag :type="getStatusType(order.status)" effect="dark">
                {{ getStatusLabel(order.status) }}
              </el-tag>
            </div>
          </el-col>
          <el-col :span="12">
            <div class="info-item">
              <strong>Thời gian bắt đầu:</strong>
              {{ formatDateTime(order.preferred_start_time) }}
            </div>
            <div class="info-item">
              <strong>Thời gian kết thúc:</strong>
              {{ formatDateTime(order.preferred_end_time) }}
            </div>
            <div class="info-item">
              <strong>Tổng thời gian:</strong> {{ order.requested_hours }} giờ
            </div>
          </el-col>
        </el-row>
      </el-card>

      <!-- Thông tin khách hàng -->
      <el-card class="mb-4">
        <template #header>
          <h3>Thông tin khách hàng</h3>
        </template>
        <el-row :gutter="20">
          <el-col :span="12">
            <div class="info-item">
              <strong>Tên khách hàng:</strong> {{ order.customer_name }}
            </div>
            <div v-if="order.customer_details" class="info-item">
              <strong>Số điện thoại:</strong> {{ order.customer_details.phone }}
            </div>
            <div v-if="order.customer_details" class="info-item">
              <strong>Email:</strong> {{ order.customer_details.email }}
            </div>
          </el-col>
          <el-col :span="12">
            <div v-if="order.customer_details" class="info-item">
              <strong>Địa chỉ:</strong> {{ order.customer_details.address }}
            </div>
          </el-col>
        </el-row>
      </el-card>

      <!-- Thông tin dịch vụ -->
      <el-card class="mb-4">
        <template #header>
          <h3>Chi tiết dịch vụ</h3>
        </template>
        <el-row :gutter="20">
          <el-col :span="12">
            <div class="info-item">
              <strong>Loại dịch vụ:</strong>
              {{ order.service_details?.name || "N/A" }}
            </div>
            <div class="info-item">
              <strong>Diện tích:</strong> {{ order.area_m2 }} m²
            </div>
            <div class="info-item">
              <strong>Đơn giá:</strong>
              {{ formatCurrency(order.service_details?.price_per_m2 || 0) }}/m²
            </div>
          </el-col>
          <el-col :span="12">
            <div class="info-item">
              <strong>Tổng tiền:</strong>
              <span class="text-xl font-bold text-green-600">
                {{ order.cost_confirm }}
              </span>
            </div>
            <div class="info-item">
              <strong>Ghi chú:</strong> {{ order.note || "Không có" }}
            </div>
          </el-col>
        </el-row>
      </el-card>
    </div>

    <!-- Dialog cập nhật trạng thái -->
    <el-dialog
      v-model="showStatusDialog"
      title="Cập nhật trạng thái đơn hàng"
      width="400px"
    >
      <el-form>
        <el-form-item label="Trạng thái hiện tại:">
          <el-tag :type="getStatusType(order?.status)" effect="dark">
            {{ getStatusLabel(order?.status) }}
          </el-tag>
        </el-form-item>
        <el-form-item label="Trạng thái mới:">
          <el-select
            v-model="newStatus"
            placeholder="Chọn trạng thái mới"
            style="width: 100%"
          >
            <el-option
              v-for="status in availableStatuses"
              :key="status.value"
              :label="status.label"
              :value="status.value"
            />
          </el-select>
        </el-form-item>
      </el-form>

      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showStatusDialog = false">Hủy</el-button>
          <el-button
            type="primary"
            :loading="updateLoading"
            @click="handleUpdateStatus"
            :disabled="!newStatus"
          >
            Cập nhật
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import OrderService from "../../../services/dss/order";
import { ElMessage, ElMessageBox } from "element-plus";
import { useRouter, useRoute } from "vue-router";
import {
  formatDate,
  formatDateTime,
} from "../../../utils/time";
import {formatCurrency} from "../../../utils/formatters";

const router = useRouter();
const route = useRoute();
const loading = ref(false);
const updateLoading = ref(false);
const order = ref(null);
const showStatusDialog = ref(false);
const newStatus = ref("");

definePageMeta({
  layout: "dss",
});

// Available statuses for employee
const availableStatuses = [
  { value: "in_progress", label: "Đang thực hiện" },
  { value: "completed", label: "Hoàn thành" },
  { value: "on_hold", label: "Tạm dừng" },
];

// Check if employee can edit status
const canEditStatus = computed(() => {
  if (!order.value) return false;
  // Employee có thể edit những đơn hàng pending, confirmed, in_progress, on_hold (chưa completed hoặc cancelled)
  return ["pending", "confirmed", "in_progress", "on_hold"].includes(
    order.value.status
  );
});

// Fetch order details
const fetchOrderDetails = async () => {
  loading.value = true;
  try {
    const orderId = route.params.id;
    const data = await OrderService.getOrder(orderId);
    order.value = data;
  } catch (error) {
    console.error("Lỗi khi tải thông tin đơn hàng:", error);
    ElMessage.error("Không thể tải thông tin đơn hàng.");
  } finally {
    loading.value = false;
  }
};

// Handle update status
const handleUpdateStatus = async () => {
  if (!newStatus.value) return;

  updateLoading.value = true;
  try {
    await OrderService.updateOrderStatus(order.value.id, newStatus.value);
    order.value.status = newStatus.value;
    showStatusDialog.value = false;

    console.log("Order status updated to:", order.value.status);

    // Nếu trạng thái mới là completed, gọi API xử lý assignment và employee
    if (newStatus.value === "completed") {
      console.log("Completing order...");
      await OrderService.completeOrder(order.value.id, order.value.requested_hours);
    }

    ElMessage.success("Cập nhật trạng thái thành công!");
  } catch (error) {
    console.error("Lỗi khi cập nhật trạng thái:", error);
    ElMessage.error("Cập nhật trạng thái thất bại. Vui lòng thử lại.");
  } finally {
    updateLoading.value = false;
  }
};

// Print order
const handlePrintOrder = () => {
  if (!order.value) return;

  // Create print content
  const printContent = `
    <html>
    <head>
      <title>Đơn hàng ${order.value.id}</title>
      <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        h1 { text-align: center; }
        .info-section { margin-bottom: 20px; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
        .total { font-weight: bold; margin-top: 20px; text-align: right; }
      </style>
    </head>
    <body>
      <h1>CHI TIẾT ĐƠN HÀNG</h1>
      
      <div class="info-section">
        <h2>Thông tin đơn hàng</h2>
        <p><strong>Mã đơn:</strong> ${order.value.id}</p>
        <p><strong>Ngày tạo:</strong> ${formatDate(order.value.created_at)}</p>
        <p><strong>Trạng thái:</strong> ${getStatusLabel(
          order.value.status
        )}</p>
      </div>
      
      <div class="info-section">
        <h2>Thông tin khách hàng</h2>
        <p><strong>Tên:</strong> ${order.value.customer_name}</p>
        ${
          order.value.customer_details
            ? `
        <p><strong>Số điện thoại:</strong> ${order.value.customer_details.phone}</p>
        <p><strong>Email:</strong> ${order.value.customer_details.email}</p>
        <p><strong>Địa chỉ:</strong> ${order.value.customer_details.address}</p>
        `
            : ""
        }
      </div>
      
      <h2>Chi tiết dịch vụ</h2>
      <table>
        <tr>
          <th>Dịch vụ</th>
          <th>Diện tích (m²)</th>
          <th>Đơn giá</th>
          <th>Thành tiền</th>
        </tr>
        <tr>
          <td>${order.value.service_details?.name || ""}</td>
          <td>${order.value.area_m2}</td>
          <td>${formatCurrency(
            order.value.service_details?.price_per_m2 || 0
          )}</td>
          <td>${formatCurrency(calculateTotalAmount(order.value))}</td>
        </tr>
      </table>
      
      <div class="total">
        <p>Tổng tiền: ${order.value.cost_confirm}</p>
      </div>
      
      <div class="info-section">
        <h2>Thời gian dự kiến</h2>
        <p><strong>Bắt đầu:</strong> ${formatDateTime(
          order.value.preferred_start_time
        )}</p>
        <p><strong>Kết thúc:</strong> ${formatDateTime(
          order.value.preferred_end_time
        )}</p>
        <p><strong>Tổng thời gian yêu cầu:</strong> ${
          order.value.requested_hours
        } giờ</p>
        <p><strong>Ghi chú:</strong> ${order.value.note || "Không có"}</p>
      </div>
    </body>
    </html>
  `;

  // Create a new window for printing
  const printWindow = window.open("", "_blank");
  printWindow.document.write(printContent);
  printWindow.document.close();
  printWindow.focus();

  // Print after resources loaded
  printWindow.onload = function () {
    printWindow.print();
    printWindow.onafterprint = function () {
      printWindow.close();
    };
  };
};

// Get status label
const getStatusLabel = (status) => {
  const statusMap = {
    pending: "Chờ xử lý",
    confirmed: "Đã xác nhận",
    in_progress: "Đang thực hiện",
    completed: "Hoàn thành",
    cancelled: "Đã hủy",
    on_hold: "Tạm dừng",
  };
  return statusMap[status] || status;
};

// Get status type for tag color
const getStatusType = (status) => {
  const typeMap = {
    pending: "warning",
    confirmed: "info",
    in_progress: "primary",
    completed: "success",
    cancelled: "danger",
    on_hold: "warning",
  };
  return typeMap[status] || "info";
};

// Calculate total amount
const calculateTotalAmount = (order) => {
  if (!order || !order.service_details || !order.area_m2) return 0;
  const area = parseFloat(order.area_m2);
  const pricePerM2 = order.service_details.price_per_m2 || 0;
  return area * pricePerM2;
};

// Navigate back to employee orders list
const navigateBack = () => {
  router.push("/dss/employee-orders");
};

onMounted(() => {
  fetchOrderDetails();
});
</script>

<style scoped>
.employee-order-detail-container {
  max-width: 1200px;
  margin: 0 auto;
}

.info-item {
  margin-bottom: 12px;
  padding: 8px 0;
  border-bottom: 1px solid #f0f0f0;
}

.info-item:last-child {
  border-bottom: none;
}

.info-item strong {
  color: #606266;
  margin-right: 8px;
}
</style>
