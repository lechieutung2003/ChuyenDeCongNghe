<template>
  <div class="about-page">
    <section class="stripe white">
      <div class="container">
        <div class="content-header">
          <div class="header-top">
            <div class="header-info">
              <h1 class="section-title">{{ t('edit_order_title') }}</h1>
              <p class="section-subtitle">{{ t('edit_order_subtitle') }}</p>
            </div>
            
            <div class="header-actions">
              <button 
                type="button" 
                @click="showCancelModal = true" 
                class="btn-cancel-order"
                v-if="order && order.status === 'pending'"
              >
                <span class="icon">🚫</span>
                {{ t('cancel_order_button') }}
              </button>
            </div>

          </div>
          
          <!-- Customer info display -->
          <div v-if="loading" class="customer-info loading">
            <p>{{ t('edit_order_loading') }}</p>
          </div>
          <div v-else-if="customerInfo.customer_name" class="customer-info">
            <h3>{{ t('create_order_customer_info') }}</h3>
            <div class="customer-details">
              <div class="customer-item">
                <span class="label">{{ t('create_order_customer_name') }}</span>
                <span class="value">{{ customerInfo.customer_name || 'N/A' }}</span>
              </div>
              <div class="customer-item">
                <span class="label">{{ t('create_order_customer_email') }}</span>
                <span class="value">{{ customerInfo.email || 'N/A' }}</span>
              </div>
              <div class="customer-item" v-if="customerInfo.phone">
                <span class="label">{{ t('create_order_customer_phone') }}</span>
                <span class="value">{{ customerInfo.phone }}</span>
              </div>
              <div class="customer-item" v-if="customerInfo.address">
                <span class="label">{{ t('create_order_customer_address') }}</span>
                <span class="value">{{ customerInfo.address }}</span>
              </div>
            </div>
          </div>
        </div>

        <div v-if="error" class="error-state">
          <div class="error-message">{{ error }}</div>
          <RouterLink to="/dss/customer-orders" class="back-btn">{{ t('back') }}</RouterLink>
        </div>

        <form v-else-if="order" class="order-form" @submit.prevent="saveOrder">
          <div class="form-grid">
            <div class="form-column">
              <!-- Service Selection -->
              <div class="form-group">
                <label>{{ t('create_order_service') }} <span class="required">*</span></label>
                <div class="input-wrapper">
                  <select v-model="formData.service_type" @change="handleServiceChange" class="form-input" required>
                    <option value="">{{ t('create_order_service_placeholder') }}</option>
                    <option v-for="service in services" :key="service.id" :value="service.id">
                      {{ service.name }} - {{ formatPrice(service.price_per_m2) }}/m²
                    </option>
                  </select>
                </div>
              </div>

              <!-- Area -->
              <div class="form-group">
                <label>{{ t('create_order_area') }} <span class="required">*</span></label>
                <div class="input-wrapper">
                  <input 
                    type="number" 
                    v-model="formData.area_m2" 
                    :placeholder="t('create_order_area_placeholder')"
                    @input="handleAreaChange"
                    min="1"
                    step="0.01"
                    class="form-input"
                    required
                  />
                </div>
              </div>

              <!-- Note -->
              <div class="form-group">
                <label>{{ t('create_order_note') }}</label>
                <div class="input-wrapper">
                  <textarea 
                    v-model="formData.note" 
                    :placeholder="t('create_order_note_placeholder')"
                    class="form-input"
                    rows="3"
                  ></textarea>
                </div>
              </div>
            </div>
            
            <div class="form-column">
              <!-- Start Time -->
              <div class="form-group">
                <label>{{ t('create_order_start_time') }} <span class="required">*</span></label>
                <div class="input-wrapper">
                  <input 
                    type="datetime-local" 
                    v-model="formData.preferred_start_time"
                    @change="handleTimeChange"
                    class="form-input"
                    required
                  />
                </div>
              </div>

              <!-- End Time -->
              <div class="form-group">
                <label>{{ t('create_order_end_time') }} <span class="required">*</span></label>
                <div class="input-wrapper">
                  <input 
                    type="datetime-local" 
                    v-model="formData.preferred_end_time"
                    @change="handleTimeChange"
                    class="form-input"
                    required
                  />
                </div>
              </div>

              <!-- Price per m2 Display -->
              <div class="form-group" v-if="selectedServicePrice">
                <label>{{ t('create_order_price_per_m2') }}</label>
                <div class="input-wrapper">
                  <input 
                    type="text" 
                    :value="formatPrice(selectedServicePrice)" 
                    class="form-input price-display"
                    readonly
                  />
                </div>
              </div>
            </div>
          </div>

          <!-- Calculation section -->
          <div class="calculation-section">
            <h3 class="calculation-title">{{ t('create_order_calculation_title') }}</h3>
            <div class="notice">{{ t('edit_order_calculation_notice') }}</div>
            
            <div class="calculation-grid">
              <div class="form-group">
                <label>{{ t('create_order_estimated_hours') }}</label>
                <div class="input-wrapper">
                  <input 
                    type="text" 
                    :value="formatTime(formData.estimated_hours)" 
                    :placeholder="t('create_order_estimated_hours_placeholder')"
                    class="form-input estimated-display"
                    readonly
                  />
                </div>
              </div>

              <div class="form-group">
                <label>{{ t('create_order_requested_hours') }}</label>
                <div class="input-wrapper">
                  <input 
                    type="text" 
                    :value="formatTime(formData.requested_hours)" 
                    :placeholder="t('create_order_requested_hours_placeholder')"
                    class="form-input requested-display"
                    readonly
                  />
                </div>
              </div>

              <div class="form-group">
                <label>{{ t('create_order_estimated_price') }}</label>
                <div class="input-wrapper">
                  <input 
                    type="text" 
                    :value="formatPrice(formData.cost_confirm)" 
                    :placeholder="t('create_order_estimated_price_placeholder')"
                    class="form-input price-estimated"
                    readonly
                  />
                </div>
              </div>

              <!-- Service details and price explanation -->
              <div class="form-group" v-if="selectedService">
                <label>{{ t('create_order_productivity') }}</label>
                <div class="form-hint success">
                  {{ t('create_order_productivity', { productivity: selectedService.productivity_rate }) }}
                </div>
                <div class="form-hint">
                  {{ t('create_order_min_time', { time: formatTime(selectedService.min_time_hours) }) }}
                </div>
              </div>
            </div>

            <!-- Price explanation -->
            <div v-if="priceExplanation" class="price-explanation">
              <div class="explanation-text" v-html="priceExplanation.replace(/\n/g, '<br>')"></div>
            </div>

            <!-- Time validation -->
            <div v-if="timeValidationMessage" class="error-message">
              {{ timeValidationMessage }}
            </div>
          </div>
          
          <!-- Action buttons -->
          <div class="form-actions">
            <button type="button" @click="cancelEdit" class="btn-close">
              {{ t('edit_order_cancel_button') }}
            </button>
            <button type="submit" :disabled="saving || !isTimeValid" class="featured-cta">
              {{ saving ? t('edit_order_saving') : (!isTimeValid ? t('create_order_time_invalid') : t('edit_order_save_button')) }}
            </button>
          </div>
        </form>
      </div>
    </section>

    <!-- Toast Notification -->
    <div v-if="showToast" :class="['toast-notification', toastType]">
      {{ toastMessage }}
    </div>

    <!-- Cancel Order Modal -->
    <div v-if="showCancelModal" class="modal-overlay" @click="closeCancelModal">
      <div class="modal-content cancel-modal" @click.stop>
        <div class="modal-header">
          <h2>{{ t('cancel_order_title') }}</h2>
          <button class="close-btn" @click="closeCancelModal">×</button>
        </div>
        
        <div class="modal-body">
          <div class="cancel-info">
            <div class="warning-icon">⚠️</div>
            <h3>{{ t('cancel_order_warning') }}</h3>
            <p>{{ t('cancel_order_description') }}</p>
          </div>

          <div class="admin-contact">
            <h4>{{ t('cancel_order_contact_admin') }}</h4>
            <div class="contact-item">
              <span class="contact-label">{{ t('cancel_order_phone') }}</span>
              <div class="contact-value">
                <span class="phone-number">0123-456-789</span>
                <button 
                  type="button" 
                  @click="copyPhoneNumber" 
                  class="copy-btn"
                  :title="t('copy_phone')"
                >
                  📋
                </button>
              </div>
            </div>
            <div class="contact-item">
              <span class="contact-label">{{ t('cancel_order_email') }}</span>
              <div class="contact-value">
                <span class="email-address">admin@dss-cleaning.com</span>
                <button 
                  type="button" 
                  @click="copyEmail" 
                  class="copy-btn"
                  :title="t('copy_email')"
                >
                  📋
                </button>
              </div>
            </div>
          </div>

          <div class="cancel-note">
            <p><strong>{{ t('cancel_order_note_title') }}</strong></p>
            <ul>
              <li>{{ t('cancel_order_note_1') }}</li>
              <li>{{ t('cancel_order_note_2') }}</li>
              <li>{{ t('cancel_order_note_3') }}</li>
            </ul>
          </div>
        </div>

        <div class="modal-footer">
          <button class="btn-close" @click="closeCancelModal">
            {{ t('cancel_order_close') }}
          </button>
          <a 
            href="tel:0123456789" 
            class="btn-call"
          >
            📞 {{ t('cancel_order_call_now') }}
          </a>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import CustomerOrderService from '@/services/dss/users/customer'
