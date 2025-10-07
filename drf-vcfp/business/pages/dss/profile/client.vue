<script setup>
import { ref, onMounted } from 'vue'
import customerApi from '@/services/dss/users/customer'
definePageMeta({
  middleware: 'role-based'
})

const user = ref(null)
const loading = ref(true)
const error = ref(null)

const fetchUserInfo = async () => {
  try {
    loading.value = true
    error.value = null
    console.log('Calling customerApi.getUser()...')
    
    const response = await customerApi.getUser()
    console.log('API response:', response)
    console.log('Response data:', response.data)
    
    // Kiểm tra cấu trúc response
    const userData = response.data || response
    user.value = userData
    console.log('Customer info loaded:', userData)
    console.log('User ref after assignment:', user.value)
  } catch (err) {
    console.error('Error loading customer info:', err)
    error.value = err.response?.data?.detail || 'Không thể tải thông tin người dùng'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchUserInfo()
})
</script>

<template>
  <div class="profile-container">
    <div class="profile-wrapper">
      
      <!-- Header -->
      <div class="profile-header">
        <div class="avatar-section">
          <div class="avatar">
            <span class="avatar-text">{{ user?.name?.charAt(0)?.toUpperCase() || 'U' }}</span>
          </div>
          <div class="user-basic-info">
            <h1 class="user-name">{{ user?.name || 'Loading...' }}</h1>
            <p class="user-email">{{ user?.email || '' }}</p>
          </div>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="loading-card">
        <div class="loading-spinner"></div>
        <p>Đang tải thông tin...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="error-card">
        <div class="error-icon">⚠️</div>
        <p>{{ error }}</p>
        <button @click="fetchUserInfo" class="retry-button">Thử lại</button>
      </div>

      <!-- Profile Info Cards -->
      <div v-else-if="user" class="profile-content">
        
        <!-- Personal Information Card -->
        <div class="info-card">
          <div class="card-header">
            <h2 class="card-title">Thông tin cá nhân</h2>
            <button class="edit-button">Chỉnh sửa</button>
          </div>
          <div class="card-content">
            <div class="info-row">
              <div class="info-label">Tên</div>
              <div class="info-value">{{ user.name }}</div>
            </div>
            <div class="info-row">
              <div class="info-label">Email</div>
              <div class="info-value">{{ user.email }}</div>
            </div>
            <div class="info-row">
              <div class="info-label">Số điện thoại</div>
              <div class="info-value">{{ user.phone || 'Chưa cập nhật' }}</div>
            </div>
          </div>
        </div>

        <!-- Address Information Card -->
        <div class="info-card">
          <div class="card-header">
            <h2 class="card-title">Thông tin địa chỉ</h2>
            <button class="edit-button">Chỉnh sửa</button>
          </div>
          <div class="card-content">
            <div class="info-row">
              <div class="info-label">Địa chỉ</div>
              <div class="info-value">{{ user.address || 'Chưa cập nhật' }}</div>
            </div>
            <div class="info-row">
              <div class="info-label">Khu vực</div>
              <div class="info-value">{{ user.area || 'Chưa cập nhật' }}</div>
            </div>
          </div>
        </div>

        <!-- Account Settings Card -->
        <div class="info-card">
          <div class="card-header">
            <h2 class="card-title">Cài đặt tài khoản</h2>
            <button class="edit-button">Chỉnh sửa</button>
          </div>
          <div class="card-content">
            <div class="info-row">
              <div class="info-label">Ngày tạo tài khoản</div>
              <div class="info-value">{{ new Date(user.created_at).toLocaleDateString('vi-VN') }}</div>
            </div>
            <div class="info-row">
              <div class="info-label">Lần cập nhật cuối</div>
              <div class="info-value">{{ new Date(user.updated_at).toLocaleDateString('vi-VN') }}</div>
            </div>
          </div>
        </div>

      </div>
      
    </div>
  </div>
</template>

<style scoped>
/* Facebook-style Profile Layout */
.profile-container {
  min-height: 100vh;
  background-color: #f0f2f5;
  padding: 20px 0;
}

.profile-wrapper {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 20px;
}

/* Profile Header */
.profile-header {
  background: #fff;
  border-radius: 8px;
  padding: 24px;
  margin-bottom: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.avatar-section {
  display: flex;
  align-items: center;
  gap: 16px;
}

.avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: linear-gradient(45deg, #4267b2, #365899);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.avatar-text {
  font-size: 32px;
  font-weight: 600;
  color: white;
}

.user-basic-info {
  flex: 1;
}

.user-name {
  font-size: 32px;
  font-weight: 700;
  color: #1c1e21;
  margin: 0 0 4px 0;
}

.user-email {
  font-size: 15px;
  color: #65676b;
  margin: 0;
}

/* Loading Card */
.loading-card {
  background: #fff;
  border-radius: 8px;
  padding: 40px;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #e4e6ea;
  border-top: 4px solid #4267b2;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 16px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Error Card */
.error-card {
  background: #fff;
  border-radius: 8px;
  padding: 40px;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.error-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.retry-button {
  background: #4267b2;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  margin-top: 16px;
  transition: background-color 0.2s;
}

.retry-button:hover {
  background: #365899;
}

/* Profile Content */
.profile-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* Info Cards */
.info-card {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid #e4e6ea;
}

.card-title {
  font-size: 20px;
  font-weight: 700;
  color: #1c1e21;
  margin: 0;
}

.edit-button {
  background: #e4e6ea;
  color: #4b4f56;
  border: none;
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s;
}

.edit-button:hover {
  background: #d8dadf;
}

.card-content {
  padding: 0;
}

.info-row {
  display: flex;
  padding: 16px 24px;
  border-bottom: 1px solid #f0f2f5;
}

.info-row:last-child {
  border-bottom: none;
}

.info-label {
  flex: 0 0 150px;
  font-size: 15px;
  font-weight: 600;
  color: #4b4f56;
}

.info-value {
  flex: 1;
  font-size: 15px;
  color: #1c1e21;
  word-break: break-word;
}

/* Responsive Design */
@media (max-width: 768px) {
  .profile-wrapper {
    padding: 0 16px;
  }
  
  .profile-header {
    padding: 20px 16px;
  }
  
  .avatar-section {
    flex-direction: column;
    text-align: center;
    gap: 12px;
  }
  
  .user-name {
    font-size: 24px;
  }
  
  .card-header {
    padding: 16px;
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
  
  .info-row {
    flex-direction: column;
    gap: 4px;
    padding: 12px 16px;
  }
  
  .info-label {
    flex: none;
    font-size: 13px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }
}

/* Hover Effects */
.info-card:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.12);
  transition: box-shadow 0.2s ease;
}
</style>
