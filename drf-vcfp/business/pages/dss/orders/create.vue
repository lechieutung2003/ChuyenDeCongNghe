<script setup lang="ts">
import { ref, onMounted, watch, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useI18n } from 'vue-i18n';
import CreateOrderService from '@/services/dss/users/customer';
import { useOauthStore } from '@/stores/oauth';
import serviceTypesApi from '@/services/dss/serviceTypes';
// Import customer CSS
import '@/assets/css/customer.css';
definePageMeta({
  middleware: 'role-based'
})
const store = useOauthStore();
const router = useRouter();
const { t } = useI18n();

// Thông tin customer từ hr_customer
const customerInfo = ref<any>(null);
const loadingCustomer = ref(true);

const order = ref({
  customer: null as string | null, // Sẽ được cập nhật sau khi lấy thông tin customer
  service_type: null,
  area_m2: null,
  requested_hours: null as number | null,
  preferred_start_time: '',
  preferred_end_time: '',
  estimated_hours: null as number | null,
  status: 'pending',
  note: '',
  cost_confirm: '',
  payment_method: 'cash' as 'cash' | 'transfer'
});

const productivity = ref<number | null>(null);
const estimatedPrice = ref<number | null>(null);
const priceExplanation = ref<string>(''); // 🆕 label mô tả cách tính
const minRequiredHours = ref<number | null>(null); // 🆕 thời gian tối thiểu
const isTimeValid = ref<boolean>(true); // 🆕 kiểm tra thời gian hợp lệ
const timeValidationMessage = ref<string>(''); // 🆕 thông báo lỗi thời gian
const isStartTimeValid = ref<boolean>(true); // 🆕 kiểm tra thời gian bắt đầu hợp lệ
const startTimeValidationMessage = ref<string>(''); // 🆕 thông báo lỗi thời gian bắt đầu

// 🆕 Modal thanh toán
const showPaymentModal = ref<boolean>(false);
const paymentMethod = ref<'cash' | 'transfer'>('cash');
const isSubmitting = ref<boolean>(false);

// 🆕 Modal hóa đơn
const showInvoiceModal = ref<boolean>(false);
const invoiceData = ref<any>(null);

type ServiceType = { id: string; name: string; [key: string]: any };
const serviceTypes = ref<ServiceType[]>([]);

// Hàm lấy thông tin customer từ hr_customer
const fetchCustomerInfo = async () => {
  try {
    loadingCustomer.value = true;
    console.log('Loading customer info...');
    
    const response = await CreateOrderService.getUser();
    console.log('Customer API response:', response);
    
    const customer = response.data || response;
    customerInfo.value = customer;
    
    // Cập nhật customer ID vào order
    order.value.customer = customer.id;
    
    console.log('Customer info loaded:', customer);
    console.log('Order customer updated:', order.value.customer);
    
  } catch (error) {
    console.error('Error loading customer info:', error);
    alert(t('create_order_customer_error'));
  } finally {
    loadingCustomer.value = false;
  }
};

// Computed property để lấy giá dịch vụ được chọn
const selectedServicePrice = computed(() => {
  if (!order.value.service_type) return null;
  
  const service = serviceTypes.value.find(s => s.id === order.value.service_type);
  if (!service) return null;
  
  if (service.price_per_m2) {
    return Number(service.price_per_m2);
  } else if (service.name?.toLowerCase().includes('deep cleaning')) {
    return 3000;
  } else if (service.name?.toLowerCase().includes('regular cleaning')) {
    return 155000;
  }
  
  return null;
});

const fetchServiceTypes = async () => {
  const response = await serviceTypesApi.getAll();
  if (response && response.results) {
    serviceTypes.value = response.results;
  } else if (Array.isArray(response)) {
    serviceTypes.value = response;
  } else {
    serviceTypes.value = [];
  }
  console.log('serviceTypes.value:', serviceTypes.value);
};

const calcProductivity = () => {
  const serviceId = order.value.service_type;
  if (!serviceId) {
    productivity.value = null;
    return;
  }
  const service = serviceTypes.value.find(s => s.id === serviceId);
  if (service) {
    if (service.cleaning_rate_m2_per_h) {
      productivity.value = Number(service.cleaning_rate_m2_per_h);
    } else if (service.name?.toLowerCase().includes('regular cleaning')) {
      productivity.value = 40;
    } else if (service.name?.toLowerCase().includes('deep cleaning')) {
      productivity.value = 35;
    } else {
      productivity.value = null;
    }
  } else {
    productivity.value = null;
  }
};

