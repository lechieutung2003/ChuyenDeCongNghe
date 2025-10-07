<template>
  <header :class="['user-topbar', { 'scrolled': isScrolled }]">
    <div class="user-topbar-wrapper">
      <!-- Logo với hiệu ứng clean, sparkle -->
      <div class="company-name" @click="goHome">
        <div class="logo">
          <span class="logo-icon">✨</span>
          <h1 class="logo-text">Clean Go</h1>
          <div class="sparkle sparkle-1"></div>
          <div class="sparkle sparkle-2"></div>
          <div class="sparkle sparkle-3"></div>
        </div>
      </div>
      
      <!-- Navigation với icon dọn dẹp -->
      <nav class="nav-right">
        <span class="nav-link" :class="{ active: selected === 'about' }" @click="selectMenu('about', goAbout)">
          <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
            <circle cx="12" cy="7" r="4"></circle>
          </svg>
          <span class="nav-text">{{ $t('nav_about') }}</span>
        </span>
        
        <span class="nav-link" :class="{ active: selected === 'services' }" @click="selectMenu('services', goServices)">
          <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M3 12h18m-9 4.5L21 7.5M12 16.5L3 7.5"></path>
          </svg>
          <span class="nav-text">{{ $t('nav_services') }}</span>
        </span>
        
        <span class="nav-link" :class="{ active: selected === 'contact' }" @click="selectMenu('contact', goContact)">
          <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path>
            <polyline points="22,6 12,13 2,6"></polyline>
          </svg>
          <span class="nav-text">{{ $t('nav_contact') }}</span>
        </span>
        
        <span class="nav-link orders-link" :class="{ active: selected === 'orders' }" @click="selectMenu('orders', goOrders)">
          <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M9 11H5a2 2 0 0 0-2 2v7a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7a2 2 0 0 0-2-2h-4"></path>
            <path d="M9 11V5a2 2 0 0 1 4 0v6"></path>
          </svg>
          <span class="nav-text">{{ $t('nav_orders') }}</span>
        </span>
        
        <span class="cta-btn" :class="{ active: selected === 'create' }" @click="selectMenu('create', goCreateOrder)">
          <div class="cta-content">
            <svg class="cta-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
              <circle cx="12" cy="12" r="10"></circle>
              <line x1="12" y1="8" x2="12" y2="16"></line>
              <line x1="8" y1="12" x2="16" y2="12"></line>
            </svg>
            <span>{{ $t('nav_create_order') }}</span>
          </div>
          <div class="cta-shine"></div>
        </span>
        
        <!-- Language Switcher -->
        <div class="language-wrapper">
          <div class="language-toggle" @click="toggleLangMenu">
            <span class="lang-flag">{{ getCurrentLangFlag }}</span>
            <span class="lang-text">{{ getCurrentLangName }}</span>
            <svg class="lang-arrow" :class="{ 'rotated': showLangMenu }" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="6,9 12,15 18,9"></polyline>
            </svg>
          </div>
          
          <transition name="dropdown">
            <div v-if="showLangMenu" class="language-menu" @click.stop>
              <div class="language-item" :class="{ active: locale === 'vi' }" @click="changeLanguage('vi')">
                <span class="lang-flag">🇻🇳</span>
                <span>Tiếng Việt</span>
                <svg v-if="locale === 'vi'" class="check-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polyline points="20,6 9,17 4,12"></polyline>
                </svg>
              </div>
              <div class="language-item" :class="{ active: locale === 'en' }" @click="changeLanguage('en')">
                <span class="lang-flag">🇺🇸</span>
                <span>English</span>
                <svg v-if="locale === 'en'" class="check-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polyline points="20,6 9,17 4,12"></polyline>
                </svg>
              </div>
            </div>
          </transition>
        </div>
        
        <!-- Avatar dropdown với hiệu ứng clean -->
        <div class="profile-wrapper">
          <div class="avatar-container" @click="toggleMenu">
            <el-avatar class="avatar" :size="40">{{ initials }}</el-avatar>
            <div class="avatar-ring"></div>
          </div>
          
          <transition name="dropdown">
            <div v-if="showMenu" class="dropdown-menu" @click.stop>
              <div class="dropdown-item" @click="goProfile">
                <svg class="dropdown-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                  <circle cx="12" cy="7" r="4"></circle>
                </svg>
                <span>{{ $t('nav_profile') }}</span>
              </div>
              <div class="dropdown-item logout" @click="logout">
                <svg class="dropdown-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
                  <polyline points="16,17 21,12 16,7"></polyline>
                  <line x1="21" y1="12" x2="9" y2="12"></line>
                </svg>
                <span>{{ $t('nav_logout') }}</span>
              </div>
            </div>
          </transition>
        </div>
      </nav>
    </div>
  </header>