import ServiceTypeService from '@/services/dss/order-serviceType'
import '@/assets/css/customer.css'

// Apply role-based middleware
definePageMeta({
  middleware: 'role-based'
})

const { t } = useI18n()
const route = useRoute()
const router = useRouter()

const orderId = route.params.id
const loading = ref(true)
const saving = ref(false)
const error = ref('')
const order = ref(null)
const customerInfo = ref({})
const services = ref([])

// Form data
const formData = ref({
  service_type: '',
  area_m2: '',
  preferred_start_time: '',
  preferred_end_time: '',
  note: '',
  requested_hours: 0,
  estimated_hours: 0,
  cost_confirm: 0
})

// Calculation variables similar to create page
const productivity = ref(null)
const estimatedPrice = ref(null)
const priceExplanation = ref('')
const minRequiredHours = ref(null)
const isTimeValid = ref(true)
const timeValidationMessage = ref('')

// Toast notification
const showToast = ref(false)
const toastMessage = ref('')
const toastType = ref('success')

// Cancel order modal
const showCancelModal = ref(false)

// Computed properties similar to create page
const selectedService = computed(() => {
  return services.value.find(s => s.id === formData.value.service_type)
})

const selectedServicePrice = computed(() => {
  if (!formData.value.service_type) return null
  
  const service = services.value.find(s => s.id === formData.value.service_type)
  if (!service) return null
  
  if (service.price_per_m2) {
    return Number(service.price_per_m2)
  } else if (service.name?.toLowerCase().includes('deep cleaning')) {
    return 3000
  } else if (service.name?.toLowerCase().includes('regular cleaning')) {
    return 155000
  }
  
  return null
})

