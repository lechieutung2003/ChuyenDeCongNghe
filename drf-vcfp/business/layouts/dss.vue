<template>
  <div class="w-full h-full flex bg-tertiary-light align-center justify-center">
    <div v-if="!authenticated" class="lg:py-20 py-6">
      <LoginForm>
        <div class="flex text-center justify-center">
          <AmozLogo class="h-20" />
        </div>
        <div class="my-5">
          <p class="lg:text-l text-center font-bold">
            {{ $t("welcome_to_dss") }}
          </p>
        </div>
      </LoginForm>
    </div>
    <div v-else class="absolute w-full">
      <TopbarNav />
      <div class="flex flex-row-content">
        <aside>
          <Sidebar>
            <template #header>
              <h5 class="text-white font-bold">DSS</h5>
            </template>

            <!-- Admin menu -->
            <el-menu-item index="/dss/dashboard" v-if="isAdmin">
              <span>Dashboard</span>
            </el-menu-item>
            <el-menu-item index="/dss/services" v-if="isAdmin">
              <span>Quản lý Dịch vụ</span>
            </el-menu-item>
            <!-- <el-menu-item index="/dss/orders" v-if="isAdmin || isStaff">
              <span>Quản lý Đơn hàng</span>
            </el-menu-item> -->
            <el-menu-item index="/dss/users" v-if="isAdmin">
              <span>Quản lý Nhân viên</span>
            </el-menu-item>
            <el-menu-item index="/dss/customers" v-if="isAdmin">
              <span>Quản lý Khách hàng</span>
            </el-menu-item>
            <!-- <el-menu-item index="/dss/tasks" v-if="isAdmin">
              <span>Giao task cho nhân viên</span>
            </el-menu-item> -->

            <!-- Admin + Staff đơn hàng -->
            <el-menu-item
              :index="isAdmin ? '/dss/orders' : '/dss/employee-orders'"
              v-if="isAdmin || isStaff"
            >
              <span>{{ isAdmin ? "Quản lý Đơn hàng" : "Đơn của tôi" }}</span>
            </el-menu-item>

            <!-- Thông tin cá nhân luôn hiển thị -->
            <el-menu-item index="/dss/profile">
              <span>Thông tin cá nhân</span>
            </el-menu-item>
          </Sidebar>
        </aside>
        <div class="flex-auto">
          <slot />
        </div>
      </div>
      <footer class="w-full bg-gray-100 flex justify-center">
        <FooterContent />
      </footer>
    </div>
  </div>
</template>

<script setup>
import AmozLogo from "/assets/icons/Logo.svg";
import { useOauthStore } from "@/stores/oauth";
import { computed } from "vue";

const { t } = useI18n();

const oauthStore = useOauthStore();
const authenticated = computed(() => {
  const { tokenInfo } = oauthStore;
  if (!tokenInfo) return false;
  const { access_token } = tokenInfo;
  if (!access_token) return false;
  return access_token.length > 0;
});

const isAdmin = computed(
  () => oauthStore.user?.isAdmin || oauthStore.tokenInfo?.isSuperuser
);
const isStaff = computed(
  () => oauthStore.user?.isStaff || oauthStore.tokenInfo?.isStaff
);
const isGuest = computed(
  () => oauthStore.user?.isGuest || oauthStore.tokenInfo?.isGuest
);
</script>

<style scoped></style>