</template>

<script setup>
import { useOauthStore } from '@/stores/oauth'
import { useRouter } from 'vue-router'
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { ElAvatar } from 'element-plus'

const store = useOauthStore()
const router = useRouter()
const showMenu = ref(false)
const showLangMenu = ref(false)
const selected = ref('home')
const isScrolled = ref(false)

// i18n setup
const { locale, locales, setLocale } = useI18n()

const fullName = computed(() =>
  store.user?.name || `${store.user?.first_name || ''} ${store.user?.last_name || ''}`.trim()
)
const initials = computed(() => {
  if (!fullName.value) return ''
  return fullName.value.split(' ').map(w => w[0]).join('').toUpperCase()
})

const selectMenu = (key, callback) => {
  selected.value = key
  callback()
}

const goHome = () => router.push('/dss/home')
const goAbout = () => router.push('/dss/about')
const goServices = () => router.push('/dss/services/customer')
const goContact = () => router.push('/dss/contact')
const goOrders = () => router.push('/dss/customer-orders')
const goCreateOrder = () => router.push('/dss/orders/create')
const goProfile = () => { showMenu.value = false; router.push('/dss/profile/client') }
const logout = () => { showMenu.value = false; store.$reset(); router.push('/') }

const handleClickOutside = (e) => { 
  if (!e.target.closest('.profile-wrapper')) showMenu.value = false
  if (!e.target.closest('.language-wrapper')) showLangMenu.value = false
}
const toggleMenu = () => { showMenu.value = !showMenu.value }
const toggleLangMenu = () => { showLangMenu.value = !showLangMenu.value }

const changeLanguage = (lang) => {
  setLocale(lang)
  showLangMenu.value = false
}

const getCurrentLangFlag = computed(() => {
  return locale.value === 'vi' ? '🇻🇳' : '🇺🇸'
})

const getCurrentLangName = computed(() => {
  return locale.value === 'vi' ? 'Tiếng Việt' : 'English'
})

const onScroll = () => {
  isScrolled.value = window.scrollY > 10
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  window.addEventListener('scroll', onScroll)
})
onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
  window.removeEventListener('scroll', onScroll)
})
</script>