// Calculation functions similar to create page
const calcProductivity = () => {
  const serviceId = formData.value.service_type
  if (!serviceId) {
    productivity.value = null
    return
  }
  const service = services.value.find(s => s.id === serviceId)
  if (service) {
    if (service.cleaning_rate_m2_per_h) {
      productivity.value = Number(service.cleaning_rate_m2_per_h)
    } else if (service.name?.toLowerCase().includes('regular cleaning')) {
      productivity.value = 40
    } else if (service.name?.toLowerCase().includes('deep cleaning')) {
      productivity.value = 35
    } else {
      productivity.value = null
    }
  } else {
    productivity.value = null
  }
}

const calcEstimatedHours = () => {
  const area = formData.value.area_m2
  if (!area || !productivity.value || productivity.value <= 0) {
    formData.value.estimated_hours = null
    minRequiredHours.value = null
    return
  }
  formData.value.estimated_hours = +(area / productivity.value).toFixed(2)
  // Tính thời gian tối thiểu = 60% thời gian ước tính
  minRequiredHours.value = +(formData.value.estimated_hours * 0.6).toFixed(2)
}

const validateRequestedTime = () => {
  const requested = formData.value.requested_hours
  const minRequired = minRequiredHours.value
  const estimated = formData.value.estimated_hours
  
  if (!requested || !minRequired || !estimated) {
    isTimeValid.value = true
    timeValidationMessage.value = ''
    return
  }
  
  if (requested < minRequired) {
    isTimeValid.value = false
    timeValidationMessage.value = t('create_order_validation_error', { 
      message: `${t('create_order_min_time', { time: formatTime(minRequired) })} (60% của ${formatTime(estimated)})` 
    })
  } else {
    isTimeValid.value = true
    timeValidationMessage.value = ''
  }
}

