<script setup>
definePageMeta({
  layout: "anonymous",
});

import { computed, watchEffect } from "vue";
import { useRouter } from "vue-router";
import { useOauthStore } from "@/stores/oauth";
import GuestInfo from "@/components/GuestInfo.vue";
import LoginForm from "@/components/LoginForm.vue";

const router = useRouter();
const oauthStore = useOauthStore();

// Xác định quyền
const isAdmin = computed(() => {
  return oauthStore.hasAllScopes([
    "users:view",
    "users:edit",
    "roles:view",
    "roles:edit",
  ]);
});

const isStaff = computed(() => {
  return oauthStore.hasOneOfScopes(["employees:view", "tasks:view-mine"]);
});

const isGuest = computed(() => {
  return (
    oauthStore.hasAllScopes(["users:view-mine"]) &&
    !oauthStore.hasOneOfScopes(["employees:view", "roles:view"])
  );
});
const isEmployee = computed(() => {
  return oauthStore.hasOneOfScopes(["employees:view"]);
});


const isLoggedIn = computed(() => {
  const token = oauthStore.tokenInfo?.access_token;
  const currentTime = Math.floor(Date.now() / 1000);
  const tokenValid = oauthStore.tokenInfo?.exp && oauthStore.tokenInfo.exp > currentTime;
  return !!(token && tokenValid);
});

// redirect nếu là admin hoặc employee - CHỈ KHI ĐÃ LOGIN
watchEffect(() => {
  if (!isLoggedIn.value) {
    // Nếu chưa login, không redirect, hiển thị login form
    return;
  }
  
  if (isAdmin.value) {
    // Chỉ admin mới được vào dashboard
    router.push("/dss/dashboard");
  } 
  else if (isEmployee.value || isStaff.value) {
    // Employee redirect tới employee-orders thay vì dashboard
    router.push("/dss/employee-orders");
  }
  else if (isGuest.value) {
    router.push("/dss/home");
  }
});



console.log("isAdmin:", isAdmin.value);
console.log("isStaff:", isStaff.value);
console.log("isGuest:", isGuest.value);
console.log("tokenInfo:", oauthStore.tokenInfo);
</script>

<template>
  <div class="center-container">
    <div style="width:100%;max-width:500px;">
      <LoginForm v-if="!isLoggedIn" />
      <GuestInfo v-else-if="isGuest" />
    </div>
  </div>
</template>
<style scoped>
.center-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
}
.welcome-text {
  margin-top: 24px;
  color: #444;
  font-size: 16px;
  text-align: center;
}
</style>