<style scoped>
:root { 
  --primary: #3b82f6;
  --secondary: #0d9488; 
  --accent: #059669;
  --text-dark: #1e293b;
  --text-light: #64748b;
  --bg-light: #f8fafc;
  --bg-card: #ffffff;
  --shadow: 0 10px 25px -3px rgba(0, 0, 0, 0.1);
  --shadow-hover: 0 20px 40px -4px rgba(0, 0, 0, 0.15);
  --gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  --clean-gradient: linear-gradient(135deg, #3b82f6 0%, #0d9488 100%);
  --sparkle: #fbbf24;
  --soft-white: #fefefe;
  --soft-gray: #f8fafc;
  --text-muted: #64748b;
  --clean-shadow: 0 4px 20px rgba(59, 130, 246, 0.08);
  --clean-glow: 0 0 20px rgba(59, 130, 246, 0.15);
}

.user-topbar {
  position: sticky; 
  top: 0; 
  z-index: 1000;
  width: 100%; 
  display: flex; 
  justify-content: center;
  background: linear-gradient(to bottom, rgba(255,255,255,0.98), rgba(248,250,252,0.95));
  backdrop-filter: blur(20px) saturate(180%);
  border-bottom: 1px solid rgba(203, 213, 225, 0.3);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: var(--clean-shadow);
}

.user-topbar.scrolled {
  background: rgba(255,255,255,0.85); /* Trong suốt hơn khi scroll */
  backdrop-filter: blur(15px) saturate(160%);
  box-shadow: 0 2px 20px rgba(0, 0, 0, 0.05);
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.user-topbar-wrapper {
  width: 100%; 
  max-width: 1280px;
  padding: 16px 32px;
  display: flex; 
  align-items: center; 
  justify-content: space-between;
  position: relative;
}

/* Logo Design - Clean & Sparkly */
.company-name {
  position: static;
  z-index: 10;
}

.logo {
  position: relative;
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.logo:hover {
  transform: scale(1.05);
  filter: brightness(1.1);
}

.logo-icon {
  font-size: 24px;
  animation: sparkle 2s infinite;
}

.logo-text {
  margin: 0;
  font-size: 28px;
  font-weight: 900;
  background: linear-gradient(135deg, #059669 0%, #047857 50%, #065f46 100%); /* Xanh đậm hơn */
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  letter-spacing: -0.5px;
  text-shadow: 0 2px 4px rgba(5, 150, 105, 0.2);
}

/* Sparkle Animation */
.sparkle {
  position: absolute;
  width: 4px;
  height: 4px;
  background: var(--sparkle);
  border-radius: 50%;
  animation: float 3s infinite;
}

.sparkle-1 { top: -5px; left: 10px; animation-delay: 0s; }
.sparkle-2 { top: 5px; right: -5px; animation-delay: 1s; }
.sparkle-3 { bottom: -5px; left: 50%; animation-delay: 2s; }

@keyframes sparkle {
  0%, 100% { transform: scale(1) rotate(0deg); }
  50% { transform: scale(1.2) rotate(180deg); }
}

@keyframes float {
  0%, 100% { transform: translateY(0px) scale(0.8); opacity: 0.7; }
  50% { transform: translateY(-8px) scale(1.2); opacity: 1; }
}

/* Navigation */
.nav-right { 
  display: flex; 
  align-items: center; 
  gap: 8px;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  font-size: 15px;
  font-weight: 600;
  padding: 12px 16px;
  border-radius: 12px;
  color: var(--text-dark);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.nav-link::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(59, 130, 246, 0.1), transparent);
  transition: left 0.5s;
}

.nav-link:hover::before {
  left: 100%;
}

.nav-link:hover {
  background: rgba(34, 197, 94, 0.1); /* Xanh lá cây nhẹ */
  color: var(--accent);
  transform: translateY(-1px);
  box-shadow: var(--shadow);
  border: 1px solid rgba(34, 197, 94, 0.2);
}

.nav-link.active {
  background: transparent;
  color: #000000; /* Màu đen */
  box-shadow: none;
  position: relative;
}

.nav-link.active::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 50%;
  transform: translateX(-50%);
  width: 60%;
  height: 3px;
  background: var(--accent); /* Gạch chân màu xanh */
  border-radius: 2px;
}

.nav-icon {
  width: 18px;
  height: 18px;
  transition: all 0.3s ease;
}

.nav-link:hover .nav-icon {
  transform: scale(1.1) rotate(5deg);
}

.nav-text {
  white-space: nowrap;
}

.orders-link {
  background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%); /* Xanh lá cây nhẹ */
  border: 1px solid rgba(34, 197, 94, 0.2);
}

/* CTA Button - Special Clean Design */
.cta-btn {
  position: relative;
  display: flex;
  align-items: center;
  cursor: pointer;
  padding: 14px 24px;
  border-radius: 50px;
  background: linear-gradient(135deg, #059669 0%, #047857 100%); /* Xanh đậm hơn */
  color: white;
  font-weight: 700;
  font-size: 15px;
  box-shadow: 0 4px 20px rgba(5, 150, 105, 0.4); /* Shadow đậm hơn */
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
  margin-left: 12px;
  border: 2px solid rgba(5, 150, 105, 0.3); /* Thêm border để nổi bật */
}

.cta-btn::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  transition: all 0.4s ease;
  transform: translate(-50%, -50%);
}

.cta-btn:hover::before {
  width: 300px;
  height: 300px;
}

.cta-btn:hover {
  background: linear-gradient(135deg, #16a34a 0%, #15803d 100%); /* Xanh đậm hơn khi hover */
  transform: translateY(-2px) scale(1.05);
  box-shadow: 0 8px 32px rgba(22, 163, 74, 0.5); /* Shadow xanh đậm */
  border-color: rgba(22, 163, 74, 0.5);
}

.cta-content {
  display: flex;
  align-items: center;
  gap: 8px;
  position: relative;
  z-index: 2;
}

.cta-icon {
  width: 20px;
  height: 20px;
  transition: all 0.3s ease;
}

.cta-btn:hover .cta-icon {
  transform: rotate(90deg) scale(1.1);
}

.cta-shine {
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: linear-gradient(45deg, transparent 40%, rgba(255,255,255,0.3) 50%, transparent 60%);
  transform: translateX(-100%);
  transition: transform 0.8s;
}

.cta-btn:hover .cta-shine {
  transform: translateX(100%);
}

/* Avatar Design */
.profile-wrapper {
  position: relative;
  margin-left: 20px;
}

/* Language Switcher */
.language-wrapper {
  position: relative;
  margin-left: 12px;
}

.language-toggle {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  padding: 10px 16px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.8);
  border: 1px solid rgba(59, 130, 246, 0.1);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  backdrop-filter: blur(10px);
  font-size: 14px;
  font-weight: 500;
  color: var(--text-dark);
  box-shadow: var(--clean-shadow);
}

.language-toggle:hover {
  background: rgba(34, 197, 94, 0.1);
  border-color: rgba(34, 197, 94, 0.3);
  transform: translateY(-1px);
  box-shadow: 0 4px 20px rgba(34, 197, 94, 0.2);
}

.lang-flag {
  font-size: 18px;
  line-height: 1;
  display: flex;
  align-items: center;
}

.lang-text {
  font-weight: 600;
  white-space: nowrap;
}

.lang-arrow {
  width: 16px;
  height: 16px;
  transition: all 0.3s ease;
  color: var(--text-light);
}

.lang-arrow.rotated {
  transform: rotate(180deg);
  color: var(--accent);
}

.language-menu {
  position: absolute;
  top: 50px;
  right: 0;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px) saturate(180%);
  border: 1px solid rgba(59, 130, 246, 0.1);
  border-radius: 16px;
  box-shadow: 0 20px 40px rgba(59, 130, 246, 0.15);
  min-width: 180px;
  z-index: 1000;
  overflow: hidden;
  transform-origin: top right;
}