const calcRequestedHours = () => {
  const start = formData.value.preferred_start_time
  const end = formData.value.preferred_end_time
  if (!start || !end) {
    formData.value.requested_hours = null
    return
  }
  const startDate = new Date(start)
  const endDate = new Date(end)
  const diffMs = endDate.getTime() - startDate.getTime()
  if (diffMs > 0) {
    formData.value.requested_hours = +(diffMs / (1000 * 60 * 60)).toFixed(2)
  } else {
    formData.value.requested_hours = null
  }
}

const calcEstimatedPrice = () => {
  const serviceId = formData.value.service_type
  const area = formData.value.area_m2
  if (!serviceId || !area || area <= 0) {
    estimatedPrice.value = null
    formData.value.cost_confirm = null
    priceExplanation.value = ''
    return
  }
  
  let pricePerM2 = 0
  const service = services.value.find(s => s.id === serviceId)
  if (service) {
    if (service.price_per_m2) {
      pricePerM2 = Number(service.price_per_m2)
    } else if (service.name?.toLowerCase().includes('deep cleaning')) {
      pricePerM2 = 3000
    } else if (service.name?.toLowerCase().includes('regular cleaning')) {
      pricePerM2 = 155000
    }
  }

  let basePrice = pricePerM2 > 0 ? pricePerM2 * area : null
  let explanation = `Giá cơ bản: ${pricePerM2.toLocaleString('vi-VN')} x ${area} m² = ${(basePrice || 0).toLocaleString('vi-VN')} VNĐ`

  const requested = formData.value.requested_hours
  const estimated = formData.value.estimated_hours
  if (basePrice && requested && estimated && requested < estimated) {
    const diff = estimated - requested
    let factor = 1
    if (diff > 0.1 && diff <= 1) factor = 1.2
    else if (diff > 1 && diff <= 2) factor = 1.3
    else if (diff > 2) factor = 1.5

    if (factor > 1) {
      explanation += ` (áp dụng hệ số ${factor} do số giờ yêu cầu < số giờ ước tính)`
      basePrice = basePrice * factor
    }
  }

  // Thêm 10% VAT vào giá cuối cùng
  if (basePrice) {
    const vatAmount = Math.round(basePrice * 0.1)
    const finalPrice = basePrice + vatAmount
    explanation += `\nGiá gốc: ${basePrice.toLocaleString('vi-VN')} VNĐ + VAT 10% (${vatAmount.toLocaleString('vi-VN')} VNĐ) = ${finalPrice.toLocaleString('vi-VN')} VNĐ`
    estimatedPrice.value = finalPrice
    formData.value.cost_confirm = finalPrice
  } else {
    estimatedPrice.value = null
    formData.value.cost_confirm = null
  }

  priceExplanation.value = explanation
}

// Watch for changes similar to create page
watch(() => [formData.value.service_type], calcProductivity)
watch(() => [formData.value.area_m2, productivity.value], calcEstimatedHours)
watch(() => [formData.value.preferred_start_time, formData.value.preferred_end_time], () => {
  calcRequestedHours()
  validateRequestedTime()
})
watch(() => [formData.value.service_type, formData.value.area_m2, formData.value.requested_hours, formData.value.estimated_hours], calcEstimatedPrice)
watch(() => [formData.value.requested_hours, minRequiredHours.value], validateRequestedTime)

