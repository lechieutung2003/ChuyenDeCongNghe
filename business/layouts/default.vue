<template>
  <div class="w-full h-full flex bg-tertiary-light align-center justify-center">
    <div v-if="!authenticated" class="lg:py-20 py-6">
      <LoginForm>
        <div class="flex text-center justify-center">
          <AmozLogo class="h-20" />
        </div>
        <div class="my-5">
          <p class="lg:text-l text-center font-bold">
            {{ $t("welcome_to_amoz") }}
          </p>
        </div>
      </LoginForm>
    </div>
    <div v-else class="w-full">
      <TopbarNav v-if="!isCustomer" />
      <UserTopbar v-else />
      <div class="pt-20">
        <slot />
      </div>
      <footer v-if="!isCustomer" class="w-full bg-gray-100 flex justify-center">
        <FooterContent />
      </footer>
    </div>
  </div>
</template>
<script setup>
import AmozLogo from "~/assets/icons/Logo.svg";
import { More } from "@element-plus/icons-vue";
import { useOauthStore } from "@/stores/oauth";
import UserTopbar from '@/components/topbar/UserTopbar.vue'
import { computed } from "vue";
const oauthStore = useOauthStore();
const authenticated = computed(() => {
  const { tokenInfo } = oauthStore;
  if (!tokenInfo) return false;
  const { access_token } = tokenInfo;
  if (!access_token) return false;
  return access_token.length > 0;
});

const isCustomer = computed(() => {
  return oauthStore.user?.role === 'customer'
    || oauthStore.user?.role === 'Guest'
    || oauthStore.hasOneOfScopes?.(['customers:view-mine', 'users:view-mine']);
});
</script>