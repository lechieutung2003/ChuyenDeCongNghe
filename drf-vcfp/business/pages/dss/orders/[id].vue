<template>
  <div class="order-detail-container p-4">
    <!-- Tiêu đề trang -->
    <div class="mb-6   flex justify-between items-center">
      <h1 class="text-2xl font-bold">Chi tiết đơn hàng #{{ $route.params.id }}</h1>
      <div>
        <el-button type="primary" @click="handlePrintOrder">
          <i class="el-icon-printer mr-1"></i> In đơn hàng
        </el-button>
        <el-button @click="navigateBack">
          <i class="el-icon-back mr-1"></i> Quay lại
        </el-button>
      </div>
    </div>

    <el-tabs v-model="activeTab">
      <el-tab-pane label="Thông tin đơn hàng" name="details">
        <OrderDetails 
          :order="order" 
          :loading="loading"
          @cancel-order="handleCancelOrder"
        />
      </el-tab-pane>

      <el-tab-pane 
        v-if="order && order.status !== 'completed' && order.status !== 'rejected'" 
        label="Phân công nhân viên" 
        name="assignment">
        <EmployeeAssignment 
          :order="order" 
          :loading="loading" 
        />
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import OrderService from '../../../services/dss/order';
import { ElMessage, ElMessageBox } from 'element-plus';
import { useRouter, useRoute } from 'vue-router';
import { formatCurrency} from '../../../utils/formatters';
import { formatDate, formatDateTime } from '../../../utils/time';
import OrderDetails from '../../../components/dss/orders/OrderDetails.vue';
import EmployeeAssignment from './EmployeeAssignment.vue';

const router = useRouter();
const route = useRoute();
const loading = ref(false);
const order = ref(null);
const activeTab = ref('details');

definePageMeta({
  layout: "dss",
});

// Fetch order details
const fetchOrderDetails = async () => {
  loading.value = true;
  try {
    const orderId = route.params.id;
    const data = await OrderService.getOrder(orderId);
    order.value = data;
  } catch (error) {
    console.error('Lỗi khi tải thông tin đơn hàng:', error);
    ElMessage.error('Không thể tải thông tin đơn hàng.');
  } finally {
    loading.value = false;
  }
};

// Handle cancel order
const handleCancelOrder = () => {
  OrderService.updateOrderStatus(order.value.id, 'cancelled')
    .then(() => {
      order.value.status = 'cancelled';
      ElMessage.success('Hủy đơn hàng thành công');
    })
    .catch((error) => {
      console.error('Lỗi khi hủy đơn hàng:', error);
      ElMessage.error('Hủy đơn hàng thất bại');
    });
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
        <p><strong>Trạng thái:</strong> ${getStatusLabel(order.value.status)}</p>
      </div>
      
      <div class="info-section">
        <h2>Thông tin khách hàng</h2>
        <p><strong>Tên:</strong> ${order.value.customer_name}</p>
        ${order.value.customer_details ? `
        <p><strong>Số điện thoại:</strong> ${order.value.customer_details.phone}</p>
        <p><strong>Email:</strong> ${order.value.customer_details.email}</p>
        <p><strong>Địa chỉ:</strong> ${order.value.customer_details.address}</p>
        ` : ''}
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
          <td>${order.value.service_details?.name || ''}</td>
          <td>${order.value.area_m2}</td>
          <td>${formatCurrency(order.value.service_details?.price_per_m2 || 0)}</td>
          <td>${formatCurrency(calculateTotalAmount(order.value))}</td>
        </tr>
      </table>
      
      <div class="total">
        <p>Tổng tiền: ${formatCurrency(calculateTotalAmount(order.value))}</p>
      </div>
      
      <div class="info-section">
        <h2>Thời gian dự kiến</h2>
        <p><strong>Bắt đầu:</strong> ${formatDateTime(order.value.preferred_start_time)}</p>
        <p><strong>Kết thúc:</strong> ${formatDateTime(order.value.preferred_end_time)}</p>
        <p><strong>Tổng thời gian yêu cầu:</strong> ${order.value.requested_hours} giờ</p>
        <p><strong>Ghi chú:</strong> ${order.value.note || 'Không có'}</p>
      </div>
    </body>
    </html>
  `;
  
  // Create a new window for printing
  const printWindow = window.open('', '_blank');
  printWindow.document.write(printContent);
  printWindow.document.close();
  printWindow.focus();
  
  // Print after resources loaded
  printWindow.onload = function() {
    printWindow.print();
    printWindow.onafterprint = function() {
      printWindow.close();
    };
  };
};

// Get status label
const getStatusLabel = (status) => {
  const statusMap = {
    'pending': 'Chờ xử lý',
    'confirmed': 'Đã xác nhận',
    'in_progress': 'Đang xử lý',
    'completed': 'Hoàn thành',
    'cancelled': 'Đã hủy'
  };
  return statusMap[status] || status;
};

// Calculate total amount
const calculateTotalAmount = (order) => {
  if (!order || !order.service_details || !order.area_m2) return 0;
  const area = parseFloat(order.area_m2);
  const pricePerM2 = order.service_details.price_per_m2 || 0;
  return area * pricePerM2;
};

// Navigate back to orders list
const navigateBack = () => {
  router.push('/dss/orders');
};

onMounted(() => {
  fetchOrderDetails();
  
  // Check if we should activate assignment tab
  if (route.query.tab === 'assignment') {
    activeTab.value = 'assignment';
  }
});
</script>

<style>
.order-detail-container .el-tabs__content {
  padding-top: 20px;
}
</style>