// Load customer info (similar to create page)
const loadCustomerInfo = async () => {
  try {
    console.log('Loading customer info...')
    
    const response = await CustomerOrderService.getUser()
    console.log('Customer API response:', response)
    
    const customer = response.data || response
    customerInfo.value = {
      customer_name: customer.name || customer.customer_name,
      email: customer.email,
      phone: customer.phone,
      address: customer.address
    }
    
    console.log('Customer info loaded:', customerInfo.value)
    
  } catch (error) {
    console.error('Error loading customer info:', error)
    showToastMessage('Không thể tải thông tin khách hàng', 'error')
  }
}

// Load order data
const loadOrder = async () => {
  try {
    loading.value = true
    error.value = ''
    
    const orderResponse = await CustomerOrderService.getOrder(orderId)
    console.log('Order response:', orderResponse)
    
    order.value = orderResponse
    
    // Check if order can be edited (only pending status)
    if (order.value.status !== 'pending') {
      error.value = 'Chỉ có thể chỉnh sửa đơn hàng ở trạng thái "Chờ xác nhận"'
      return
    }
    
    // Set form data
    formData.value = {
      service_type: order.value.service_type,
      area_m2: parseFloat(order.value.area_m2),
      preferred_start_time: formatDateTimeForInput(order.value.preferred_start_time),
      preferred_end_time: formatDateTimeForInput(order.value.preferred_end_time),
      note: order.value.note || '',
      requested_hours: parseFloat(order.value.requested_hours),
      estimated_hours: parseFloat(order.value.estimated_hours),
      cost_confirm: parseInt(order.value.cost_confirm)
    }
    
  } catch (e) {
    console.error('Error loading order:', e)
    error.value = 'Không thể tải thông tin đơn hàng: ' + e.message
  } finally {
    loading.value = false
  }
}

// Load services data
const loadServices = async () => {
  try {
    const response = await ServiceTypeService.getServiceTypes()
    console.log('Services response:', response)
    
    // Handle response format
    let servicesData = []
    if (Array.isArray(response)) {
      servicesData = response
    } else if (response.results && Array.isArray(response.results)) {
      servicesData = response.results
    } else if (response.data && Array.isArray(response.data)) {
      servicesData = response.data
    } else {
      console.warn('Unexpected services response format:', response)
      servicesData = []
    }
    
    services.value = servicesData.map(service => ({
      id: service.id,
      name: service.name,
      price_per_m2: service.price_per_m2,
      productivity_rate: service.cleaning_rate_m2_per_h || 50,
      min_time_hours: service.min_time_hours || 2
    }))
    
  } catch (e) {
    console.error('Error loading services:', e)
    // Fallback to mock data if API fails
    services.value = [
      {
        id: 'ce1d971a-dd5f-444c-804b-72709998bcf2',
        name: 'Dọn dẹp cơ bản',
        price_per_m2: 50000,
        productivity_rate: 50,
        min_time_hours: 2
      }
    ]
  }
}

// Handle service change
const handleServiceChange = () => {
  if (selectedService.value) {
    calcProductivity()
    calcEstimatedHours()
    calcEstimatedPrice()
  }
}

// Handle area change
const handleAreaChange = () => {
  calcEstimatedHours()
  calcEstimatedPrice()
}

// Handle time change
const handleTimeChange = () => {
  // Validate time range
  if (formData.value.preferred_start_time && formData.value.preferred_end_time) {
    const startTime = new Date(formData.value.preferred_start_time)
    const endTime = new Date(formData.value.preferred_end_time)
    
    if (endTime <= startTime) {
      showToastMessage('Thời gian kết thúc phải sau thời gian bắt đầu', 'error')
      return
    }
  }
  
  calcRequestedHours()
  validateRequestedTime()
  calcEstimatedPrice()
}

