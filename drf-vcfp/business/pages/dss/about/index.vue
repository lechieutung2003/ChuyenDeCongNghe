<script setup lang="ts">
import { useRouter } from 'vue-router';
import { useI18n } from 'vue-i18n';

const router = useRouter();
const { t } = useI18n();

const goToCreateOrder = () => router.push('/dss/orders/create');
const goContact = () => router.push('/dss/contact');
</script>

<template>
  <div class="about-page">

    <!-- HERO với background image như customer.css -->
    <section class="hero-section">
      <div class="hero-background">
        <img src="@/assets/images/bg.png" alt="Background" class="hero-bg-image" />
      </div>
      <div class="hero-overlay"></div>
      
      <div class="hero-content">
        <div class="hero-text">
          <p class="eyebrow">{{ t('about_hero_eyebrow') }}</p>
          <h1 class="title" v-html="t('about_hero_title')"></h1>
          <p class="sub">
            {{ t('about_hero_description') }}
          </p>
          <div class="cta-row">
            <button class="btn" @click="goToCreateOrder">{{ t('about_hero_cta1') }}</button>
            <button class="btn ghost" @click="goContact">{{ t('about_hero_cta2') }}</button>
          </div>

          <!-- Logos/Badges -->
          <ul class="badges">
            <li>{{ t('about_hero_badge1') }}</li>
            <li>{{ t('about_hero_badge2') }}</li>
            <li>{{ t('about_hero_badge3') }}</li>
          </ul>
        </div>
      </div>
    </section>

    <!-- LỊCH SỬ (BE) -->
    <section class="stripe white">
      <div class="container">
        <h2>{{ t('about_history_title') }}</h2>
        <p class="section-subtitle">{{ t('about_history_subtitle') }}</p>

        <div class="timeline-grid">
          <div class="t-item">
            <div class="t-year">19xx</div>
            <div class="t-card">
              <h3>{{ t('about_history_1990_title') }}</h3>
              <p>{{ t('about_history_1990_desc') }}</p>
            </div>
          </div>
          <div class="t-item">
            <div class="t-year">200x</div>
            <div class="t-card">
              <h3>{{ t('about_history_2000_title') }}</h3>
              <p>{{ t('about_history_2000_desc') }}</p>
            </div>
          </div>
          <div class="t-item">
            <div class="t-year">201x</div>
            <div class="t-card">
              <h3>{{ t('about_history_2010_title') }}</h3>
              <p>{{ t('about_history_2010_desc') }}</p>
            </div>
          </div>
          <div class="t-item">
            <div class="t-year">202x</div>
            <div class="t-card">
              <h3>{{ t('about_history_2020_title') }}</h3>
              <p>{{ t('about_history_2020_desc') }}</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- TẦM NHÌN | SỨ MỆNH | GIÁ TRỊ (TRẮNG) -->
    <section class="stripe beige">
      <div class="container vmv">
        <h2>{{ t('about_vmv_title') }}</h2>

        <div class="vmv-grid">
          <div class="card">
            <h3>{{ t('about_vision_title') }}</h3>
            <p>{{ t('about_vision_desc') }}</p>
          </div>
          <div class="card">
            <h3>{{ t('about_mission_title') }}</h3>
            <p>{{ t('about_mission_desc') }}</p>
          </div>
          <div class="card">
            <h3>{{ t('about_values_title') }}</h3>
            <ul class="bullets">
              <li>{{ t('about_values_1') }}</li>
              <li>{{ t('about_values_2') }}</li>
              <li>{{ t('about_values_3') }}</li>
              <li>{{ t('about_values_4') }}</li>
            </ul>
          </div>
        </div>
      </div>
    </section>

    <!-- NĂNG LỰC & SỐ LIỆU (BE) -->
    <section class="stripe white">
      <div class="container stats">
        <h2>{{ t('about_stats_title') }}</h2>
        <p class="section-subtitle">{{ t('about_stats_subtitle') }}</p>

        <div class="stats-grid">
          <div class="s-card">
            <div class="s-num">{{ t('about_stats_projects') }}</div>
            <div class="s-label">{{ t('about_stats_projects_label') }}</div>
          </div>
          <div class="s-card">
            <div class="s-num">{{ t('about_stats_satisfaction') }}</div>
            <div class="s-label">{{ t('about_stats_satisfaction_label') }}</div>
          </div>
          <div class="s-card">
            <div class="s-num">{{ t('about_stats_support') }}</div>
            <div class="s-label">{{ t('about_stats_support_label') }}</div>
          </div>
          <div class="s-card">
            <div class="s-num">{{ t('about_stats_coverage') }}</div>
            <div class="s-label">{{ t('about_stats_coverage_label') }}</div>
          </div>
        </div>
      </div>
    </section>

    <!-- ĐỘI NGŨ LÃNH ĐẠO (TRẮNG) -->
    <section class="stripe beige">
      <div class="container team">
        <h2>{{ t('about_team_title') }}</h2>
        <p class="section-subtitle">{{ t('about_team_subtitle') }}</p>

        <div class="team-grid">
          <div class="member">
            <img src="@/assets/images/a0.png" alt="CEO" />
            <h3>{{ t('about_team_ceo') }}</h3>
            <p class="role">{{ t('about_team_ceo_role') }}</p>
          </div>
          <div class="member">
            <img src="@/assets/images/a0.png" alt="COO" />
            <h3>{{ t('about_team_coo') }}</h3>
            <p class="role">{{ t('about_team_coo_role') }}</p>
          </div>
          <div class="member">
            <img src="@/assets/images/a0.png" alt="QA" />
            <h3>{{ t('about_team_qa') }}</h3>
            <p class="role">{{ t('about_team_qa_role') }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- CHỨNG NHẬN | ĐỐI TÁC (BE) -->
    <section class="stripe white">
      <div class="container certs">
        <h2>{{ t('about_certs_title') }}</h2>
        <div class="certs-row">
          <div class="cert">{{ t('about_cert_iso9001') }}</div>
          <div class="cert">{{ t('about_cert_iso14001') }}</div>
          <div class="cert">{{ t('about_cert_green') }}</div>
          <div class="cert">{{ t('about_cert_trusted') }}</div>
        </div>
      </div>
    </section>

    <!-- CTA CUỐI TRANG (TRẮNG) -->
    <section class="stripe beige">
      <div class="container final-cta">
        <h2>{{ t('about_final_cta_title') }}</h2>
        <p>{{ t('about_final_cta_desc') }}</p>
        <div class="cta-row">
          <button class="btn" @click="goToCreateOrder">{{ t('about_final_cta1') }}</button>
          <button class="btn ghost" @click="goContact">{{ t('about_final_cta2') }}</button>
        </div>
      </div>
    </section>

  </div>
</template>