.language-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 18px;
  cursor: pointer;
  color: var(--text-dark);
  font-size: 14px;
  font-weight: 500;
  transition: all 0.2s ease;
  border-bottom: 1px solid rgba(203, 213, 225, 0.3);
  position: relative;
}

.language-item:last-child {
  border-bottom: none;
}

.language-item:hover {
  background: rgba(34, 197, 94, 0.1);
  color: var(--accent);
  transform: translateX(4px);
}

.language-item.active {
  background: rgba(34, 197, 94, 0.15);
  color: var(--accent);
  font-weight: 600;
}

.language-item .lang-flag {
  font-size: 16px;
}

.check-icon {
  width: 16px;
  height: 16px;
  color: var(--accent);
  margin-left: auto;
}

/* Responsive cho language switcher */
@media (max-width: 768px) {
  .language-wrapper {
    margin-left: 8px;
  }
  
  .language-toggle {
    padding: 8px 12px;
  }
  
  .lang-text {
    display: none;
  }
  
  .lang-arrow {
    width: 14px;
    height: 14px;
  }
}

.avatar-container {
  position: relative;
  cursor: pointer;
  transition: all 0.3s ease;
}

.avatar-container:hover {
  transform: scale(1.1);
  filter: drop-shadow(0 4px 12px rgba(5, 150, 105, 0.3)); /* Thêm drop-shadow xanh */
}

