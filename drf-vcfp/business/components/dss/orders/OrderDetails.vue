<template>
  <el-card v-loading="loading" class="order-details-card">
    <div v-if="order">
      <!-- Header với trạng thái đơn hàng nổi bật -->
      <div class="flex justify-between items-center mb-5 pb-3 border-b">
        <div>
          <h2 class="text-xl font-semibold mb-1">Đơn hàng #{{ order.id }}</h2>
          <p class="text-sm text-gray-500">Tạo ngày {{ formatDate(order.created_at) }}</p>
        </div>
        <el-tag :type="getStatusType(order.status)" size="large" effect="dark">
          {{ getStatusLabel(order.status) }}
        </el-tag>
      </div>
      
      <!-- Thông tin tổng quan - Grid layout -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-5">
        <!-- Thông tin đơn hàng -->
        <div class="bg-gray-50 rounded-lg p-4 border border-gray-100">
          <h3 class="text-lg font-medium mb-3 flex items-center">
            <i class="el-icon-document mr-2"></i>Thông tin đơn hàng
          </h3>
          <div class="space-y-2">
            <!-- <div class="flex justify-between">
              <span class="text-gray-600">Diện tích:</span>
              <strong>{{ order.area_m2 }} m²</strong>
            </div> -->
            <div class="flex justify-between">
              <span class="text-gray-600">Thời gian ước tính</span>
              <strong>{{ order.estimated_hours }} giờ</strong>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-600">Thời gian yêu cầu</span>
              <strong>{{ order.requested_hours }} giờ</strong>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-600">Thời gian bắt đầu:</span>
              <strong>{{ formatDateTime(order.preferred_start_time) }}</strong>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-600">Thời gian kết thúc:</span>
              <strong>{{ formatDateTime(order.preferred_end_time) }}</strong>
            </div>
            <div>
              <span class="text-gray-600 block">Ghi chú:</span>
              <p class="mt-1 italic text-gray-700">{{ order.note || 'Không có' }}</p>
            </div>
          </div>
        </div>
        
        <!-- Thông tin khách hàng -->
        <div class="bg-blue-50 rounded-lg p-4 border border-blue-100">
          <h3 class="text-lg font-medium mb-3 flex items-center">
            <i class="el-icon-user mr-2"></i>Thông tin khách hàng
          </h3>
          <div class="space-y-2">
            <div class="flex justify-between">
              <span class="text-gray-600">Tên khách hàng:</span>
              <strong>{{ order.customer_name }}</strong>
            </div>
            <div v-if="order.customer_details?.phone" class="flex justify-between">
              <span class="text-gray-600">Số điện thoại:</span>
              <strong>{{ order.customer_details.phone }}</strong>
            </div>
            <div v-if="order.customer_details?.email" class="flex justify-between">
              <span class="text-gray-600">Email:</span>
              <strong>{{ order.customer_details.email }}</strong>
            </div>
            <div v-if="order.customer_details?.area" class="flex justify-between">
              <span class="text-gray-600 block">Khu vực:</span>
              <strong class="mt-1 text-gray-700">{{ order.customer_details.area }}</strong>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Chi tiết dịch vụ - Card style -->
      <div class="mb-5">
        <div class="shadow-sm border rounded-lg overflow-hidden">
          <div class="bg-green-50 p-3 border-b border-green-100">
            <h3 class="text-lg font-medium flex items-center">
              <i class="el-icon-s-goods mr-2"></i>Chi tiết dịch vụ
            </h3>
          </div>
          <div class="p-4">
            <div class="grid grid-cols-2 gap-4">
              <div>
                <p class="text-gray-600 mb-1">Loại dịch vụ</p>
                <p class="font-semibold">{{ order.service_details?.name }}</p>
              </div>
              <div>
                <p class="text-gray-600 mb-1">Giá mỗi m²</p>
                <p class="font-semibold">{{ formatCurrency(order.service_details?.price_per_m2 || 0) }}</p>
              </div>
              <div>
                <p class="text-gray-600 mb-1">Tổng diện tích</p>
                <p class="font-semibold">{{ order.area_m2 }} m²</p>
              </div>
              <div>
                <p class="text-gray-600 mb-1">Tổng giá tiền</p>
                <p class="font-semibold text-lg text-green-600">{{ order.cost_confirm }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Thời gian dự kiến - Timeline style -->
      <!-- <div class="mb-6">
        <div class="shadow-sm border rounded-lg overflow-hidden">
          <div class="bg-purple-50 p-3 border-b border-purple-100">
            <h3 class="text-lg font-medium flex items-center">
              <i class="el-icon-time mr-2"></i>Thời gian dự kiến
            </h3>
          </div>
          <div class="p-4">
            <div class="flex items-center">
              <div class="w-1/2 pr-2 text-center border-r">
                <p class="text-gray-600 mb-1">Bắt đầu</p>
                <p class="font-semibold">{{ formatDateTime(order.preferred_start_time) }}</p>
              </div>
              <div class="w-1/2 pl-2 text-center">
                <p class="text-gray-600 mb-1">Kết thúc</p>
                <p class="font-semibold">{{ formatDateTime(order.preferred_end_time) }}</p>
              </div>
            </div>
          </div>
        </div>
      </div> -->

      <!-- Hành động - Buttons clean layout -->
      <div v-if="order.status !== 'completed' && order.status !== 'rejected'" class="mt-8">
        <h3 class="text-lg font-medium mb-3">Hành động</h3>
        <div class="flex space-x-3">
          <el-button 
            type="danger" 
            @click="handleCancelOrder"
            size="medium" 
            plain
            icon="el-icon-close"
          >
            Hủy đơn hàng
          </el-button>
          <!-- <el-button
            type="primary"
            @click="$emit('assign-employee')"
            size="medium"
            plain
            icon="el-icon-user"
          >
            Phân công nhân viên
          </el-button> -->
        </div>
      </div>
    </div>
    <div v-else class="text-center p-10">
      <el-empty description="Không tìm thấy thông tin đơn hàng"></el-empty>
    </div>
  </el-card>
</template>

<style scoped>
.order-details-card {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05) !important;
}

