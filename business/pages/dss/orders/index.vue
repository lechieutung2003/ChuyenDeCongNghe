<template>
  <div class="order-list-container p-6">
    <!-- Tiêu đề trang -->
    <div class="mb-6 flex justify-between items-center">
      <h1 class="text-2xl font-bold">Danh sách/Lịch sử đơn hàng</h1>
      <!-- <el-button type="primary" size="large" @click="handleCreateOrder">
        <i class="el-icon-plus mr-1"></i> Tạo đơn mới
      </el-button> -->
    </div>

    <!-- Bộ lọc -->
    <el-card class="mb-6 filter-card">
      <div class="grid grid-cols-3 gap-4">
        <el-form-item label="Khách hàng">
          <el-input
            v-model="filters.customer_name"
            placeholder="Tìm theo tên khách hàng..."
            @input="handleSearch"
          />
        </el-form-item>
        <el-form-item label="Trạng thái">
          <el-select
            v-model="filters.status"
            placeholder="Chọn trạng thái"
            clearable
            @change="handleSearch"
          >
            <el-option label="Chờ xử lý" value="pending" />
            <el-option label="Đã xác nhận" value="confirmed" />
            <el-option label="Đang xử lý" value="in_progress" />
            <el-option label="Hoàn thành" value="completed" />
            <el-option label="Hủy" value="rejected" />
          </el-select>
        </el-form-item>
        <el-form-item label="Ngày tạo">
          <el-date-picker
            v-model="filters.createdDate"
            type="date"
            placeholder="Chọn ngày tạo"
            @change="handleSearch"
          />
        </el-form-item>
        <el-form-item v-if="hasActiveFilters" :offset-top="10" class="col-span-3 flex justify-end">
          <el-button type="text" @click="resetFilters">Đặt lại bộ lọc</el-button>
        </el-form-item>
      </div>
    </el-card>

    <!-- Bảng dữ liệu -->
    <el-card class="order-table">
      <el-table :data="paginatedOrders" border stripe v-loading="loading">
        <el-table-column prop="id" label="Mã đơn hàng" width="150" />
        <el-table-column prop="customer_name" label="Khách hàng" />
        <el-table-column label="Ngày tạo" width="180">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="Diện tích" width="100">
          <template #default="{ row }"> {{ row.area_m2 }} m² </template>
        </el-table-column>
        <el-table-column label="Tổng tiền" width="150">
          <template #default="{ row }">
            {{ row.cost_confirm }}
          </template>
        </el-table-column>
        <el-table-column prop="status" label="Trạng thái" width="150">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">
              {{ getStatusLabel(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="Thao tác" width="280">
          <template #default="{ row }">
            <el-button
              type="primary"
              size="small"
              @click="viewOrderDetail(row.id)"
            >
              Chi tiết
            </el-button>
            <el-button
              type="warning"
              size="small"
              @click="navigateToOrderAssignment(row.id)"
              v-if="row.status !== 'completed' && row.status !== 'rejected'"
            >
              Phân công
            </el-button>
            <el-button
              type="danger"
              size="small"
              @click="handleCancelOrder(row)"
              v-if="row.status !== 'completed' && row.status !== 'rejected'"
            >
              Hủy
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
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from "vue";
import OrderService from "../../../services/dss/order";
import { ElMessage, ElMessageBox } from "element-plus";
import { useRouter } from "vue-router";
import {
  formatDate,
  formatDateTime,
} from "../../../utils/time";
import {formatCurrency} from "../../../utils/formatters";
const router = useRouter();
const loading = ref(false);
const orderList = ref([]);

definePageMeta({
  layout: "dss",
  middleware: ["auth", "role-based"],
});

// Bộ lọc
const filters = reactive({
  customer_name: "",
  status: "",
  createdDate: "",
});

// Phân trang
const pagination = reactive({
  currentPage: 1,
  pageSize: 3,
  total: 0,
});

// Hàm lấy danh sách đơn hàng
const fetchOrders = async () => {
  loading.value = true;
  try {
    const response = await OrderService.getOrders({
      // Không truyền page và pageSize
      // Hoặc truyền pageSize lớn để lấy tất cả
      pageSize: 1000 
    });

    orderList.value = response.results || [];
    pagination.total = orderList.value.length;
  } catch (error) {
    console.error("Lỗi khi tải danh sách đơn hàng:", error);
    ElMessage.error("Không thể tải danh sách đơn hàng.");
  } finally {
    loading.value = false;
  }
};

const filteredOrders = computed(() => {
  return orderList.value.filter(order => {
    // Lọc theo tên khách hàng
    const matchCustomer = !filters.customer_name || 
      order.customer_name?.toLowerCase().includes(filters.customer_name.toLowerCase());
    
    // Lọc theo trạng thái
    const matchStatus = !filters.status || order.status === filters.status;
    
    // Lọc theo ngày tạo
    const matchDate = !filters.createdDate || (
      order.created_at && 
      formatDate(order.created_at) === formatDate(filters.createdDate)
    );
    
    return matchCustomer && matchStatus && matchDate;
  });
});

// Xử lý tìm kiếm
const handleSearch = () => {
  pagination.currentPage = 1;
  // Không gọi fetchOrders() nữa vì lọc trên frontend
  pagination.total = filteredOrders.value.length; // Cập nhật tổng số bản ghi sau khi lọc
};

const paginatedOrders = computed(() => {
  const startIndex = (pagination.currentPage - 1) * pagination.pageSize;
  const endIndex = startIndex + pagination.pageSize;
  return filteredOrders.value.slice(startIndex, endIndex);
});

const hasActiveFilters = computed(() => {
  return filters.customer_name || filters.status || filters.createdDate;
});

// Đặt lại bộ lọc
const resetFilters = () => {
  filters.customer_name = "";
  filters.status = "";
  filters.createdDate = "";
  handleSearch();
};

// Xử lý thay đổi kích thước trang
const handleSizeChange = (size) => {
  pagination.pageSize = size;
  pagination.currentPage = 1;
  // Không gọi fetchOrders()
};

// Xử lý thay đổi trang hiện tại
const handleCurrentChange = (page) => {
  pagination.currentPage = page;
};

// Xem chi tiết đơn hàng
const viewOrderDetail = (orderId) => {
  router.push(`/dss/orders/${orderId}`);
};

// Chuyển đến trang phân công
const navigateToOrderAssignment = (orderId) => {
  router.push(`/dss/orders/${orderId}?tab=assignment`);
};

// Tính tổng số tiền dựa trên diện tích và giá
const calculateTotalAmount = (order) => {
  if (!order || !order.service_details || !order.area_m2) return 0;
  const area = parseFloat(order.area_m2);
  const pricePerM2 = order.service_details.price_per_m2 || 0;
  return area * pricePerM2;
};

// Lấy nhãn trạng thái
const getStatusLabel = (status) => {
  const statusMap = {
    'pending': 'Chờ xử lý',
    'confirmed': 'Đã xác nhận',
    'in_progress': 'Đang xử lý',
    'completed': 'Hoàn thành',
    'rejected': 'Đã hủy'
  };
  return statusMap[status] || status;
};

// Lấy loại màu cho trạng thái
const getStatusType = (status) => {
  const statusTypeMap = {
    pending: "warning",
    confirmed: "primary",
    in_progress: "info",
    completed: "success",
    cancelled: "danger",
  };
  return statusTypeMap[status] || "";
};

// Xử lý cập nhật trạng thái
// const handleUpdateStatus = (order) => {
//   ElMessageBox.prompt('Chọn trạng thái mới', 'Cập nhật trạng thái', {
//     confirmButtonText: 'Xác nhận',
//     cancelButtonText: 'Hủy',
//     inputType: 'select',
//     inputValue: order.status,
//     inputPlaceholder: 'Chọn trạng thái',
//     inputOptions: [
//       { value: 'pending', label: 'Chờ xử lý' },
//       { value: 'confirmed', label: 'Đã xác nhận' },
//       { value: 'in_progress', label: 'Đang xử lý' },
//       { value: 'completed', label: 'Hoàn thành' }
//     ]
//   }).then(({ value }) => {
//     OrderService.updateOrderStatus(order.id, value)
//       .then(() => {
//         const index = orderList.value.findIndex(item => item.id === order.id);
//         if (index !== -1) {
//           orderList.value[index].status = value;
//         }
//         ElMessage.success('Cập nhật trạng thái thành công');
//       })
//       .catch((error) => {
//         console.error('Lỗi khi cập nhật trạng thái:', error);
//         ElMessage.error('Cập nhật trạng thái thất bại');
//       });
//   }).catch(() => {
//     // Người dùng đã hủy cập nhật
//   });
// };

// Xử lý hủy đơn hàng
const handleCancelOrder = (order) => {
  ElMessageBox.prompt(
    "Vui lòng nhập lý do hủy đơn hàng",
    "Xác nhận hủy",
    {
      confirmButtonText: "Xác nhận",
      cancelButtonText: "Hủy",
      type: "warning",
      inputType: "textarea",
      inputPlaceholder: "Nhập lý do hủy đơn hàng..."
    }
  )
    .then(({ value: reason }) => {
      // Ghi log lý do hủy
      OrderService.rejectOrder(order.id, reason)
        .then(() => {
          // Cập nhật trạng thái đơn hàng thành "rejected"
          return OrderService.updateOrderStatus(order.id, "rejected");
        })
        .then(() => {
          // Cập nhật trạng thái trong danh sách
          const index = orderList.value.findIndex(
            (item) => item.id === order.id
          );
          if (index !== -1) {
            orderList.value[index].status = "rejected";
          }
          ElMessage.success("Hủy đơn hàng thành công");
        })
        .catch((error) => {
          console.error("Lỗi khi hủy đơn hàng:", error);
          ElMessage.error("Hủy đơn hàng thất bại");
        });
    })
    .catch(() => {
      // Người dùng đã hủy thao tác
    });
};

// Xử lý tạo đơn mới
const handleCreateOrder = () => {
  router.push("/dss/orders/create");
};

// Load dữ liệu khi component được mount
onMounted(() => {
  fetchOrders();
});
</script>

<style>
.filter-card .el-form-item {
  margin-bottom: 0;
}

.order-table {
  min-height: 400px;
}
</style>
