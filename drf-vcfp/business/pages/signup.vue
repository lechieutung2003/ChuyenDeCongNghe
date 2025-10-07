<template>
  <div class="h-screen w-full flex justify-center items-center bg-gray-50">
    <div class="form">
      <div class="form-header">
        <h1 class="form-title">{{ $t('create_account_title') }}</h1>
        <p class="form-subtitle">{{ $t('create_account_subtitle') }}</p>
      </div>
      <form @submit.prevent="submitForm" class="grid grid-cols-1 md:grid-cols-2 gap-3">
        <!-- First Name -->
        <div class="flex-column">
          <label>{{ $t('first_name') }}</label>
          <div class="inputForm">
            <input
              v-model="form.first_name"
              type="text"
              class="input"
              :placeholder="$t('first_name')"
            />
          </div>
        </div>

        <!-- Last Name -->
        <div class="flex-column">
          <label>{{ $t('last_name') }}</label>
          <div class="inputForm">
            <input
              v-model="form.last_name"
              type="text"
              class="input"
              :placeholder="$t('last_name')"
            />
          </div>
        </div>

        <!-- Email -->
        <div class="flex-column">
          <label>{{ $t('email') }}</label>
          <div class="inputForm" :class="{ 'error-border': emailError }">
            <input
              v-model="form.email"
              type="email"
              class="input"
              :placeholder="$t('email')"
              @blur="validateEmail"
            />
          </div>
          <span v-if="emailError" class="error-text">{{ emailError }}</span>
        </div>

        <!-- Password -->
        <div class="flex-column">
          <label>{{ $t('password') }}</label>
          <div class="inputForm" :class="{ 'error-border': passwordError }">
            <input
              v-model="form.password"
              type="password"
              class="input"
              :placeholder="$t('password')"
              @blur="validatePassword"
            />
          </div>
          <span v-if="passwordError" class="error-text">{{ passwordError }}</span>
        </div>

        <!-- Phone -->
        <div class="flex-column">
          <label>{{ $t('phone') }}</label>
          <div class="inputForm">
            <input
              v-model="form.phone"
              type="text"
              class="input"
              :placeholder="$t('phone')"
            />
          </div>
        </div>

        <!-- Address -->
        <div class="flex-column">
          <label>{{ $t('Address') }}</label>
          <div class="inputForm">
            <input
              v-model="form.address"
              type="text"
              class="input"
              :placeholder="$t('Address')"
            />
          </div>
        </div>

        <!-- Area -->
        <div class="flex-column col-span-2">
          <label>{{ $t('area') }}</label>
          <div class="inputForm" style="position: relative;">
            <input
              v-model="form.area"
              type="text"
              class="input"
              :placeholder="$t('area_placeholder')"
              @input="filterAreas"
              @focus="showAreaList = true"
              @blur="hideAreaList"
              autocomplete="off"
            />
            <!-- Dropdown danh sách khu vực -->
            <div v-if="showAreaList && filteredAreas.length > 0" class="area-dropdown">
              <div
                v-for="area in filteredAreas"
                :key="area"
                class="area-option"
                @mousedown="selectArea(area)"
              >
                <span class="area-icon">📍</span>
                <span class="area-name">{{ area }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Submit Button -->
        <div class="col-span-2">
          <button type="submit" class="button-submit" :disabled="isLoading">
            <span v-if="isLoading">{{ $t('Registering') }}</span>
            <span v-else>{{ $t('Register') }}</span>
          </button>
        </div>

        <!-- Success Message -->
        <p v-if="isSubmitted" class="p col-span-2">
          {{ $t('Account created for', { email: form.email }) }}
        </p>

        <!-- Login Link -->
        <div class="flex justify-center items-center col-span-2">
          <p class="text-center">
            {{ $t('have_an_account') }}
            <NuxtLink to="/" class="span font-semibold">
              {{ $t('Login') }}
            </NuxtLink>
          </p>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import IconAmoz from '~/assets/icons/BigLogo.svg'
import { ref, computed, watch, onMounted } from 'vue'
import { ElNotification } from 'element-plus'
import OAuthService from '@/services/oauth'
import '@/assets/css/form.css'

definePageMeta({
  layout: 'anonymous'
})

const form = ref({
  email: '',
  password: '',
  first_name: '',
  last_name: '',
  // name sẽ tự động tạo từ first_name + last_name ở backend
  phone: '',
  address: '',
  area: ''
})

const isLoading = ref(false)
const isSubmitted = ref(false)
const emailError = ref('')
const passwordError = ref('')

// Area search functionality
const showAreaList = ref(false)
const filteredAreas = ref<string[]>([])

// Area keys for translation
const areaKeys: string[] = [
  // Các quận
  'haichau', 'nguhanhson', 'lienchieu', 'sontra', 'camle', 'thanhkhe',
  // Các phường xã
  'anhai', 'ankhe', 'anthang', 'avuong', 'bana', 'banthach', 'bengiang', 'benhien',
  'chiendan', 'dacpring', 'dailoc', 'dienban', 'dienbanbac', 'dienbandong', 'dienbantay',
  'dongduong', 'donggiang', 'ducphu', 'duynghia', 'duyxuyen', 'gonoi', 'hanha',
  'haivan', 'hiepduc', 'hoacuong', 'hoakhanh', 'hoatien', 'hoavang', 'hoaxuan',
  'hoangsa', 'hoian', 'hoiandong', 'hoiantay', 'hungson', 'huongtra', 'khamduc',
  'ladee', 'laee', 'lanhngoc', 'namgiang', 'namphuoc', 'namtramy', 'nongson',
  'nuithanh', 'phuninh', 'phuthuan', 'phuocchanh', 'phuochiep', 'phuocnang',
  'phuocthanh', 'phuoctra', 'quangphu', 'quephuoc', 'queson', 'quesontrung',
  'soncamha', 'songkon', 'songvang', 'tamanh', 'tamhai', 'tamky', 'tammy',
  'tamxuan', 'tanhiep', 'taygiang', 'tayho', 'thangan', 'thangbinh', 'thangdien',
  'thangphu', 'thangtruong', 'thanhbinh', 'thanhmy', 'thubon', 'thuongduc',
  'tienphuoc', 'tradoc', 'tragiap', 'traleng', 'tralien', 'tralinh', 'tramy',
  'tratan', 'tratap', 'travan', 'vietan', 'vugia', 'xuanphu'
]

// Fallback static areas (Vietnamese)
const staticAreas = [
  'Hải Châu', 'Ngũ Hành Sơn', 'Liên Chiểu', 'Sơn Trà', 'Cẩm Lệ', 'Thanh Khê',
  'An Hải', 'An Khê', 'An Thắng', 'Avương', 'Bà Nà', 'Bàn Thạch', 'Bến Giằng', 'Bến Hiên',
  'Chiên Đàn', 'Đắc Pring', 'Đại Lộc', 'Điện Bàn', 'Điện Bàn Bắc', 'Điện Bàn Đông', 'Điện Bàn Tây',
  'Đồng Dương', 'Đông Giang', 'Đức Phú', 'Duy Nghĩa', 'Duy Xuyên', 'Gò Nổi', 'Hà Nha',
  'Hải Vân', 'Hiệp Đức', 'Hòa Cường', 'Hòa Khánh', 'Hòa Tiến', 'Hòa Vang', 'Hòa Xuân',
  'Hoàng Sa', 'Hội An', 'Hội An Đông', 'Hội An Tây', 'Hùng Sơn', 'Hương Trà', 'Khâm Đức',
  'La Dêê', 'La Êê', 'Lãnh Ngọc', 'Nam Giang', 'Nam Phước', 'Nam Trà My', 'Nông Sơn',
  'Núi Thành', 'Phú Ninh', 'Phú Thuận', 'Phước Chánh', 'Phước Hiệp', 'Phước Năng',
  'Phước Thành', 'Phước Trà', 'Quảng Phú', 'Quế Phước', 'Quế Sơn', 'Quế Sơn Trung',
  'Sơn Cẩm Hà', 'Sông Kôn', 'Sông Vàng', 'Tam Anh', 'Tam Hải', 'Tam Kỳ', 'Tam Mỹ',
  'Tam Xuân', 'Tân Hiệp', 'Tây Giang', 'Tây Hồ', 'Thăng An', 'Thăng Bình', 'Thăng Điền',
  'Thăng Phú', 'Thăng Trường', 'Thạnh Bình', 'Thạnh Mỹ', 'Thu Bồn', 'Thượng Đức',
  'Tiên Phước', 'Trà Đốc', 'Trà Giáp', 'Trà Leng', 'Trà Liên', 'Trà Linh', 'Trà My',
  'Trà Tân', 'Trà Tập', 'Trà Vân', 'Việt An', 'Vu Gia', 'Xuân Phú'
]

// Get translated areas with fallback
const allAreas = computed(() => {
  try {
    const { $t } = useNuxtApp()
    return areaKeys.map(key => $t(key) || key)
  } catch (error) {
    // Fallback to static areas if translation fails
    return staticAreas
  }
})

// Initialize with all areas
onMounted(() => {
  filteredAreas.value = allAreas.value
})

// Watch for language changes to update filtered areas
watch(allAreas, (newAreas) => {
  if (!form.value.area) {
    filteredAreas.value = newAreas
  } else {
    filterAreas()
  }
})

// Area search functions
const filterAreas = () => {
  const searchTerm = form.value.area.toLowerCase()
  if (!searchTerm) {
    filteredAreas.value = allAreas.value
    return
  }
  
  filteredAreas.value = allAreas.value.filter(area => 
    area.toLowerCase().includes(searchTerm)
  )
}

const hideAreaList = () => {
  setTimeout(() => {
    showAreaList.value = false
  }, 200)
}

const selectArea = (area: string) => {
  form.value.area = area
  showAreaList.value = false
}

const validateEmail = () => {
  if (!form.value.email) {
    emailError.value = 'Email không được để trống'
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.value.email)) {
    emailError.value = 'Email không hợp lệ'
  } else {
    emailError.value = ''
  }
}

