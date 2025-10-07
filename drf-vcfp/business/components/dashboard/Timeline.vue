<template>
  <div class="timeline-container">
    <div v-for="(item, index) in items" :key="item.id" class="timeline-item">
      <!-- Timeline line -->
      <div class="timeline-line" v-if="index !== items.length - 1"></div>

      <!-- Timeline dot -->
      <div class="timeline-dot" :class="getDotClass(item.type)">
        <el-icon size="12">
          <component :is="getIcon(item.type)" />
        </el-icon>
      </div>

      <!-- Timeline content -->
      <div class="timeline-content">
        <div class="timeline-header">
          <h4 class="timeline-title">{{ item.title }}</h4>
          <span class="timeline-time">{{ item.time }}</span>
        </div>
        <p class="timeline-description">{{ item.description }}</p>
        <div class="timeline-meta" v-if="item.user || item.location">
          <span v-if="item.user" class="timeline-user">
            <el-icon size="14"><User /></el-icon>
            {{ item.user }}
          </span>
          <span v-if="item.location" class="timeline-location">
            <el-icon size="14"><Location /></el-icon>
            {{ item.location }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import {
  CircleCheckFilled,
  Warning,
  Plus,
  Star,
  User,
  Location,
  Clock,
} from "@element-plus/icons-vue";

defineProps({
  items: {
    type: Array,
    required: true,
    default: () => [],
  },
});

const getDotClass = (type) => {
  const classes = {
    success: "bg-green-500 text-white",
    warning: "bg-yellow-500 text-white",
    info: "bg-blue-500 text-white",
    error: "bg-red-500 text-white",
    rating: "bg-purple-500 text-white",
  };
  return classes[type] || "bg-gray-500 text-white";
};

const getIcon = (type) => {
  const icons = {
    success: CircleCheckFilled,
    warning: Warning,
    info: Plus,
    error: Warning,
    rating: Star,
  };
  return icons[type] || Clock;
};
</script>

<style scoped>
.timeline-container {
  position: relative;
  padding-left: 2rem;
}

.timeline-item {
  position: relative;
  margin-bottom: 1.5rem;
}

.timeline-line {
  position: absolute;
  left: -2rem;
  top: 2rem;
  width: 2px;
  height: calc(100% + 1.5rem);
  background-color: #e5e7eb;
}

.timeline-dot {
  position: absolute;
  left: -2.5rem;
  top: 0.25rem;
  width: 2rem;
  height: 2rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.timeline-content {
  background: white;
  border-radius: 0.5rem;
  padding: 1rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  border: 1px solid #f3f4f6;
}

.timeline-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 0.5rem;
}

.timeline-title {
  font-weight: 600;
  color: #1f2937;
  margin: 0;
  flex: 1;
}

.timeline-time {
  font-size: 0.75rem;
  color: #6b7280;
  white-space: nowrap;
  margin-left: 1rem;
}

.timeline-description {
  color: #4b5563;
  margin-bottom: 0.75rem;
  font-size: 0.875rem;
  line-height: 1.4;
}

.timeline-meta {
  display: flex;
  gap: 1rem;
  font-size: 0.75rem;
  color: #6b7280;
}

.timeline-user,
.timeline-location {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}
</style>
