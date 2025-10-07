<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import '@/assets/css/customer.css'

const router = useRouter()
const { t } = useI18n()

// Form state
const form = ref({
  fullName: '',
  phone: '',
  email: '',
  service: '',
  message: '',
  agree: true
})
const sending = ref(false)
const sent = ref(false)
const error = ref('')

// Fake submit (thay bằng call API của bạn)
const handleSubmit = async () => {
  error.value = ''
  // validate nhẹ
  if (!form.value.fullName || !form.value.phone || !form.value.message) {
    error.value = t('contact_form_validation_error')
    return
  }
  sending.value = true
  try {
    // TODO: gọi API của bạn ở đây
    await new Promise(r => setTimeout(r, 800))
    sent.value = true
  } catch (e) {
    error.value = t('contact_form_submit_error')
  } finally {
    sending.value = false
  }
}

// Chuyển trang đặt dịch vụ
const goToCreateOrder = () => router.push('/dss/orders/create')
</script>

<template>
  <div class="about-page">
    <!-- HERO (BEIGE) -->
    <section class="stripe beige">
      <div class="container hero">
        <p class="eyebrow">{{ t('contact_eyebrow') }}</p>
        <h1 class="title">{{ t('contact_title') }}</h1>
        <p class="sub" v-html="t('contact_subtitle')">
        </p>
        <div class="cta-row">
          <button class="btn" @click="goToCreateOrder">{{ t('contact_cta_book_service') }}</button>
          <a href="tel:19001234" class="btn ghost">{{ t('contact_cta_hotline') }}</a>
        </div>
        <ul class="badges">
          <li>{{ t('contact_badge_support') }}</li>
          <li>{{ t('contact_badge_pricing') }}</li>
          <li>{{ t('contact_badge_insurance') }}</li>
        </ul>
      </div>
    </section>

    <!-- FORM + THÔNG TIN (TRẮNG) -->
    <section class="stripe white">
      <div class="container">
        <div class="timeline-grid">
          <!-- LEFT: FORM -->
          <div class="t-card">
            <h2>{{ t('contact_form_title') }}</h2>
            <p style="color: var(--text-light); margin-bottom: 1rem;">{{ t('contact_form_subtitle') }}</p>

            <form @submit.prevent="handleSubmit" v-if="!sent">
              <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1rem;">
                <div style="display: flex; flex-direction: column; gap: 0.5rem;">
                  <label style="font-weight: 600; font-size: 14px; color: var(--text-dark);">{{ t('contact_form_fullname') }} <span style="color: #ef4444;">*</span></label>
                  <input v-model="form.fullName" type="text" :placeholder="t('contact_form_placeholder_fullname')" style="border: 1px solid #e5e7eb; border-radius: 8px; padding: 10px 12px; outline: none; font-size: 14px;" />
                </div>
                <div style="display: flex; flex-direction: column; gap: 0.5rem;">
                  <label style="font-weight: 600; font-size: 14px; color: var(--text-dark);">{{ t('contact_form_phone') }} <span style="color: #ef4444;">*</span></label>
                  <input v-model="form.phone" type="tel" :placeholder="t('contact_form_placeholder_phone')" style="border: 1px solid #e5e7eb; border-radius: 8px; padding: 10px 12px; outline: none; font-size: 14px;" />
                </div>
              </div>

              <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1rem;">
                <div style="display: flex; flex-direction: column; gap: 0.5rem;">
                  <label style="font-weight: 600; font-size: 14px; color: var(--text-dark);">{{ t('contact_form_email') }}</label>
                  <input v-model="form.email" type="email" :placeholder="t('contact_form_placeholder_email')" style="border: 1px solid #e5e7eb; border-radius: 8px; padding: 10px 12px; outline: none; font-size: 14px;" />
                </div>
                <div style="display: flex; flex-direction: column; gap: 0.5rem;">
                  <label style="font-weight: 600; font-size: 14px; color: var(--text-dark);">{{ t('contact_form_service_need') }}</label>
                  <select v-model="form.service" style="border: 1px solid #e5e7eb; border-radius: 8px; padding: 10px 12px; outline: none; font-size: 14px;">
                    <option value="">{{ t('contact_form_placeholder_service_select') }}</option>
                    <option value="basic">{{ t('contact_service_basic') }}</option>
                    <option value="deep">{{ t('contact_service_deep') }}</option>
                    <option value="office">{{ t('contact_service_office') }}</option>
                    <option value="post">{{ t('contact_service_post') }}</option>
                  </select>
                </div>
              </div>

              <div style="display: flex; flex-direction: column; gap: 0.5rem; margin-bottom: 1rem;">
                <label style="font-weight: 600; font-size: 14px; color: var(--text-dark);">{{ t('contact_form_message') }} <span style="color: #ef4444;">*</span></label>
                <textarea v-model="form.message" rows="5" :placeholder="t('contact_form_placeholder_message')" style="border: 1px solid #e5e7eb; border-radius: 8px; padding: 10px 12px; outline: none; font-size: 14px; resize: vertical;"></textarea>
              </div>

              <label style="display: flex; gap: 8px; align-items: flex-start; margin: 1rem 0; font-size: 14px; color: var(--text-dark);">
                <input type="checkbox" v-model="form.agree" />
                {{ t('contact_form_agree') }}
              </label>

              <p v-if="error" style="color: #ef4444; font-weight: 600; margin: 0.5rem 0;">{{ error }}</p>

              <button class="btn" style="width: 100%;" :disabled="sending">
                <span v-if="!sending">{{ t('contact_form_submit') }}</span>
                <span v-else>{{ t('contact_form_submitting') }}</span>
              </button>
            </form>

            <div v-else style="text-align: center; padding: 1.5rem;">
              <h3 style="margin: 0 0 0.5rem; font-size: 20px; font-weight: 700; color: var(--accent);">{{ t('contact_success_title') }}</h3>
              <p style="margin-bottom: 1rem; color: var(--text-light);">{{ t('contact_success_message') }}</p>
              <button class="btn" @click="goToCreateOrder">{{ t('contact_success_cta') }}</button>
            </div>
          </div>

          <!-- RIGHT: INFO -->
          <div>
            <div class="t-card" style="margin-bottom: 1rem;">
              <h3 style="margin: 0 0 0.5rem; font-size: 1.25rem; font-weight: 700; color: var(--accent);">{{ t('contact_info_hotline') }}</h3>
              <a href="tel:19001234" style="font-weight: 700; color: var(--text-dark); text-decoration: none;">{{ t('contact_info_hotline_number') }}</a>
              <p style="color: var(--text-light); margin: 0.25rem 0 0;">{{ t('contact_info_hotline_hours') }}</p>
            </div>
            
            <div class="t-card" style="margin-bottom: 1rem;">
              <h3 style="margin: 0 0 0.5rem; font-size: 1.25rem; font-weight: 700; color: var(--accent);">{{ t('contact_info_email') }}</h3>
              <a :href="`mailto:${t('contact_info_email_address')}`" style="font-weight: 700; color: var(--text-dark); text-decoration: none;">{{ t('contact_info_email_address') }}</a>
              <p style="color: var(--text-light); margin: 0.25rem 0 0;">{{ t('contact_info_email_response') }}</p>
            </div>
            
            <div class="t-card" style="margin-bottom: 1rem;">
              <h3 style="margin: 0 0 0.5rem; font-size: 1.25rem; font-weight: 700; color: var(--accent);">{{ t('contact_info_messaging') }}</h3>
              <p style="color: var(--text-dark); font-weight: 600; margin: 0.25rem 0;">{{ t('contact_info_messaging_number') }}</p>
              <p style="color: var(--text-light); margin: 0;">{{ t('contact_info_messaging_desc') }}</p>
            </div>
            
            <div class="t-card" style="margin-bottom: 1rem;">
              <h3 style="margin: 0 0 0.5rem; font-size: 1.25rem; font-weight: 700; color: var(--accent);">{{ t('contact_info_office') }}</h3>
              <p style="color: var(--text-dark); font-weight: 600; margin: 0.25rem 0;">{{ t('contact_info_office_address') }}</p>
              <p style="color: var(--text-light); margin: 0;">{{ t('contact_info_office_branches') }}</p>
            </div>
            
            <div class="t-card" style="background: var(--bg-light);">
              <h3 style="margin: 0 0 0.5rem; font-size: 1.25rem; font-weight: 700; color: var(--accent);">{{ t('contact_info_hours') }}</h3>
              <div style="margin-top: 0.5rem;">
                <div style="display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px dashed #e5e5e5;">
                  <span style="color: var(--text-dark); font-weight: 500;">{{ t('contact_info_weekdays') }}</span>
                  <span style="color: var(--text-dark); font-weight: 600;">{{ t('contact_info_weekdays_hours') }}</span>
                </div>
                <div style="display: flex; justify-content: space-between; padding: 0.5rem 0;">
                  <span style="color: var(--text-dark); font-weight: 500;">{{ t('contact_info_weekend') }}</span>
                  <span style="color: var(--text-dark); font-weight: 600;">{{ t('contact_info_weekend_hours') }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>    <!-- BẢN ĐỒ (BEIGE) -->
    <section class="stripe beige">
      <div class="container">
        <div style="text-align: center; margin-bottom: 2rem;">
          <h2 class="section-title">{{ t('contact_map_title') }}</h2>
          <p class="section-subtitle">{{ t('contact_map_subtitle') }}</p>
        </div>
        <!-- Thay src bằng Google Maps của bạn -->
        <div style="border-radius: 24px; overflow: hidden; box-shadow: var(--shadow);">
          <iframe
            title="Google Map"
            src="https://maps.google.com/maps?q=Ben%20Thanh%20Market&t=&z=13&ie=UTF8&iwloc=&output=embed"
            loading="lazy"
            referrerpolicy="no-referrer-when-downgrade"
            style="width: 100%; height: 400px; border: 0; display: block;"
          ></iframe>
        </div>
      </div>
    </section>

    <!-- CÂU HỎI THƯỜNG GẶP (TRẮNG) -->
    <section class="stripe white">
      <div class="container">
        <div style="text-align: center; margin-bottom: 2rem;">
          <h2 class="section-title">{{ t('contact_faq_title') }}</h2>
        </div>
        <div class="vmv-grid">
          <div class="vmv">
            <div class="card">
              <h3>{{ t('contact_faq_q1') }}</h3>
              <p>{{ t('contact_faq_a1') }}</p>
            </div>
          </div>
          <div class="vmv">
            <div class="card">
              <h3>{{ t('contact_faq_q2') }}</h3>
              <p>{{ t('contact_faq_a2') }}</p>
            </div>
          </div>
          <div class="vmv">
            <div class="card">
              <h3>{{ t('contact_faq_q3') }}</h3>
              <p>{{ t('contact_faq_a3') }}</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>