const validatePassword = () => {
  if (!form.value.password) {
    passwordError.value = 'Mật khẩu không được để trống'
  } else if (form.value.password.length < 6) {
    passwordError.value = 'Mật khẩu tối thiểu 6 ký tự'
  } else {
    passwordError.value = ''
  }
}

const validateForm = () => {
  validateEmail()
  validatePassword()
  return !emailError.value && !passwordError.value
}

const submitForm = async () => {
  if (!validateForm()) return
  
  isLoading.value = true
  try {
    await OAuthService.registerCustomer(form.value)
    isSubmitted.value = true
    ElNotification({
      title: 'Thành công',
      message: 'Tài khoản đã được tạo thành công!',
      type: 'success',
      duration: 5000
    })
  } catch (error: any) {
    console.error('Registration error:', error)
    
    let errorMessage = 'Có lỗi xảy ra khi đăng ký. Vui lòng thử lại!'
    
    // Handle specific error cases
    if (error?.response?.status === 400) {
      const errorData = error.response.data
      if (errorData?.email) {
        errorMessage = 'Email này đã được sử dụng. Vui lòng chọn email khác!'
      } else if (errorData?.phone) {
        errorMessage = 'Số điện thoại này đã được sử dụng. Vui lòng chọn số khác!'
      } else if (errorData?.area) {
        errorMessage = 'Khu vực không hợp lệ. Vui lòng chọn khu vực từ danh sách!'
      } else if (errorData?.non_field_errors) {
        errorMessage = errorData.non_field_errors[0] || errorMessage
      } else if (typeof errorData === 'string') {
        errorMessage = errorData
      }
    } else if (error?.response?.status === 500) {
      errorMessage = 'Lỗi server. Vui lòng thử lại sau!'
    } else if (error?.code === 'NETWORK_ERROR' || !error?.response) {
      errorMessage = 'Không thể kết nối đến server. Vui lòng kiểm tra kết nối internet!'
    } else if (error?.message && !error.message.includes('POST')) {
      errorMessage = error.message
    }
    
    ElNotification({
      title: 'Đăng ký thất bại',
      message: errorMessage,
      type: 'error',
      duration: 8000
    })
  } finally {
    isLoading.value = false
  }
}
</script>
<style scoped>
.form {
  width: 70%;
  max-width: 80%; 
  height: 87%;
  padding: 40px; 
  background-color: #fff; 
  border-radius: 10px; 
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1); 
  margin-top: 5%;
}
.input {
  width: 400px; 
}
.error-text {
  margin-top: 0.25rem; 
}

/* Area search dropdown styles */
.area-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  max-height: 250px;
  overflow-y: auto;
  background: white;
  border: 2px solid #e5e7eb;
  border-top: none;
  border-radius: 0 0 12px 12px;
  z-index: 1000;
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  animation: slideDown 0.2s ease-out;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.area-option {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  cursor: pointer;
  border-bottom: 1px solid #f3f4f6;
  transition: all 0.2s ease;
  font-size: 14px;
}

.area-option:last-child {
  border-bottom: none;
  border-radius: 0 0 10px 10px;
}

.area-option:hover {
  background-color: #f8fafc;
  border-left: 3px solid #2d79f3;
  padding-left: 13px;
}

.area-option:active {
  background-color: #e5e7eb;
}

.area-icon {
  margin-right: 8px;
  font-size: 16px;
}

.area-name {
  flex: 1;
  font-weight: 500;
  color: #374151;
}

/* Scrollbar styling */
.area-dropdown::-webkit-scrollbar {
  width: 6px;
}

.area-dropdown::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 10px;
}

.area-dropdown::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 10px;
}

.area-dropdown::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}
</style>