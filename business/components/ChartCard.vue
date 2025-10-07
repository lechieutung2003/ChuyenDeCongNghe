<template>
  <div class="bg-white rounded-lg shadow-md p-6">
    <div class="flex items-center justify-between mb-6">
      <h3 class="text-lg font-semibold text-gray-900">{{ title }}</h3>
      <el-icon v-if="icon" class="text-blue-600" size="24">
        <component :is="icon" />
      </el-icon>
    </div>

    <!-- Chart Content -->
    <div class="relative">
      <!-- Revenue Chart -->
      <div v-if="type === 'revenue'" class="space-y-4">
        <div class="text-center mb-4">
          <p class="text-2xl font-bold text-green-600">
            {{ formatCurrency(totalRevenue) }}
          </p>
          <p class="text-sm text-gray-500">Tổng doanh thu 7 ngày qua</p>
        </div>

        <div class="space-y-2">
          <div
            v-for="(item, index) in chartData?.revenue || []"
            :key="index"
            class="flex items-center justify-between p-2 rounded hover:bg-gray-50"
          >
            <span class="text-sm text-gray-600">{{
              formatDate(item.date)
            }}</span>
            <span class="font-medium text-green-600">{{
              formatCurrency(item.amount)
            }}</span>
          </div>
        </div>
      </div>

      <!-- Task Status Chart -->
      <div v-else-if="type === 'tasks'" class="space-y-4">
        <div class="grid grid-cols-3 gap-4 mb-4">
          <div class="text-center">
            <p class="text-xl font-bold text-green-600">
              {{ getTaskTotal("completed") }}
            </p>
            <p class="text-xs text-gray-500">Hoàn thành</p>
          </div>
          <div class="text-center">
            <p class="text-xl font-bold text-blue-600">
              {{ getTaskTotal("in_progress") }}
            </p>
            <p class="text-xs text-gray-500">Đang làm</p>
          </div>
          <div class="text-center">
            <p class="text-xl font-bold text-orange-600">
              {{ getTaskTotal("pending") }}
            </p>
            <p class="text-xs text-gray-500">Chờ xử lý</p>
          </div>
        </div>

        <!-- Simple Progress Bars -->
        <div class="space-y-3">
          <div class="flex items-center gap-3">
            <div class="w-20 text-xs text-gray-600">Hoàn thành</div>
            <div class="flex-1 bg-gray-200 rounded-full h-2">
              <div
                class="bg-green-500 h-2 rounded-full transition-all duration-500"
                :style="{ width: getTaskPercentage('completed') + '%' }"
              ></div>
            </div>
            <span class="text-xs text-gray-500"
              >{{ getTaskPercentage("completed") }}%</span
            >
          </div>

          <div class="flex items-center gap-3">
            <div class="w-20 text-xs text-gray-600">Đang làm</div>
            <div class="flex-1 bg-gray-200 rounded-full h-2">
              <div
                class="bg-blue-500 h-2 rounded-full transition-all duration-500"
                :style="{ width: getTaskPercentage('in_progress') + '%' }"
              ></div>
            </div>
            <span class="text-xs text-gray-500"
              >{{ getTaskPercentage("in_progress") }}%</span
            >
          </div>

          <div class="flex items-center gap-3">
            <div class="w-20 text-xs text-gray-600">Chờ xử lý</div>
            <div class="flex-1 bg-gray-200 rounded-full h-2">
              <div
                class="bg-orange-500 h-2 rounded-full transition-all duration-500"
                :style="{ width: getTaskPercentage('pending') + '%' }"
              ></div>
            </div>
            <span class="text-xs text-gray-500"
              >{{ getTaskPercentage("pending") }}%</span
            >
          </div>
        </div>
      </div>

      <!-- Performance Trends -->
      <div v-else-if="type === 'performance'" class="space-y-4">
        <div class="grid grid-cols-2 gap-4">
          <div class="text-center p-3 bg-blue-50 rounded">
            <p class="text-lg font-bold text-blue-600">{{ avgRating }}/5.0</p>
            <p class="text-xs text-gray-600">Đánh giá TB</p>
          </div>
          <div class="text-center p-3 bg-green-50 rounded">
            <p class="text-lg font-bold text-green-600">{{ avgTime }}h</p>
            <p class="text-xs text-gray-600">Thời gian TB</p>
          </div>
        </div>

        <div class="mt-4">
          <div class="flex items-center justify-between mb-2">
            <span class="text-sm text-gray-600">Hiệu suất tổng thể</span>
            <span class="text-sm font-medium text-blue-600"
              >{{ performance }}%</span
            >
          </div>
          <div class="w-full bg-gray-200 rounded-full h-3">
            <div
              class="bg-gradient-to-r from-blue-500 to-green-500 h-3 rounded-full transition-all duration-500"
              :style="{ width: performance + '%' }"
            ></div>
          </div>
        </div>
      </div>

      <!-- Default/Loading State -->
      <div v-else class="text-center py-8">
        <el-icon class="text-gray-400 text-4xl mb-2"><TrendCharts /></el-icon>
        <p class="text-gray-500">Đang tải dữ liệu biểu đồ...</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";
import { TrendCharts } from "@element-plus/icons-vue";

const props = defineProps({
  title: {
    type: String,
    required: true,
  },
  type: {
    type: String,
    required: true,
    validator: (value) => ["revenue", "tasks", "performance"].includes(value),
  },
  chartData: {
    type: Object,
    default: null,
  },
  icon: {
    type: Object,
    default: null,
  },
  avgRating: {
    type: Number,
    default: 4.8,
  },
  avgTime: {
    type: Number,
    default: 2.3,
  },
  performance: {
    type: Number,
    default: 85,
  },
});

// Computed properties
const totalRevenue = computed(() => {
  if (!props.chartData?.revenue) return 0;
  return props.chartData.revenue.reduce((sum, item) => sum + item.amount, 0);
});

// Helper methods
const formatCurrency = (amount) => {
  return new Intl.NumberFormat("vi-VN", {
    style: "currency",
    currency: "VND",
    maximumFractionDigits: 0,
  }).format(amount);
};

const formatDate = (dateStr) => {
  const date = new Date(dateStr);
  return date.toLocaleDateString("vi-VN", {
    day: "2-digit",
    month: "2-digit",
  });
};

const getTaskTotal = (status) => {
  if (!props.chartData?.tasks || props.chartData.tasks[status] === undefined)
    return 0;

  // Handle both array and number formats
  const value = props.chartData.tasks[status];
  return Array.isArray(value)
    ? value.reduce((sum, val) => sum + val, 0) // Array format
    : value || 0; // Number format
};

const getTaskPercentage = (status) => {
  const total =
    getTaskTotal("completed") +
    getTaskTotal("in_progress") +
    getTaskTotal("pending");
  if (total === 0) return 0;
  return Math.round((getTaskTotal(status) / total) * 100);
};
</script>

<style scoped>
.hover\:bg-gray-50:hover {
  background-color: #f9fafb;
}
</style>
