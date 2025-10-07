<template>
  <div class="order-list-container p-4 pt-16">
    <!-- Tiêu đề trang -->
    <div class="mb-4">
      <h1 class="text-xl font-bold">Danh sách/Lịch sử đơn hàng</h1>
    </div>

    <!-- Bộ lọc -->
    <el-card class="mb-4 filter-card">
      <div class="grid grid-cols-2 md:grid-cols-4 gap-2">
        <el-form-item label="Từ khóa">
          <el-input
            v-model="filters.keyword"
            placeholder="Tìm theo mã đơn, khách hàng..."
          />
        </el-form-item>
        <el-form-item label="Trạng thái">
          <el-select
            v-model="filters.status"
            placeholder="Chọn trạng thái"
            clearable
          >
            <el-option label="Chờ xử lý" value="pending" />
            <el-option label="Đã xác nhận" value="confirmed" />
            <el-option label="Đang xử lý" value="in_progress" />
            <el-option label="Hoàn thành" value="completed" />
            <el-option label="Hủy" value="cancelled" />
          </el-select>
        </el-form-item>
        <el-form-item label="Từ ngày">
          <el-date-picker
            v-model="filters.startDate"
            type="date"
            placeholder="Chọn ngày"
          />
        </el-form-item>
        <el-form-item label="Đến ngày">
          <el-date-picker
            v-model="filters.endDate"
            type="date"
            placeholder="Chọn ngày"
          />
        </el-form-item>
      </div>
      <div class="flex justify-end mt-4">
        <el-button type="primary" @click="handleSearch">Tìm kiếm</el-button>
        <el-button @click="resetFilters">Đặt lại</el-button>
      </div>
    </el-card>

    <!-- Bảng dữ liệu -->
    <el-card class="order-table">
      <el-table :data="paginatedOrders" border stripe v-loading="loading">
        <el-table-column label="Mã đơn hàng" width="140" show-overflow-tooltip>
          <template #default="{ row }">
            {{ row.order_details?.id || "N/A" }}
          </template>
        </el-table-column>
        <el-table-column
          label="Khách hàng"
          min-width="120"
          show-overflow-tooltip
        >
          <template #default="{ row }">
            {{ row.order_details?.customer_name || "N/A" }}
          </template>
        </el-table-column>
        <el-table-column label="Ngày tạo" width="100" show-overflow-tooltip>
          <template #default="{ row }">
            {{ formatDate(row.order_details?.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="Diện tích" width="80" show-overflow-tooltip>
          <template #default="{ row }">
            {{ row.order_details?.area_m2 || 0 }}
          </template>
        </el-table-column>
        <el-table-column label="Tổng tiền" width="120" show-overflow-tooltip>
          <template #default="{ row }">
            {{ row.order_details.cost_confirm }}
          </template>
        </el-table-column>
        <el-table-column label="Trạng thái" width="100">
          <template #default="{ row }">
            <el-tag
              :type="getStatusType(row.order_details?.status)"
              size="small"
            >
              {{ getStatusLabel(row.order_details?.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="Thao tác" width="80">
          <template #default="{ row }">
            <el-button
              type="primary"
              size="small"
              @click="viewOrderDetail(row.order_details?.id)"
            >
              Chi tiết
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- Phân trang -->
      <div class="flex justify-center mt-4">
        <el-pagination
          v-model:currentPage="pagination.currentPage"
          v-model:page-size="pagination.pageSize"
          :total="filteredOrders.length"
          :page-sizes="[10, 20, 50]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from "vue";
import employeeOrderService from "@/services/dss/employeeOrderService";
import { ElMessage } from "element-plus";
import { definePageMeta } from "#imports";

definePageMeta({
  layout: "dss",
  middleware: ["auth", "role-based"],
});

const loading = ref(false);
const orders = ref([]);

// Bộ lọc
const filters = reactive({
  keyword: "",
  status: "",
  startDate: "",
  endDate: "",
});

// Phân trang
const pagination = reactive({
  currentPage: 1,
  pageSize: 10,
});

// Lấy danh sách
const fetchOrders = async () => {
  loading.value = true;
  try {
    const response = await employeeOrderService.getOrders();
    orders.value = response || [];
  } catch (error) {
    console.error(error);
    orders.value = [];
    ElMessage.error("Lấy danh sách đơn hàng thất bại");
  } finally {
    loading.value = false;
  }
};

// Computed: lọc
const filteredOrders = computed(() => {
  return (orders.value || []).filter((o) => {
    const keywordMatch = filters.keyword
      ? o.order_details?.customer_name
          ?.toLowerCase()
          .includes(filters.keyword.toLowerCase())
      : true;
    const statusMatch = filters.status
      ? o.order_details?.status === filters.status
      : true;
    // Có thể thêm lọc ngày startDate/endDate ở đây
    return keywordMatch && statusMatch;
  });
});

// Computed: phân trang
const paginatedOrders = computed(() => {
  const start = (pagination.currentPage - 1) * pagination.pageSize;
  return filteredOrders.value.slice(start, start + pagination.pageSize);
});

// Các hàm trợ giúp
const formatDate = (d) => (d ? new Date(d).toLocaleDateString("vi-VN") : "");
const formatDateTime = (d) => (d ? new Date(d).toLocaleString("vi-VN") : "");
const formatCurrency = (v) =>
  new Intl.NumberFormat("vi-VN", { style: "currency", currency: "VND" }).format(
    v || 0
  );
const getStatusLabel = (status) => {
  const map = {
    pending: "Chờ xử lý",
    confirmed: "Đã xác nhận",
    in_progress: "Đang xử lý",
    completed: "Hoàn thành",
    cancelled: "Đã hủy",
  };
  return map[status] || status;
};
const getStatusType = (status) => {
  const map = {
    pending: "warning",
    confirmed: "primary",
    in_progress: "info",
    completed: "success",
    cancelled: "danger",
  };
  return map[status] || "info";
};
const calculateTotalAmount = (order) => {
  if (!order?.service_details || !order?.area_m2) return 0;
  return Number(order.area_m2) * Number(order.service_details.price_per_m2);
};

// Xem chi tiết
const viewOrderDetail = (orderId) => {
  // Navigate to detail page instead of showing dialog
  navigateTo(`/dss/employee-orders/${orderId}`);
};

// Xử lý bộ lọc
const handleSearch = () => {
  pagination.currentPage = 1;
};
const resetFilters = () => {
  filters.keyword = "";
  filters.status = "";
  filters.startDate = "";
  filters.endDate = "";
  handleSearch();
};
const handleSizeChange = (size) => {
  pagination.pageSize = size;
};
const handleCurrentChange = (page) => {
  pagination.currentPage = page;
};

onMounted(() => {
  fetchOrders();
});
</script>

<style scoped>
.filter-card .el-form-item {
  margin-bottom: 0;
}
.order-table {
  min-height: 150px;
  max-height: calc(100vh - 220px);
  overflow-y: auto;
}
.el-table {
  font-size: 0.875rem;
}
:deep(.el-card__body) {
  padding: 12px;
}
</style>