.avatar {
  background: linear-gradient(135deg, #059669 0%, #047857 100%) !important; /* Xanh đậm để nổi bật */
  color: white !important;
  font-weight: 800 !important;
  box-shadow: 0 4px 20px rgba(5, 150, 105, 0.4) !important; /* Shadow đậm hơn */
  border: 3px solid rgba(255, 255, 255, 0.9) !important; /* Border trắng đậm hơn */
  transition: all 0.3s ease !important;
}

.avatar-ring {
  position: absolute;
  top: -3px;
  left: -3px;
  right: -3px;
  bottom: -3px;
  border: 2px solid transparent;
  border-radius: 50%;
  background: linear-gradient(135deg, #059669 0%, #047857 100%); /* Xanh đậm */
  opacity: 0;
  transition: opacity 0.3s ease;
  z-index: -1;
}

.avatar-container:hover .avatar-ring {
  opacity: 0.3;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% { transform: scale(1); opacity: 0.3; }
  50% { transform: scale(1.1); opacity: 0.1; }
  100% { transform: scale(1); opacity: 0.3; }
}

/* Dropdown Menu */
.dropdown-menu {
  position: absolute;
  top: 55px;
  right: 0;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px) saturate(180%);
  border: 1px solid rgba(59, 130, 246, 0.1);
  border-radius: 16px;
  box-shadow: 0 20px 40px rgba(59, 130, 246, 0.15);
  min-width: 220px;
  z-index: 1000;
  overflow: hidden;
  transform-origin: top right;
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 20px;
  cursor: pointer;
  color: var(--text-dark);
  font-size: 15px;
  font-weight: 500;
  transition: all 0.2s ease;
  border-bottom: 1px solid rgba(203, 213, 225, 0.3);
}

.dropdown-item:last-child {
  border-bottom: none;
}

.dropdown-item:hover {
  background: rgba(34, 197, 94, 0.1); /* Xanh lá cây nhẹ */
  color: var(--accent);
  transform: translateX(4px);
}

.dropdown-item.logout:hover {
  background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
  color: #dc2626;
}

.dropdown-icon {
  width: 18px;
  height: 18px;
  transition: all 0.2s ease;
}

.dropdown-item:hover .dropdown-icon {
  transform: scale(1.1);
}

/* Transitions */
.dropdown-enter-active, .dropdown-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.dropdown-enter-from, .dropdown-leave-to {
  opacity: 0;
  transform: scale(0.95) translateY(-10px);
}

.dropdown-enter-to, .dropdown-leave-from {
  opacity: 1;
  transform: scale(1) translateY(0);
}

/* Responsive Design */
@media (max-width: 1024px) {
  .user-topbar-wrapper {
    padding: 12px 24px;
    max-width: 100%;
  }
  
  .logo-text {
    font-size: 24px;
  }
  
  .nav-right {
    gap: 4px;
  }
  
  .nav-link {
    padding: 10px 12px;
    font-size: 14px;
  }
  
  .nav-text {
    display: none;
  }
  
  .nav-icon {
    width: 20px;
    height: 20px;
  }
  
  .cta-btn {
    padding: 12px 20px;
    font-size: 14px;
  }
}

@media (max-width: 768px) {
  .company-name {
    position: static;
    transform: none;
    margin-right: auto;
  }
  
  .logo-text {
    font-size: 20px;
  }
  
  .nav-right {
    gap: 2px;
  }
  
  .nav-link {
    padding: 8px 10px;
  }
  
  .cta-btn {
    padding: 10px 16px;
  }
  
  .cta-btn span {
    display: none;
  }
}

/* Clean Animations */
@keyframes cleanSweep {
  0% { transform: translateX(-100%) rotate(-45deg); }
  100% { transform: translateX(400px) rotate(-45deg); }
}

.user-topbar::after {
  content: '';
  position: absolute;
  top: 0;
  left: -100px;
  width: 100px;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(59, 130, 246, 0.1), transparent);
  transform: skewX(-45deg);
  animation: cleanSweep 8s infinite;
}
</style>