const calcEstimatedHours = () => {
  const area = order.value.area_m2;
  if (!area || !productivity.value || productivity.value <= 0) {
    order.value.estimated_hours = null;
    minRequiredHours.value = null;
    return;
  }
  order.value.estimated_hours = +(area / productivity.value).toFixed(2);
  // Tính thời gian tối thiểu = 60% thời gian ước tính
  minRequiredHours.value = +(order.value.estimated_hours * 0.6).toFixed(2);
};

//  Hàm kiểm tra thời gian bắt đầu hợp lệ
const validateStartTime = () => {
  const startTime = order.value.preferred_start_time;
  
  if (!startTime) {
    isStartTimeValid.value = true;
    startTimeValidationMessage.value = '';
    return;
  }
  
  const startDate = new Date(startTime);
  const currentDate = new Date();
  const oneHourLater = new Date(currentDate.getTime() + 60 * 60 * 1000); // Thêm 1 tiếng
  
  if (startDate < oneHourLater) {
    isStartTimeValid.value = false;
    startTimeValidationMessage.value = `Thời gian bắt đầu phải cách thời điểm hiện tại ít nhất 1 tiếng (sau ${oneHourLater.toLocaleString('vi-VN')})`;
  } else {
    isStartTimeValid.value = true;
    startTimeValidationMessage.value = '';
  }
};

//  Hàm kiểm tra thời gian yêu cầu hợp lệ
const validateRequestedTime = () => {
  const requested = order.value.requested_hours;
  const minRequired = minRequiredHours.value;
  const estimated = order.value.estimated_hours;
  
  if (!requested || !minRequired || !estimated) {
    isTimeValid.value = true;
    timeValidationMessage.value = '';
    return;
  }
  
  if (requested < minRequired) {
    isTimeValid.value = false;
    timeValidationMessage.value = t('create_order_validation_error', { 
      message: `${t('create_order_min_time', { time: formatHourMinute(minRequired) })} (60% của ${formatHourMinute(estimated)})` 
    });
  } else {
    isTimeValid.value = true;
    timeValidationMessage.value = '';
  }
};

const calcRequestedHours = () => {
  const start = order.value.preferred_start_time;
  const end = order.value.preferred_end_time;
  if (!start || !end) {
    order.value.requested_hours = null;
    return;
  }
  const startDate = new Date(start);
  const endDate = new Date(end);
  const diffMs = endDate.getTime() - startDate.getTime();
  if (diffMs > 0) {
    order.value.requested_hours = +(diffMs / (1000 * 60 * 60)).toFixed(2);
  } else {
    order.value.requested_hours = null;
  }
};

const calcEstimatedPrice = () => {
  const serviceId = order.value.service_type;
  const area = order.value.area_m2;
  if (!serviceId || !area || area <= 0) {
    estimatedPrice.value = null;
    priceExplanation.value = '';
    return;
  }
  let pricePerM2 = 0;
  const service = serviceTypes.value.find(s => s.id === serviceId);
  if (service) {
    if (service.price_per_m2) {
      pricePerM2 = Number(service.price_per_m2);
    } else if (service.name?.toLowerCase().includes('deep cleaning')) {
      pricePerM2 = 3000;
    } else if (service.name?.toLowerCase().includes('regular cleaning')) {
      pricePerM2 = 155000;
    }
  }

  let basePrice = pricePerM2 > 0 ? pricePerM2 * area : null;
  let explanation = `Giá cơ bản: ${pricePerM2.toLocaleString('vi-VN')} x ${area} m² = ${(basePrice || 0).toLocaleString('vi-VN')} VNĐ`;

  const requested = order.value.requested_hours;
  const estimated = order.value.estimated_hours;
  if (basePrice && requested && estimated && requested < estimated) {
    const diff = estimated - requested;
    let factor = 1;
    if (diff > 0.1 && diff <= 1) factor = 1.2;
    else if (diff > 1 && diff <= 2) factor = 1.3;
    else if (diff > 2) factor = 1.5;

    if (factor > 1) {
      explanation += ` (áp dụng hệ số ${factor} do số giờ yêu cầu < số giờ ước tính)`;
      basePrice = basePrice * factor;
    }
  }

  // Thêm 10% VAT vào giá cuối cùng
  if (basePrice) {
    const vatAmount = Math.round(basePrice * 0.1);
    const finalPrice = basePrice + vatAmount;
    explanation += `\nGiá gốc: ${basePrice.toLocaleString('vi-VN')} VNĐ + VAT 10% (${vatAmount.toLocaleString('vi-VN')} VNĐ) = ${finalPrice.toLocaleString('vi-VN')} VNĐ`;
    estimatedPrice.value = finalPrice;
  } else {
    estimatedPrice.value = null;
  }

  priceExplanation.value = explanation;
};