// Save order
const saveOrder = async () => {
  try {
    // Validate required fields
    if (!formData.value.service_type) {
      showToastMessage('Vui lòng chọn dịch vụ', 'error')
      return
    }
    
    if (!formData.value.area_m2 || formData.value.area_m2 <= 0) {
      showToastMessage('Vui lòng nhập diện tích hợp lệ', 'error')
      return
    }
    
    if (!formData.value.preferred_start_time || !formData.value.preferred_end_time) {
      showToastMessage('Vui lòng chọn thời gian bắt đầu và kết thúc', 'error')
      return
    }
    
    if (!isTimeValid.value) {
      showToastMessage(timeValidationMessage.value, 'error')
      return
    }
    
    // Validate time range
    const startTime = new Date(formData.value.preferred_start_time)
    const endTime = new Date(formData.value.preferred_end_time)
    
    if (endTime <= startTime) {
      showToastMessage('Thời gian kết thúc phải sau thời gian bắt đầu', 'error')
      return
    }
    
    // Confirm before saving
    if (!confirm('Bạn có chắc muốn lưu thay đổi? Giá và thời gian sẽ được tính lại.')) {
      return
    }
    
    saving.value = true
    
    const updateData = {
      service_type: formData.value.service_type,
      area_m2: formData.value.area_m2.toString(),
      preferred_start_time: new Date(formData.value.preferred_start_time).toISOString(),
      preferred_end_time: new Date(formData.value.preferred_end_time).toISOString(),
      note: formData.value.note,
      requested_hours: formData.value.requested_hours.toString(),
      estimated_hours: formData.value.estimated_hours.toString(),
      cost_confirm: formData.value.cost_confirm.toString()
    }
    
    console.log('Update data being sent:', updateData)
    
    await CustomerOrderService.updateOrder(orderId, updateData)
    
    showToastMessage(t('edit_order_success'), 'success')
    
    // Redirect back to orders list after 2 seconds
    setTimeout(() => {
      router.push('/dss/customer-orders')
    }, 2000)
    
  } catch (e) {
    console.error('Error saving order:', e)
    showToastMessage(t('edit_order_error'), 'error')
  } finally {
    saving.value = false
  }
}

// Cancel edit
const cancelEdit = () => {
  if (confirm(t('edit_order_confirm_cancel'))) {
    router.push('/dss/customer-orders')
  }
}

// Cancel order modal functions
const closeCancelModal = () => {
  showCancelModal.value = false
}

const copyPhoneNumber = async () => {
  try {
    await navigator.clipboard.writeText('0123456789')
    showToastMessage(t('copy_phone_success'), 'success')
  } catch (error) {
    console.error('Failed to copy phone number:', error)
    showToastMessage(t('copy_phone_error'), 'error')
  }
}

const copyEmail = async () => {
  try {
    await navigator.clipboard.writeText('admin@dss-cleaning.com')
    showToastMessage(t('copy_email_success'), 'success')
  } catch (error) {
    console.error('Failed to copy email:', error)
    showToastMessage(t('copy_email_error'), 'error')
  }
}

// Utility functions similar to create page
const formatPrice = (price) => {
  if (!price) return '0 VNĐ'
  return new Intl.NumberFormat('vi-VN', {
    style: 'currency',
    currency: 'VND'
  }).format(price)
}

const formatTime = (hours) => {
  if (!hours || isNaN(hours)) return ''
  if (hours > 0 && hours * 60 < 1) return t('create_order_time_one_minute')
  const h = Math.floor(hours)
  let m = Math.round((hours - h) * 60)
  if (h === 0) return t('create_order_time_minutes', { minutes: m })
  if (m === 0) return t('create_order_time_hours', { hours: h })
  return t('create_order_time_hours_minutes', { hours: h, minutes: m })
}

const formatDateTimeForInput = (datetime) => {
  if (!datetime) return ''
  const date = new Date(datetime)
  return date.toISOString().slice(0, 16) // Format: YYYY-MM-DDTHH:mm
}

// Show toast message
const showToastMessage = (message, type = 'success') => {
  toastMessage.value = message
  toastType.value = type
  showToast.value = true
  
  setTimeout(() => {
    showToast.value = false
  }, 3000)
}

onMounted(() => {
  loadServices()
  loadCustomerInfo()
  loadOrder()
})
</script>

<style scoped>
/* Customer info styles - similar to create page */
.customer-info {
  background: var(--bg-card);
  border: 1px solid rgba(59, 130, 246, 0.1);
  border-radius: 20px;
  padding: 1.5rem;
  margin: 2rem 0;
  box-shadow: var(--shadow);
}

