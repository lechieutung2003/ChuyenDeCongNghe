<template>
  <div class="access-denied-container">
    <div class="access-denied-content">
      <div class="icon-section">
        <el-icon size="80" color="#f56c6c">
          <Warning />
        </el-icon>
      </div>

      <h1 class="title">Truy cập bị từ chối</h1>
      <p class="message">
        Bạn không có quyền truy cập vào trang này. Vui lòng liên hệ quản trị
        viên để được hỗ trợ.
      </p>

      <div class="actions">
        <el-button type="primary" @click="goBack">
          <el-icon><Back /></el-icon>
          Quay lại
        </el-button>
        <el-button @click="goHome">
          <el-icon><HomeFilled /></el-icon>
          Trang chủ
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { Warning, Back, HomeFilled } from "@element-plus/icons-vue";
import { useRouter } from "vue-router";
import { useOauthStore } from "@/stores/oauth";

const router = useRouter();
const oauthStore = useOauthStore();

definePageMeta({
  layout: false, // Không sử dụng layout nào để loại bỏ topbar
});

const goBack = () => {
  router.go(-1);
};

const goHome = () => {
  // Redirect based on user role
  const { tokenInfo } = oauthStore;

  if (tokenInfo?.isStaff || tokenInfo?.isSuperuser) {
    router.push("/dss/dashboard");
  } else if (oauthStore.hasOneOfScopes(["employees:view"])) {
    router.push("/dss/employee-orders");
  } else {
    router.push("/dss/profile/client");
  }
};
</script>

<style scoped>
.access-denied-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f5f7fa;
  padding: 20px;
}

.access-denied-content {
  background: white;
  border-radius: 12px;
  padding: 60px 40px;
  text-align: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  max-width: 500px;
  width: 100%;
}

.icon-section {
  margin-bottom: 30px;
}

.title {
  font-size: 28px;
  font-weight: 600;
  color: #303133;
  margin: 0 0 20px 0;
}

.message {
  font-size: 16px;
  color: #606266;
  line-height: 1.6;
  margin: 0 0 40px 0;
}

.actions {
  display: flex;
  gap: 12px;
  justify-content: center;
  flex-wrap: wrap;
}

@media (max-width: 640px) {
  .access-denied-content {
    padding: 40px 20px;
  }

  .title {
    font-size: 24px;
  }

  .actions {
    flex-direction: column;
    align-items: center;
  }

  .actions .el-button {
    width: 200px;
  }
}
</style>