// Theo dõi thay đổi để tính toán
watch(() => [order.value.service_type], calcProductivity);
watch(() => [order.value.area_m2, productivity.value], calcEstimatedHours);
watch(() => [order.value.preferred_start_time], () => {
  validateStartTime();
});
watch(() => [order.value.preferred_start_time, order.value.preferred_end_time], () => {
  calcRequestedHours();
  validateRequestedTime();
});
watch(() => [order.value.service_type, order.value.area_m2, order.value.requested_hours, order.value.estimated_hours], calcEstimatedPrice);
watch(() => [order.value.requested_hours, minRequiredHours.value], validateRequestedTime);

const openPaymentModal = () => {
  if (!isTimeValid.value) {
    alert(t('create_order_validation_error', { message: timeValidationMessage.value }));
    return;
  }
  
  if (!isStartTimeValid.value) {
    alert(`Lỗi thời gian: ${startTimeValidationMessage.value}`);
    return;
  }
  
  showPaymentModal.value = true;
};

const closePaymentModal = () => {
  showPaymentModal.value = false;
  paymentMethod.value = 'cash';
  isSubmitting.value = false;
};

// 🆕 Hàm tạo hóa đơn
const generateInvoice = (orderResponse: any) => {
  const currentDate = new Date();
  // Sử dụng ID của đơn hàng làm invoiceNumber trực tiếp
  const invoiceNumber = orderResponse.id;
  
  // estimatedPrice đã bao gồm VAT, cần tính ngược lại để lấy giá gốc
  const totalPrice = estimatedPrice.value || 0;
  const subtotal = Math.round(totalPrice / 1.1); // Giá gốc (không bao gồm VAT)
  const tax = totalPrice - subtotal; // VAT = 10% của giá gốc
  
  invoiceData.value = {
    invoiceNumber,
    orderInfo: {
      id: orderResponse.id,
      serviceName: serviceTypes.value.find(s => s.id === order.value.service_type)?.name || t('create_order_value_na'),
      area: order.value.area_m2,
      workingHours: formatHourMinute(order.value.requested_hours),
      startTime: order.value.preferred_start_time,
      endTime: order.value.preferred_end_time,
      note: order.value.note || t('create_order_value_none'),
      paymentMethod: paymentMethod.value === 'cash' ? t('payment_cash') : t('payment_transfer')
    },
    customerInfo: {
      name: customerInfo.value?.name || t('Customer'),
      email: customerInfo.value?.email || '',
      phone: customerInfo.value?.phone || ''
    },
    pricing: {
      subtotal: subtotal,
      tax: tax,
      total: totalPrice
    },
    issueDate: currentDate.toLocaleDateString('vi-VN'),
    dueDate: new Date(currentDate.getTime() + 7 * 24 * 60 * 60 * 1000).toLocaleDateString('vi-VN') // 7 ngày sau
  };
  
  showInvoiceModal.value = true;
};

const closeInvoiceModal = () => {
  showInvoiceModal.value = false;
  invoiceData.value = null;
};