/* Header styles */
.header-top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.header-info {
  flex: 1;
}

.header-actions {
  margin-left: 2rem;
}

.btn-cancel-order {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 12px 20px;
  background: #dc3545;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 4px rgba(220, 53, 69, 0.2);
}

.btn-cancel-order:hover {
  background: #c82333;
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(220, 53, 69, 0.3);
}

.btn-cancel-order .icon {
  font-size: 16px;
}

.customer-info.loading {
  text-align: center;
  color: var(--text-light);
}

.customer-info h3 {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--accent);
  margin: 0 0 1rem;
  text-align: center;
}

.customer-details {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.customer-item {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.customer-item .label {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-light);
  min-width: 60px;
}

.customer-item .value {
  font-size: 0.875rem;
  color: var(--text-dark);
  font-weight: 500;
}

/* Form styles - similar to create page */
.order-form {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
}

.form-column {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: var(--text-dark);
}

.required {
  color: #ef4444;
}

.input-wrapper {
  border: 1.5px solid #ecedec;
  border-radius: 10px;
  min-height: 50px;
  display: flex;
  align-items: center;
  padding: 0 1rem;
  transition: all 0.2s ease-in-out;
  background: var(--bg-card);
}

.input-wrapper:focus-within {
  border-color: var(--primary);
}

.input-wrapper.error {
  border-color: #ef4444;
  background-color: #fef2f2;
}

.form-input {
  border: none;
  width: 100%;
  height: 100%;
  background: transparent;
  color: var(--text-dark);
  font-size: 1rem;
  resize: vertical;
  min-height: inherit;
}

.form-input:focus {
  outline: none;
}

.form-input:disabled {
  color: var(--text-light);
  cursor: not-allowed;
}

.form-input.price-display {
  color: var(--primary);
  font-weight: 600;
}

.form-input.estimated-display {
  color: var(--accent);
  font-weight: 700;
}

.form-input.requested-display {
  color: #ef4444;
  font-weight: 700;
}

.form-input.price-estimated {
  color: #ef4444;
  font-weight: 700;
}

.form-hint {
  color: var(--text-light);
  font-style: italic;
  margin-top: 0.25rem;
  display: block;
  font-size: 0.75rem;
}

.form-hint.success {
  color: var(--accent);
}

.error-message {
  color: #ef4444;
  font-size: 0.813rem;
  font-weight: 500;
  margin-top: 0.25rem;
  padding: 0.5rem 0.75rem;
  background-color: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 8px;
}

/* Calculation section - similar to create page */
.calculation-section {
  background: var(--bg-light);
  border-radius: 16px;
  padding: 1.5rem;
  border: 1px solid rgba(59, 130, 246, 0.1);
}

.calculation-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--text-dark);
  margin: 0 0 1.5rem;
  text-align: center;
}

.notice {
  background: #e3f2fd;
  padding: 10px;
  border-radius: 8px;
  margin-bottom: 20px;
  color: #1976d2;
  font-size: 14px;
  text-align: center;
}

.calculation-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
}

/* Price explanation */
.price-explanation {
  background: #fff9c4;
  padding: 1rem;
  border-radius: 8px;
  margin-top: 1rem;
  border: 1px solid #fde047;
}

.explanation-text {
  color: #92400e;
  font-size: 0.875rem;
  line-height: 1.5;
}

/* Action buttons */
.form-actions {
  display: flex;
  gap: 15px;
  justify-content: flex-end;
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid #eee;
}

.btn-close {
  padding: 12px 24px;
  border: 1px solid #ddd;
  background: white;
  color: #333;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s ease;
  text-decoration: none;
}

.btn-close:hover {
  background: #f5f5f5;
  border-color: #bbb;
}

.featured-cta {
  padding: 12px 24px;
  border: none;
  background: var(--primary);
  color: white;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.featured-cta:hover:not(:disabled) {
  background: var(--primary-dark);
}

.featured-cta:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  background: #9ca3af;
}

/* Error states */
.error-state {
  text-align: center;
  padding: 40px;
}

.error-message {
  color: #e74c3c;
  margin-bottom: 20px;
  font-size: 16px;
}

