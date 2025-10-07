<template>
  <div class="employee-stats-grid">
    <div v-for="employee in employees" :key="employee.id" class="employee-card">
      <!-- Employee Avatar & Info -->
      <div class="employee-header">
        <div class="employee-avatar">
          <img
            v-if="employee.avatar"
            :src="employee.avatar"
            :alt="employee.name"
            class="avatar-image"
          />
          <div v-else class="avatar-placeholder">
            {{ getInitials(employee.name) }}
          </div>
          <div
            class="status-indicator"
            :class="getStatusClass(employee.status)"
          ></div>
        </div>
        <div class="employee-info">
          <h4 class="employee-name">{{ employee.name }}</h4>
          <p class="employee-role">{{ employee.role }}</p>
          <div class="employee-status">
            <span
              class="status-text"
              :class="getStatusTextClass(employee.status)"
            >
              {{ getStatusText(employee.status) }}
            </span>
          </div>
        </div>
      </div>

      <!-- Performance Metrics -->
      <div class="performance-metrics">
        <div class="metric-item">
          <div class="metric-label">Hoàn thành</div>
          <div class="metric-value">
            {{ employee.completedTasks }}/{{ employee.totalTasks }}
          </div>
          <div class="metric-bar">
            <div
              class="metric-progress"
              :style="{
                width:
                  (employee.completedTasks / employee.totalTasks) * 100 + '%',
              }"
            ></div>
          </div>
        </div>

        <div class="metric-item">
          <div class="metric-label">Đánh giá</div>
          <div class="metric-value">{{ employee.rating }}/5</div>
          <div class="rating-stars">
            <el-icon
              v-for="star in 5"
              :key="star"
              :class="star <= employee.rating ? 'star-filled' : 'star-empty'"
            >
              <StarFilled v-if="star <= employee.rating" />
              <Star v-else />
            </el-icon>
          </div>
        </div>

        <div class="metric-item">
          <div class="metric-label">Hiệu suất</div>
          <div class="metric-value">{{ employee.efficiency }}%</div>
          <div
            class="efficiency-indicator"
            :class="getEfficiencyClass(employee.efficiency)"
          >
            <el-icon><TrendCharts /></el-icon>
          </div>
        </div>
      </div>

      <!-- Current Task -->
      <div class="current-task" v-if="employee.currentTask">
        <div class="task-header">
          <el-icon class="task-icon"><Clock /></el-icon>
          <span class="task-label">Nhiệm vụ hiện tại</span>
        </div>
        <p class="task-description">{{ employee.currentTask }}</p>
        <div class="task-location" v-if="employee.currentLocation">
          <el-icon><Location /></el-icon>
          {{ employee.currentLocation }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import {
  Star,
  StarFilled,
  Clock,
  Location,
  TrendCharts,
} from "@element-plus/icons-vue";

defineProps({
  employees: {
    type: Array,
    required: true,
    default: () => [],
  },
});

const getInitials = (name) => {
  return name
    .split(" ")
    .map((word) => word[0])
    .join("")
    .toUpperCase()
    .slice(0, 2);
};

const getStatusClass = (status) => {
  const classes = {
    online: "bg-green-500",
    busy: "bg-red-500",
    away: "bg-yellow-500",
    offline: "bg-gray-400",
  };
  return classes[status] || "bg-gray-400";
};

const getStatusText = (status) => {
  const texts = {
    online: "Đang hoạt động",
    busy: "Đang bận",
    away: "Tạm vắng",
    offline: "Offline",
  };
  return texts[status] || "Không rõ";
};

const getStatusTextClass = (status) => {
  const classes = {
    online: "text-green-600",
    busy: "text-red-600",
    away: "text-yellow-600",
    offline: "text-gray-500",
  };
  return classes[status] || "text-gray-500";
};

const getEfficiencyClass = (efficiency) => {
  if (efficiency >= 90) return "text-green-500";
  if (efficiency >= 70) return "text-blue-500";
  if (efficiency >= 50) return "text-yellow-500";
  return "text-red-500";
};
</script>

<style scoped>
.employee-stats-grid {
  display: grid;
  gap: 1.5rem;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
}

.employee-card {
  background: white;
  border-radius: 1rem;
  padding: 1.5rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  border: 1px solid #f3f4f6;
  transition: all 0.3s ease;
}

.employee-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px -3px rgba(0, 0, 0, 0.1);
}

.employee-header {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.employee-avatar {
  position: relative;
  flex-shrink: 0;
}

.avatar-image,
.avatar-placeholder {
  width: 3.5rem;
  height: 3.5rem;
  border-radius: 50%;
  border: 3px solid white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.avatar-placeholder {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 600;
  font-size: 1rem;
}

.status-indicator {
  position: absolute;
  bottom: 2px;
  right: 2px;
  width: 1rem;
  height: 1rem;
  border-radius: 50%;
  border: 2px solid white;
}

.employee-info {
  flex: 1;
  min-width: 0;
}

.employee-name {
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 0.25rem 0;
  font-size: 1.1rem;
}

.employee-role {
  color: #6b7280;
  margin: 0 0 0.5rem 0;
  font-size: 0.875rem;
}

.status-text {
  font-size: 0.75rem;
  font-weight: 500;
}

.performance-metrics {
  space-y: 1rem;
}

.metric-item {
  margin-bottom: 1rem;
}

.metric-item:last-child {
  margin-bottom: 0;
}

.metric-label {
  font-size: 0.875rem;
  color: #6b7280;
  margin-bottom: 0.25rem;
}

.metric-value {
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 0.5rem;
}

.metric-bar {
  width: 100%;
  height: 0.5rem;
  background-color: #f3f4f6;
  border-radius: 0.25rem;
  overflow: hidden;
}

.metric-progress {
  height: 100%;
  background: linear-gradient(90deg, #3b82f6, #1d4ed8);
  transition: width 0.5s ease;
}

.rating-stars {
  display: flex;
  gap: 0.25rem;
}

.star-filled {
  color: #fbbf24;
}

.star-empty {
  color: #d1d5db;
}

.efficiency-indicator {
  display: inline-flex;
  align-items: center;
  font-weight: 600;
}

.current-task {
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid #f3f4f6;
}

.task-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}

.task-icon {
  color: #6b7280;
}

.task-label {
  font-size: 0.875rem;
  font-weight: 500;
  color: #374151;
}

.task-description {
  color: #4b5563;
  margin-bottom: 0.5rem;
  font-size: 0.875rem;
  line-height: 1.4;
}

.task-location {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.75rem;
  color: #6b7280;
}
</style>