const downloadInvoice = () => {
  // Tạo hóa đơn PDF
  const invoice = invoiceData.value;
  
  // Tạo HTML content cho PDF
  const htmlContent = `
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <title>${t('create_order_invoice_title')} ${invoice.invoiceNumber}</title>
      <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .header { text-align: center; margin-bottom: 30px; background: #f8f9fa; padding: 20px; }
        .title { font-size: 24px; font-weight: bold; color: #333; }
        .invoice-number { font-size: 18px; margin: 10px 0; }
        .section { margin: 20px 0; padding: 15px; border: 1px solid #ddd; }
        .section h3 { margin: 0 0 15px 0; color: #555; }
        .row { display: flex; justify-content: space-between; margin: 8px 0; }
        .total { background: #e3f2fd; padding: 15px; font-weight: bold; font-size: 18px; }
      </style>
    </head>
    <body>
      <div class="header">
        <div class="title">${t('create_order_invoice_header')}</div>
        <div class="invoice-number">${t('create_order_invoice_number', { number: invoice.invoiceNumber })}</div>
        <div>${t('create_order_invoice_issue_date', { date: invoice.issueDate })} | ${t('create_order_invoice_due_date', { date: invoice.dueDate })}</div>
      </div>
      
      <div class="section">
        <h3>${t('create_order_customer_info_title')}</h3>
        <div class="row"><span>${t('create_order_customer_name_label')}</span><span>${invoice.customerInfo.name}</span></div>
        ${invoice.customerInfo.email ? `<div class="row"><span>${t('create_order_customer_email_label')}</span><span>${invoice.customerInfo.email}</span></div>` : ''}
        ${invoice.customerInfo.phone ? `<div class="row"><span>${t('create_order_customer_phone_label')}</span><span>${invoice.customerInfo.phone}</span></div>` : ''}
      </div>
      
      <div class="section">
        <h3>${t('create_order_service_details')}</h3>
        <div class="row"><span>${t('create_order_service_name')}</span><span>${invoice.orderInfo.serviceName}</span></div>
        <div class="row"><span>${t('create_order_working_area')}</span><span>${invoice.orderInfo.area} m²</span></div>
        <div class="row"><span>${t('create_order_working_hours')}</span><span>${invoice.orderInfo.workingHours}</span></div>
        <div class="row"><span>${t('create_order_start_time_label')}</span><span>${new Date(invoice.orderInfo.startTime).toLocaleString('vi-VN')}</span></div>
        <div class="row"><span>${t('create_order_end_time_label')}</span><span>${new Date(invoice.orderInfo.endTime).toLocaleString('vi-VN')}</span></div>
        <div class="row"><span>${t('create_order_payment_method_label')}</span><span>${invoice.orderInfo.paymentMethod}</span></div>
        ${invoice.orderInfo.note !== t('create_order_value_none') ? `<div class="row"><span>${t('create_order_note_label')}</span><span>${invoice.orderInfo.note}</span></div>` : ''}
      </div>
      
      <div class="section">
        <h3>${t('create_order_payment_info')}</h3>
        <div class="row"><span>${t('create_order_subtotal')}</span><span>${invoice.pricing.subtotal.toLocaleString('vi-VN')} VNĐ</span></div>
        <div class="row"><span>${t('create_order_vat')}</span><span>${invoice.pricing.tax.toLocaleString('vi-VN')} VNĐ</span></div>
        <div class="total"><span>${t('create_order_total')}</span><span>${invoice.pricing.total.toLocaleString('vi-VN')} VNĐ</span></div>
      </div>
      
      <div style="text-align: center; margin-top: 30px; color: #666;">
        ${t('create_order_thank_you')}
      </div>
    </body>
    </html>
  `;
  
  // Tạo PDF từ HTML bằng cách in
  const printWindow = window.open('', '_blank');
  if (printWindow) {
    printWindow.document.write(htmlContent);
    printWindow.document.close();
    printWindow.focus();
    printWindow.print();
    // Tự động đóng cửa sổ sau khi in
    printWindow.onafterprint = () => printWindow.close();
  } else {
    alert(t('create_order_download_error'));
  }
};

// const submitOrder = async () => {
//   if (isSubmitting.value) return;
  
//   try {
//     isSubmitting.value = true;
//     const payload = { ...order.value };
    
//     if (estimatedPrice.value !== null) {
//       payload.cost_confirm = String(estimatedPrice.value);
//     }
    
//     // Thêm thông tin thanh toán
//     payload.payment_method = paymentMethod.value;

