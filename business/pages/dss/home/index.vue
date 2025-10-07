<script setup lang="ts">
import { useOauthStore } from '@/stores/oauth';
import { useRouter } from 'vue-router';
import { useI18n } from 'vue-i18n';
import '@/assets/css/customer.css'

const store = useOauthStore();
const router = useRouter();
const { t } = useI18n();

const goToCreateOrder = () => {
  router.push('/dss/orders/create');
};
</script>

<template>
  <div class="home-page">
    <!-- Hero Section with Background -->
    <section class="hero-section">
      <div class="hero-background">
        <div class="hero-overlay"></div>
        <img src="@/assets/images/a0.png" alt="Clean Home" class="hero-bg-image" />
      </div>
      
      <div class="hero-content">
        <div class="hero-text">
          <h1 class="hero-title">{{ t('home_hero_title') }}</h1>
          <h2 class="hero-subtitle">{{ t('home_hero_subtitle') }}</h2>
          <p class="hero-description">
            {{ t('home_hero_description') }}
          </p>
          
          <button class="hero-cta" @click="goToCreateOrder">
            <svg class="cta-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              <path d="M9 12l2 2 4-4"></path>
            </svg>
            {{ t('home_hero_cta') }}
          </button>
        </div>
        
        <!-- Service Quick Access Cards -->
        <div class="quick-services">

          <div class="service-card" @click="goToCreateOrder">
            <div class="service-image">
              <img src="@/assets/images/regular.jpg" alt="Vệ sinh văn phòng" />
            </div>
            <div class="service-info">
              <h4>{{ t('home_service_basic') }}</h4>
              <p>{{ t('home_service_basic_desc') }}</p>
            </div>
          </div>
          
          <div class="service-card" @click="goToCreateOrder">
            <div class="service-image">
              <img src="@/assets/images/deep.jpg" alt="Vệ sinh văn phòng" />
            </div>
            <div class="service-info">
              <h4>{{ t('home_service_advanced') }}</h4>
              <p>{{ t('home_service_advanced_desc') }}</p>
            </div>
          </div>
          
          
          <div class="service-card" @click="goToCreateOrder">
            <div class="service-image">
              <img src="@/assets/images/clock.jpg" alt="Dọn theo giờ" />
            </div>
            <div class="service-info">
              <h4>{{ t('home_service_hourly') }}</h4>
              <p>{{ t('home_service_hourly_desc') }}</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Hot Services Section -->
    <section class="hot-services">
      <div class="container">
        <h2 class="section-title">{{ t('home_hot_services_title') }}</h2>
        <p class="section-subtitle">
          {{ t('home_hot_services_subtitle') }}
        </p>
        
        <div class="services-grid">
          <div class="service-tile large" @click="goToCreateOrder">
            <div class="service-bg">
              <img src="@/assets/images/all.jpg" alt="Dọn dẹp tổng thể" />
            </div>
            <div class="service-overlay">
              <span class="service-tag">{{ t('home_service_top_tag') }}</span>
              <div class="service-content">
                <h3>{{ t('home_service_comprehensive') }}</h3>
                <p>{{ t('home_service_comprehensive_price') }}</p>
              </div>
            </div>
          </div>
          
          <div class="service-tile" @click="goToCreateOrder">
            <div class="service-bg">
              <img src="@/assets/images/glass.jpeg" alt="Vệ sinh kính" />
            </div>
            <div class="service-overlay">
              <div class="service-content">
                <h3>{{ t('home_service_glass') }}</h3>
                <p>{{ t('home_service_glass_price') }}</p>
              </div>
            </div>
          </div>
          
          <div class="service-tile" @click="goToCreateOrder">
            <div class="service-bg">
              <img src="@/assets/images/construct.jpeg" alt="Dọn sau xây dựng" />
            </div>
            <div class="service-overlay">
              <div class="service-content">
                <h3>{{ t('home_service_construction') }}</h3>
                <p>{{ t('home_service_construction_price') }}</p>
              </div>
            </div>
          </div>
          
          <div class="service-tile" @click="goToCreateOrder">
            <div class="service-bg">
              <img src="@/assets/images/carpet.jpeg" alt="Vệ sinh thảm" />
            </div>
            <div class="service-overlay">
              <div class="service-content">
                <h3>{{ t('home_service_carpet') }}</h3>
                <p>{{ t('home_service_carpet_price') }}</p>
              </div>
            </div>
          </div>
        </div>
        
        <div class="navigation-dots">
          <button class="nav-dot"></button>
          <button class="nav-dot active"></button>
        </div>
      </div>
    </section>

    <!-- Featured Section -->
    <section class="featured-section">
      <div class="container">
        <div class="featured-card">
          <div class="featured-image">
            <img src="@/assets/images/luxury.jpg" alt="Dịch vụ cao cấp" />
            <div class="featured-badge">{{ t('home_featured_badge') }}</div>
          </div>
          <div class="featured-content">
            <h2>{{ t('home_featured_title') }}</h2>
            <p>{{ t('home_featured_description') }}</p>
            <div class="featured-tags">
              <span class="tag">{{ t('home_featured_tag1') }}</span>
              <span class="tag">{{ t('home_featured_tag2') }}</span>
            </div>
            <button class="hero-cta1" @click="goToCreateOrder">
              {{ t('home_featured_cta') }}
              <svg class="arrow-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M7 17l10-10M7 7h10v10"/>
              </svg>
            </button>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>