.el-icon-document,
.el-icon-user,
.el-icon-s-goods,
.el-icon-time {
  font-size: 1.25rem;
}

.btn-centered {
  min-width: 150px; /* Đảm bảo độ rộng tối thiểu */
}

.btn-centered i {
  margin-right: 5px;
}

.space-y-2 > * + * {
  margin-top: 0.5rem;
}

/* Responsive text adjustments */
@media (max-width: 640px) {
  h2 {
    font-size: 1.25rem;
  }
  
  h3 {
    font-size: 1.125rem;
  }
}
</style>

<script setup>
import { defineProps, defineEmits } from 'vue';
import { ElMessageBox } from 'element-plus';
import { formatCurrency} from '../../../utils/formatters'
import { formatDate, formatDateTime } from '../../../utils/time';
import OrderService from '../../../services/dss/order';

const props = defineProps({
  order: Object,
  loading: Boolean
});

const emit = defineEmits(['update-status', 'cancel-order']);

// Calculate total amount
const calculateTotalAmount = (order) => {
  if (!order || !order.service_details || !order.area_m2) return 0;
  const area = parseFloat(order.area_m2);
  const pricePerM2 = order.service_details.price_per_m2 || 0;
  return area * pricePerM2;
};

// Get status label
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

// Get status type for color
const getStatusType = (status) => {
  const statusTypeMap = {
    'pending': 'warning',
    'confirmed': 'primary',
    'in_progress': 'info',
    'completed': 'success',
    'cancelled': 'danger'
  };
  return statusTypeMap[status] || '';
};

// Handle update status
// const handleUpdateStatus = () => {
//   ElMessageBox.prompt('Chọn trạng thái mới', 'Cập nhật trạng thái', {
//     confirmButtonText: 'Xác nhận',
//     cancelButtonText: 'Hủy',
//     inputType: 'select',
//     inputValue: props.order.status,
//     inputPlaceholder: 'Chọn trạng thái',
//     inputOptions: [
//       { value: 'pending', label: 'Chờ xử lý' },
//       { value: 'confirmed', label: 'Đã xác nhận' },
//       { value: 'in_progress', label: 'Đang xử lý' },
//       { value: 'completed', label: 'Hoàn thành' }
//     ]
//   }).then(({ value }) => {
//     emit('update-status', value);
//   }).catch(() => {
//     // User cancelled
//   });
// };

// Handle cancel order
const handleCancelOrder = () => {
  ElMessageBox.prompt('Vui lòng nhập lý do hủy đơn hàng', 'Xác nhận hủy', {
    confirmButtonText: 'Xác nhận',
    cancelButtonText: 'Hủy',
    type: 'warning',
    inputType: 'textarea',
    inputPlaceholder: 'Nhập lý do hủy đơn hàng...'
  }).then(async ({ value: reason }) => {
    const orderId = props.order.id;
    console.log('Hủy đơn hàng', orderId, 'Lý do:', reason);
    
    // Gọi API để hủy đơn hàng và ghi log
    await OrderService.rejectOrder(orderId, reason);
    
    //Cập nhật trạng thái
    await OrderService.updateOrderStatus(orderId, 'rejected');
    
    props.order.status = 'rejected';
  }).catch((error) => {
    // User cancelled
    console.log('Hủy bỏ hủy đơn hàng', error);
  });
};
</script>