//     const response = await CreateOrderService.createOrder(payload) as any;
//     console.log('API response:', response);
    
//     if (response && response.id) {
//       closePaymentModal();
      
//       // Tạo hóa đơn sau khi đặt đơn thành công
//       generateInvoice(response);
      
//       // Không chuyển trang ngay mà cho người dùng xem hóa đơn trước
//       // router.push('/dss/customer-orders');
//     } else {
//       alert('Tạo đơn thất bại, vui lòng kiểm tra thông tin.');
//     }
//   } catch (error: any) {
//     console.error('Failed to create order', error?.response?.data || error);
//     alert('Tạo đơn thất bại, vui lòng kiểm tra thông tin.');
//   } finally {
//     isSubmitting.value = false;
//   }
// };


const submitOrder = async () => {
  if (isSubmitting.value) return;
  try {
    isSubmitting.value = true;
    
    // Tạo payload với format giống Postman
    const payload: any = {
      customer: order.value.customer, // ID từ hr_customer
      service_type: order.value.service_type,
      area_m2: order.value.area_m2,
      requested_hours: order.value.requested_hours,
      preferred_start_time: order.value.preferred_start_time,
      preferred_end_time: order.value.preferred_end_time,
      estimated_hours: order.value.estimated_hours,
      status: order.value.status,
      note: order.value.note || "",
    };
    
    // Thêm cost_confirm nếu có
    if (estimatedPrice.value !== null) {
      payload.cost_confirm = String(estimatedPrice.value);
    }

    // Log payload để kiểm tra
    console.log('Payload gửi lên (format Postman):', payload);

    const response = await CreateOrderService.createOrder(payload) as any;
    console.log('API response:', response);
    
    if (response && response.id) {
      closePaymentModal();
      generateInvoice(response);
      // Có thể chuyển trang sau khi xem hóa đơn
    } else {
      alert(t('create_order_error'));
    }
  } catch (error: any) {
    console.error('Lỗi chi tiết từ backend:', error?.response?.data || error);
    alert(t('create_order_error'));
  } finally {
    isSubmitting.value = false;
  }
};
function formatHourMinute(hours: number|null) {
  if (hours === null || isNaN(hours)) return '';
  if (hours > 0 && hours * 60 < 1) return t('create_order_time_one_minute');
  const h = Math.floor(hours);
  let m = Math.round((hours - h) * 60);
  if (h === 0) return t('create_order_time_minutes', { minutes: m });
  if (m === 0) return t('create_order_time_hours', { hours: h });
  return t('create_order_time_hours_minutes', { hours: h, minutes: m });
}

onMounted(() => {
  fetchServiceTypes();
  fetchCustomerInfo();
});
</script>