.back-btn {
  display: inline-block;
  padding: 10px 20px;
  background: var(--primary);
  color: white;
  text-decoration: none;
  border-radius: 6px;
  transition: background-color 0.3s ease;
}

.back-btn:hover {
  background: var(--primary-dark);
}

/* Toast notification */
.toast-notification {
  position: fixed;
  top: 20px;
  right: 20px;
  padding: 15px 25px;
  border-radius: 6px;
  color: white;
  font-weight: 500;
  z-index: 1000;
  animation: slideIn 0.3s ease;
}

.toast-notification.success {
  background: #28a745;
}

.toast-notification.error {
  background: #dc3545;
}

/* Cancel Order Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 12px;
  padding: 0;
  max-width: 500px;
  width: 90%;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
}

.cancel-modal {
  max-width: 600px;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #eee;
}

.modal-header h2 {
  margin: 0;
  color: #dc3545;
  font-size: 1.25rem;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #666;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-btn:hover {
  color: #333;
}

.modal-body {
  padding: 20px;
}

.cancel-info {
  text-align: center;
  margin-bottom: 30px;
}

.warning-icon {
  font-size: 3rem;
  margin-bottom: 15px;
}

.cancel-info h3 {
  color: #dc3545;
  margin: 0 0 10px;
  font-size: 1.1rem;
}

.cancel-info p {
  color: #666;
  margin: 0;
  line-height: 1.5;
}

.admin-contact {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.admin-contact h4 {
  margin: 0 0 15px;
  color: #333;
  font-size: 1rem;
}

.contact-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  padding: 10px;
  background: white;
  border-radius: 6px;
  border: 1px solid #e9ecef;
}

.contact-item:last-child {
  margin-bottom: 0;
}

.contact-label {
  font-weight: 600;
  color: #495057;
  min-width: 80px;
}

.contact-value {
  display: flex;
  align-items: center;
  gap: 10px;
  flex: 1;
  justify-content: flex-end;
}

.phone-number,
.email-address {
  font-family: monospace;
  font-size: 14px;
  color: #007bff;
  font-weight: 600;
}

.copy-btn {
  background: #e9ecef;
  border: 1px solid #dee2e6;
  border-radius: 4px;
  padding: 4px 8px;
  cursor: pointer;
  font-size: 12px;
  transition: all 0.2s ease;
}

.copy-btn:hover {
  background: #dee2e6;
  border-color: #adb5bd;
}

.cancel-note {
  background: #fff3cd;
  padding: 15px;
  border-radius: 6px;
  border: 1px solid #ffeaa7;
}

.cancel-note p {
  margin: 0 0 10px;
  color: #856404;
  font-weight: 600;
}

.cancel-note ul {
  margin: 0;
  padding-left: 20px;
  color: #856404;
}

.cancel-note li {
  margin-bottom: 5px;
  line-height: 1.4;
}

.modal-footer {
  display: flex;
  gap: 15px;
  justify-content: flex-end;
  padding: 20px;
  border-top: 1px solid #eee;
}

.btn-call {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  background: #28a745;
  color: white;
  text-decoration: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-call:hover {
  background: #218838;
  color: white;
}

@keyframes slideIn {
  from {
    transform: translateX(100%);
  }
  to {
    transform: translateX(0);
  }
}

/* Responsive */
@media (max-width: 768px) {
  .form-grid {
    grid-template-columns: 1fr;
  }
  
  .calculation-grid {
    grid-template-columns: 1fr;
  }
  
  .customer-details {
    grid-template-columns: 1fr;
  }
  
  .form-actions {
    flex-direction: column;
  }

  .header-top {
    flex-direction: column;
    gap: 1rem;
  }

  .header-actions {
    margin-left: 0;
    width: 100%;
  }

  .btn-cancel-order {
    width: 100%;
    justify-content: center;
  }

  .modal-content {
    width: 95%;
    margin: 10px;
  }

  .contact-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }

  .contact-value {
    justify-content: flex-start;
    width: 100%;
  }

  .modal-footer {
    flex-direction: column;
  }

  .btn-call {
    width: 100%;
    justify-content: center;
  }
}
</style>