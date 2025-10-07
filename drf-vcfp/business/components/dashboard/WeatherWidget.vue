<template>
  <div class="weather-widget">
    <div class="weather-header">
      <h3 class="weather-title">Thời Tiết Hôm Nay</h3>
      <div class="weather-location">
        <el-icon><Location /></el-icon>
        {{ location }}
      </div>
    </div>

    <div class="weather-main">
      <div class="weather-icon">
        <el-icon size="48" :class="getWeatherIconClass()">
          <component :is="getWeatherIcon()" />
        </el-icon>
      </div>

      <div class="weather-info">
        <div class="temperature">{{ temperature }}°C</div>
        <div class="condition">{{ condition }}</div>
        <div class="feels-like">Cảm giác như {{ feelsLike }}°C</div>
      </div>
    </div>

    <div class="weather-details">
      <div class="detail-item">
        <el-icon class="detail-icon"><View /></el-icon>
        <span class="detail-label">Tầm nhìn</span>
        <span class="detail-value">{{ visibility }} km</span>
      </div>

      <div class="detail-item">
        <el-icon class="detail-icon"><Cloudy /></el-icon>
        <span class="detail-label">Độ ẩm</span>
        <span class="detail-value">{{ humidity }}%</span>
      </div>

      <div class="detail-item">
        <el-icon class="detail-icon"><WindPower /></el-icon>
        <span class="detail-label">Gió</span>
        <span class="detail-value">{{ windSpeed }} km/h</span>
      </div>
    </div>

    <div class="weather-impact">
      <div class="impact-header">
        <el-icon class="impact-icon"><Warning /></el-icon>
        <span>Ảnh hưởng công việc</span>
      </div>
      <p class="impact-text">{{ getWeatherImpact() }}</p>
    </div>
  </div>
</template>

<script setup>
import {
  Location,
  Sunny,
  Cloudy,
  View,
  WindPower,
  Warning,
} from "@element-plus/icons-vue";

const props = defineProps({
  location: {
    type: String,
    default: "TP. Hồ Chí Minh",
  },
  temperature: {
    type: Number,
    default: 32,
  },
  condition: {
    type: String,
    default: "Nắng ít mây",
  },
  feelsLike: {
    type: Number,
    default: 35,
  },
  visibility: {
    type: Number,
    default: 10,
  },
  humidity: {
    type: Number,
    default: 75,
  },
  windSpeed: {
    type: Number,
    default: 12,
  },
  weatherType: {
    type: String,
    default: "sunny", // sunny, cloudy, rainy, stormy
  },
});

const getWeatherIcon = () => {
  const icons = {
    sunny: Sunny,
    cloudy: Cloudy,
    rainy: Cloudy,
    stormy: Warning,
  };
  return icons[props.weatherType] || Sunny;
};

const getWeatherIconClass = () => {
  const classes = {
    sunny: "text-yellow-500",
    cloudy: "text-gray-500",
    rainy: "text-blue-500",
    stormy: "text-red-500",
  };
  return classes[props.weatherType] || "text-yellow-500";
};

const getWeatherImpact = () => {
  if (props.temperature > 35) {
    return "Thời tiết nóng, cần chú ý sức khỏe nhân viên làm việc ngoài trời";
  } else if (props.weatherType === "rainy") {
    return "Có mưa, có thể ảnh hưởng đến lịch trình công việc ngoài trời";
  } else if (props.visibility < 5) {
    return "Tầm nhìn hạn chế, cần cẩn thận khi di chuyển";
  } else {
    return "Thời tiết thuận lợi cho các hoạt động dọn dẹp";
  }
};
</script>

<style scoped>
.weather-widget {
  background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
  border-radius: 1rem;
  padding: 1.5rem;
  color: white;
  position: relative;
  overflow: hidden;
}

.weather-widget::before {
  content: "";
  position: absolute;
  top: -50%;
  right: -50%;
  width: 100%;
  height: 100%;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  pointer-events: none;
}

.weather-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.weather-title {
  font-weight: 600;
  margin: 0;
  color: white;
}

.weather-location {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.875rem;
  opacity: 0.9;
}

.weather-main {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.weather-icon {
  flex-shrink: 0;
}

.weather-info {
  flex: 1;
}

.temperature {
  font-size: 2.5rem;
  font-weight: bold;
  line-height: 1;
  margin-bottom: 0.25rem;
}

.condition {
  font-size: 1.1rem;
  margin-bottom: 0.25rem;
  opacity: 0.9;
}

.feels-like {
  font-size: 0.875rem;
  opacity: 0.8;
}

.weather-details {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
  margin-bottom: 1.5rem;
  padding-top: 1rem;
  border-top: 1px solid rgba(255, 255, 255, 0.2);
}

.detail-item {
  text-align: center;
}

.detail-icon {
  display: block;
  margin: 0 auto 0.25rem;
  opacity: 0.8;
}

.detail-label {
  display: block;
  font-size: 0.75rem;
  opacity: 0.8;
  margin-bottom: 0.25rem;
}

.detail-value {
  display: block;
  font-weight: 600;
  font-size: 0.875rem;
}

.weather-impact {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 0.5rem;
  padding: 0.75rem;
  backdrop-filter: blur(10px);
}

.impact-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 500;
  margin-bottom: 0.5rem;
}

.impact-icon {
  color: #ffeaa7;
}

.impact-text {
  font-size: 0.875rem;
  opacity: 0.9;
  margin: 0;
  line-height: 1.4;
}
</style>