<template>
  <div class="about-page">
    <section class="stripe white">
      <div class="container">
        <div class="content-header">
          <h1 class="section-title">{{ t('create_order_title') }}</h1>
          <p class="section-subtitle">{{ t('create_order_subtitle') }}</p>
          
          <!-- Customer info display -->
          <div v-if="loadingCustomer" class="customer-info loading">
            <p>{{ t('create_order_loading_customer') }}</p>
          </div>
          <div v-else-if="customerInfo" class="customer-info">
            <h3>{{ t('create_order_customer_info') }}</h3>
            <div class="customer-details">
              <div class="customer-item">
                <span class="label">{{ t('create_order_customer_name') }}</span>
                <span class="value">{{ customerInfo.name }}</span>
              </div>
              <div class="customer-item">
                <span class="label">{{ t('create_order_customer_email') }}</span>
                <span class="value">{{ customerInfo.email }}</span>
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
        
        <form class="order-form" @submit.prevent="submitOrder">
          <div class="form-grid">
            <div class="form-column">
              <div class="form-group">
                <label>{{ t('create_order_service') }}</label>
                <div class="input-wrapper">
                  <select v-model="order.service_type" class="form-input" required>
                    <option value="" disabled>{{ t('create_order_service_placeholder') }}</option>
                    <option v-for="service in serviceTypes" :key="service.id" :value="service.id">
                      {{ service.name }}
                    </option>
                  </select>
                </div>
              </div>
              <div class="form-group">
                <label>{{ t('create_order_area') }}</label>
                <div class="input-wrapper">
                  <input v-model="order.area_m2" type="number" class="form-input" min="0" step="any" :placeholder="t('create_order_area_placeholder')" required />
                </div>
              </div>
              <div class="form-group">
                <label>{{ t('create_order_note') }}</label>
                <div class="input-wrapper">
                  <textarea v-model="order.note" class="form-input" :placeholder="t('create_order_note_placeholder')" rows="3"></textarea>
                </div>
              </div>
            </div>
            
            <div class="form-column">
              <div class="form-group">
                <label>{{ t('create_order_price_per_m2') }}</label>
                <div class="input-wrapper">
                  <input 
                    type="text" 
                    :value="selectedServicePrice ? selectedServicePrice.toLocaleString('vi-VN') + ' VNĐ' : ''" 
                    class="form-input price-display" 
                    disabled 
                    :placeholder="t('create_order_price_placeholder')" 
                  />
                </div>
              </div>
              <div class="form-group">
                <label>{{ t('create_order_start_time') }}</label>
                <div class="input-wrapper" :class="{ 'error': !isStartTimeValid }">
                  <input v-model="order.preferred_start_time" type="datetime-local" class="form-input" required />
                </div>
                <div v-if="!isStartTimeValid && startTimeValidationMessage" class="error-message">
                  {{ startTimeValidationMessage }}
                </div>
                <small class="form-hint">
                  Thời gian bắt đầu phải cách thời điểm hiện tại ít nhất 1 tiếng
                </small>
              </div>
              <div class="form-group">
                <label>{{ t('create_order_end_time') }}</label>
                <div class="input-wrapper">
                  <input v-model="order.preferred_end_time" type="datetime-local" class="form-input" required />
                </div>
              </div>
            </div>
          </div>

          <!-- Calculation section -->
          <div class="calculation-section">
            <h3 class="calculation-title">{{ t('create_order_calculation_title') }}</h3>
            <div class="calculation-grid">
              <div class="form-group">
                <label>{{ t('create_order_estimated_hours') }}</label>
                <div class="input-wrapper">
                  <input 
                    type="text" 
                    :value="order.estimated_hours !== null ? formatHourMinute(order.estimated_hours) : ''" 
                    class="form-input estimated-display" 
                    disabled 
                    :placeholder="t('create_order_estimated_hours_placeholder')" 
                  />
                </div>
                <small v-if="productivity && order.area_m2" class="form-hint">
                  {{ t('create_order_productivity', { productivity }) }}
                </small>
              </div>
              <div class="form-group">
                <label>{{ t('create_order_requested_hours') }}</label>
                <div class="input-wrapper" :class="{ 'error': !isTimeValid }">
                  <input type="text" :value="order.requested_hours !== null ? formatHourMinute(order.requested_hours) : ''" class="form-input requested-display" readonly :placeholder="t('create_order_requested_hours_placeholder')" />
                </div>
                <div v-if="!isTimeValid && timeValidationMessage" class="error-message">
                   {{ timeValidationMessage }}
                </div>
                <small v-if="minRequiredHours" class="form-hint success">
                  {{ t('create_order_min_time', { time: formatHourMinute(minRequiredHours) }) }}
                </small>
              </div>
              <div class="form-group">
                <label>{{ t('create_order_estimated_price') }}</label>
                <div class="input-wrapper">
                  <input type="text" :value="estimatedPrice !== null ? estimatedPrice.toLocaleString('vi-VN') + ' VNĐ' : ''" class="form-input price-estimated" disabled :placeholder="t('create_order_estimated_price_placeholder')" />
                </div>
                <small v-if="priceExplanation" class="form-hint">
                  {{ priceExplanation }}
                </small>
              </div>
              <div class="form-group">
                <!-- Empty space for layout balance -->
              </div>
            </div>
          </div>
          
          <button type="button" class="featured-cta" :disabled="!isTimeValid || !isStartTimeValid" @click="openPaymentModal">
            {{ !isTimeValid || !isStartTimeValid ? t('create_order_time_invalid') : t('create_order_create_button') }}
          </button>
        </form>
      </div>
    </section>
    
    <!-- Modal thanh toán -->
    <div v-if="showPaymentModal" class="modal-overlay" @click="closePaymentModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>{{ t('create_order_payment_title') }}</h2>
          <button class="close-btn" @click="closePaymentModal">×</button>
        </div>
        
        <div class="modal-body">
          <!-- Thông tin đơn hàng -->
          <div class="t-card">
            <h3>{{ t('create_order_order_info') }}</h3>
            <div class="summary-item">
              <span>{{ t('create_order_service_label') }}</span>
              <span>{{ serviceTypes.find(s => s.id === order.service_type)?.name || t('create_order_value_na') }}</span>
            </div>
            <div class="summary-item">
              <span>{{ t('create_order_area_label') }}</span>
              <span>{{ order.area_m2 }} m²</span>
            </div>
            <div class="summary-item">
              <span>{{ t('create_order_time_label') }}</span>
              <span>{{ formatHourMinute(order.requested_hours) }}</span>
            </div>
            <div class="summary-item total">
              <span>{{ t('create_order_total_label') }}</span>
              <span class="price">{{ estimatedPrice?.toLocaleString('vi-VN') || '0' }} VNĐ</span>
            </div>
          </div>

          <!-- Chọn phương thức thanh toán -->
          <div class="payment-methods">
            <h3>{{ t('create_order_payment_methods') }}</h3>
            
            <div class="payment-option">
              <label class="radio-container">
                <input type="radio" v-model="paymentMethod" value="cash" checked>
                <span class="checkmark"></span>
                <div class="payment-info">
                  <div class="payment-title">{{ t('create_order_cash_payment') }}</div>
                  <div class="payment-desc">{{ t('create_order_cash_description') }}</div>
                </div>
              </label>
            </div>
          </div>
        </div>

        <div class="modal-footer">
          <button class="btn-close" @click="closePaymentModal">{{ t('create_order_cancel') }}</button>
          <button class="btn-download" @click="submitOrder" :disabled="isSubmitting">
            {{ isSubmitting ? t('create_order_processing') : t('create_order_confirm') }}
          </button>
        </div>
      </div>
    </div>
    
    <!-- Modal Hóa đơn -->
    <div v-if="showInvoiceModal && invoiceData" class="modal-overlay" @click="closeInvoiceModal">
      <div class="modal-content invoice-modal" @click.stop>
        <div class="modal-header">
          <h2>{{ t('create_order_invoice_title') }}</h2>
          <button class="close-btn" @click="closeInvoiceModal">×</button>
        </div>
        
        <div class="modal-body">
          <div class="invoice-header">
            <div class="invoice-title">{{ t('create_order_invoice_header') }}</div>
            <div class="invoice-number">{{ t('create_order_invoice_number', { number: invoiceData.invoiceNumber }) }}</div>
            <div class="invoice-date">
              <div>{{ t('create_order_invoice_issue_date', { date: invoiceData.issueDate }) }}</div>
              <div>{{ t('create_order_invoice_due_date', { date: invoiceData.dueDate }) }}</div>
            </div>
          </div>

          <div class="invoice-section">
            <h4>{{ t('create_order_customer_info_title') }}</h4>
            <div class="info-row">
              <span>{{ t('create_order_customer_name_label') }}</span>
              <span>{{ invoiceData.customerInfo.name }}</span>
            </div>
            <div class="info-row" v-if="invoiceData.customerInfo.email">
              <span>{{ t('create_order_customer_email_label') }}</span>
              <span>{{ invoiceData.customerInfo.email }}</span>
            </div>
            <div class="info-row" v-if="invoiceData.customerInfo.phone">
              <span>{{ t('create_order_customer_phone_label') }}</span>
              <span>{{ invoiceData.customerInfo.phone }}</span>
            </div>
          </div>

          <div class="invoice-section">
            <h4>{{ t('create_order_service_details') }}</h4>
            <div class="service-details">
              <div class="info-row">
                <span>{{ t('create_order_service_name') }}</span>
                <span>{{ invoiceData.orderInfo.serviceName }}</span>
              </div>
              <div class="info-row">
                <span>{{ t('create_order_working_area') }}</span>
                <span>{{ invoiceData.orderInfo.area }} m²</span>
              </div>
              <div class="info-row">
                <span>{{ t('create_order_working_hours') }}</span>
                <span>{{ invoiceData.orderInfo.workingHours }}</span>
              </div>
              <div class="info-row">
                <span>{{ t('create_order_start_time_label') }}</span>
                <span>{{ new Date(invoiceData.orderInfo.startTime).toLocaleString('vi-VN') }}</span>
              </div>
              <div class="info-row">
                <span>{{ t('create_order_end_time_label') }}</span>
                <span>{{ new Date(invoiceData.orderInfo.endTime).toLocaleString('vi-VN') }}</span>
              </div>
              <div class="info-row">
                <span>{{ t('create_order_payment_method_label') }}</span>
                <span>{{ invoiceData.orderInfo.paymentMethod }}</span>
              </div>
              <div class="info-row" v-if="invoiceData.orderInfo.note !== t('create_order_value_none')">
                <span>{{ t('create_order_note_label') }}</span>
                <span>{{ invoiceData.orderInfo.note }}</span>
              </div>
            </div>
          </div>

          <div class="invoice-section">
            <h4>{{ t('create_order_payment_info') }}</h4>
            <div class="pricing-details">
              <div class="info-row">
                <span>{{ t('create_order_subtotal') }}</span>
                <span>{{ invoiceData.pricing.subtotal.toLocaleString('vi-VN') }} VNĐ</span>
              </div>
              <div class="info-row">
                <span>{{ t('create_order_vat') }}</span>
                <span>{{ invoiceData.pricing.tax.toLocaleString('vi-VN') }} VNĐ</span>
              </div>
              <div class="total-amount">
                <span><strong>{{ t('create_order_total') }}</strong></span>
                <span class="total-price"><strong>{{ invoiceData.pricing.total.toLocaleString('vi-VN') }} VNĐ</strong></span>
              </div>
            </div>
          </div>
        </div>

        <div class="modal-footer">
          <button class="btn-download" @click="downloadInvoice">{{ t('create_order_download_pdf') }}</button>
          <button class="btn-close" @click="() => { closeInvoiceModal(); router.push('/dss/customer-orders'); }">
            {{ t('create_order_view_orders') }}
          </button>
        </div>        <div class="modal-footer">
          
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Customer info styles */
.customer-info {
  background: var(--bg-card);
  border: 1px solid rgba(59, 130, 246, 0.1);
  border-radius: 20px;
  padding: 1.5rem;
  margin: 2rem 0;
  box-shadow: var(--shadow);
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

/* Form styles */
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

/* Calculation section */
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

.calculation-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
}

/* Payment methods styles */
.payment-methods h3 {
  margin: 0 0 1rem;
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-dark);
}

.payment-option {
  margin-bottom: 1rem;
}

.radio-container {
  display: flex;
  align-items: center;
  cursor: pointer;
  padding: 1rem;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  transition: all 0.2s;
}

.radio-container:hover {
  border-color: var(--primary);
  background-color: var(--bg-light);
}

.radio-container input[type="radio"] {
  display: none;
}

.checkmark {
  width: 20px;
  height: 20px;
  border: 2px solid #d1d5db;
  border-radius: 50%;
  margin-right: 12px;
  position: relative;
  transition: all 0.2s;
}

.radio-container input[type="radio"]:checked + .checkmark {
  border-color: var(--primary);
  background-color: var(--primary);
}

.radio-container input[type="radio"]:checked + .checkmark::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 8px;
  height: 8px;
  background: white;
  border-radius: 50%;
}

.payment-info {
  flex: 1;
}

.payment-title {
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-dark);
  margin-bottom: 0.25rem;
}

.payment-desc {
  font-size: 0.875rem;
  color: var(--text-light);
}

/* Summary item styles */
.summary-item {
  display: flex;
  justify-content: space-between;
  padding: 0.5rem 0;
  border-bottom: 1px solid #e5e7eb;
}

.summary-item:last-child {
  border-bottom: none;
}

.summary-item.total {
  font-weight: 600;
  font-size: 1rem;
  margin-top: 0.5rem;
  padding-top: 0.75rem;
  border-top: 2px solid #e5e7eb;
}

.summary-item .price {
  color: #ef4444;
  font-weight: 700;
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
}
</style>
