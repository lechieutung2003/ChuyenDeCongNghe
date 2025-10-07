<template>
  <el-card v-loading="loading">
    <div v-if="order && order.status !== 'cancelled'">
      
      <!-- Thông tin đơn hàng cơ bản -->
      <div class="order-summary bg-blue-50 p-3 rounded mb-4 border-l-4 border-blue-400">
        <div class="grid grid-cols-4 md:grid-cols-7 gap-2">
            <!-- Khu vực - mở rộng gấp đôi -->
            <div class="col-span-1 md:col-span-1">
            <span class="text-xs text-gray-500 block">Khu vực</span>
            <strong class="text-sm truncate block">{{ order.customer_details?.area || 'Không có' }}</strong>
            </div>
            
            <!-- Khách hàng - thu nhỏ -->
            <div class="col-span-1 md:col-span-1">
            <span class="text-xs text-gray-500 block">Khách hàng</span>
            <strong class="text-sm">{{ order.customer_name }}</strong>
            </div>
            
            <!-- Diện tích - thu nhỏ -->
            <div class="col-span-1 md:col-span-1">
            <span class="text-xs text-gray-500 block">Diện tích</span>
            <strong class="text-sm">{{ order.area_m2 }} m²</strong>
            </div>
            
            <!-- Thời gian yêu cầu - mở rộng -->
            <div class="col-span-4 md:col-span-3">
            <span class="text-xs text-gray-500 block">Thời gian yêu cầu</span>
            <div class="flex items-center">
                <strong class="text-sm">
                {{ formatDateTime(order.preferred_start_time) }}
                </strong>
                <span class="mx-1 text-gray-500">→</span>
                <strong class="text-sm">
                {{ formatDateTime(order.preferred_end_time) }}
                </strong>
            </div>
            </div>
        </div>
      </div>

      <!-- Phần nút chuyển đổi DSS -->
      <div class="flex justify-between items-center mb-4">
        <h4 class="text-md font-medium">Danh sách nhân viên</h4>
        
        <div>
          <el-tooltip 
            content="Hệ thống gợi ý thông minh giúp tìm nhân viên phù hợp nhất cho đơn hàng này" 
            placement="top"
          >
            <el-button 
              :type="useDSS ? 'primary' : 'default'" 
              @click="toggleDSS"
              size="default"
              icon="el-icon-magic-stick"
            >
              {{ useDSS ? 'Tắt chế độ gợi ý thông minh' : 'Bật chế độ gợi ý thông minh' }}
            </el-button>
          </el-tooltip>
        </div>
      </div>

      <!-- Component bảng danh sách nhân viên - Thủ công hoặc DSS -->
      <EmployeeSelectionTable
        :order="order"
        :useDSS="useDSS"
        :recommendations="recommendations"
        :loadingRecommendations="loadingRecommendations"
        :loadingEmployees="loadingEmployees"
        :allEmployees="allEmployees"
        :filteredEmployees="filteredEmployees"
        :employeeFilter="employeeFilter"
        :pagination="pagination"
        :showOnlyAvailable="showOnlyAvailable"
        :availableAreas="availableAreas"
        @assign-employee="assignEmployee"
        @get-recommendations="getRecommendations"
        @filter-employees="filterEmployees"
      />

      <!-- Component bảng nhân viên đã phân công -->
      <AssignedEmployeesTable
        :order="order"
        :assignedEmployees="assignedEmployees"
        @remove-assignment="removeAssignment"
        @update-assignment-time="updateAssignmentEndTime"
        @reset-assignments="resetAssignments"
        @save-assignments="saveAssignments"
      />
    </div>
    <div v-else-if="order && order.status === 'cancelled'" class="text-center p-10">
      <el-alert
        title="Đơn hàng đã bị hủy"
        type="error"
        description="Không thể phân công nhân viên cho đơn hàng đã hủy"
        show-icon
        :closable="false"
      />
    </div>
    <div v-else class="text-center p-10">
      <p>Không tìm thấy thông tin đơn hàng.</p>
    </div>
  </el-card>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import { formatDateTime } from '../../../utils/time';
import EmployeeService from '../../../services/dss/users/employees';
import AssignmentService from '../../../services/dss/order-assignment';
import RecommendationService from '../../../services/dss/recommendationService';
import OrderService from '../../../services/dss/order';
import EmployeeSelectionTable from '../../../components/dss/orders/EmployeeSelectionTable.vue';
import AssignedEmployeesTable from '../../../components/dss/orders/AssignedEmployeesTable.vue';

const props = defineProps({
  order: Object,
  loading: Boolean,
});

// Reactive states
const useDSS = ref(false);
const loadingRecommendations = ref(false);
const recommendations = ref([]);
const assignedEmployees = ref([]);
const loadingEmployees = ref(false);
const allEmployees = ref([]);
const filteredEmployees = ref([]);
const showOnlyAvailable = ref(false);
const initialAssignments = ref([]);

// Phân trang
const pagination = reactive({
  currentPage: 1,
  pageSize: 4,
});

// Lọc nhân viên
const employeeFilter = reactive({
  keyword: '',
  area: '',
});

// Dialog hiển thị lịch
const scheduleDialog = reactive({
  visible: false,
  employee: null,
  schedule: [],
  loading: false,
});

// Lấy danh sách khu vực
const availableAreas = computed(() => {
  if (!Array.isArray(allEmployees.value)) {
    return [];
  }
  
  const areas = new Set();
  allEmployees.value.forEach(emp => {
    if (emp?.area) {
      areas.add(emp.area);
    }
  });
  return [...areas].sort();
});

// Thêm methods
const toggleDSS = () => {
  useDSS.value = !useDSS.value;
  
  if (useDSS.value) {
    ElMessage({
      message: 'Đã bật chế độ gợi ý thông minh',
      type: 'success',
      duration: 2000
    });
    
    // Tự động tìm đề xuất khi bật chế độ DSS
    if (recommendations.value.length === 0) {
      getRecommendations();
    }
  } else {
    ElMessage({
      message: 'Đã tắt chế độ gợi ý thông minh',
      type: 'info',
      duration: 2000
    });
  }
};

const getRecommendations = async () => {
  if (!props.order) return;
  
  loadingRecommendations.value = true;
  
  try {
    const response = await RecommendationService.getRecommendations(props.order.id);
    console.log('Raw API response:', response);
    
    let tempRecommendations = [];
    
    // Xử lý các định dạng response khác nhau
    if (Array.isArray(response)) {
      tempRecommendations = response;
    } 
    else if (response && Array.isArray(response.results)) {
      tempRecommendations = response.results;
    }
    else if (response && !Array.isArray(response)) {
      tempRecommendations = [response];
    }
    
    // Kiểm tra dữ liệu hợp lệ
    tempRecommendations = tempRecommendations.filter(item => 
      item && item.employee && item.score !== undefined
    );
    
    // Sắp xếp theo score cao nhất
    tempRecommendations.sort((a, b) => b.score - a.score);
    
    // Lấy 5 nhân viên có score cao nhất
    recommendations.value = tempRecommendations;
    
    console.log('Top 5 recommendations:', recommendations.value);
    
    if (recommendations.value.length === 0) {
      ElMessage.info('Không có đề xuất nào cho đơn hàng này.');
    } else if (recommendations.value.length < 5) {
      ElMessage.info(`Chỉ tìm thấy ${recommendations.value.length} nhân viên phù hợp.`);
    } else {
      ElMessage.success(`Đã tìm thấy top 5 nhân viên phù hợp nhất.`);
    }
  } catch (error) {
    console.error('Lỗi khi lấy đề xuất:', error);
    ElMessage.error('Không thể lấy danh sách đề xuất.');
  } finally {
    loadingRecommendations.value = false;
  }
};

const getEmployeeAvailability = (employee) => {
  return employee.status === 1;   
};

// Fetch all employees
const fetchAllEmployees = async () => {
  loadingEmployees.value = true;
  try {
    const response = await EmployeeService.getEmployees({
      page: 1,
      page_size: 100 // Hoặc số lượng phù hợp
    });
    
    // Kiểm tra và xử lý response
    if (response && response.results) {
      allEmployees.value = response.results;
    } else {
      allEmployees.value = [];
      console.warn('Unexpected response format:', response);
    }
    
    console.log('Fetched employees:', allEmployees.value);
    filterEmployees();
  } catch (error) {
    console.error('Lỗi khi tải danh sách nhân viên:', error);
    ElMessage.error('Không thể tải danh sách nhân viên.');
    allEmployees.value = [];
  } finally {
    loadingEmployees.value = false;
  }
};

// Fetch assigned employees
const fetchAssignedEmployees = async () => {
  if (!props.order) return;
  try {
    const data = await AssignmentService.getAssignments(props.order.id);
    assignedEmployees.value = data || [];
    initialAssignments.value = (data || []).map(a => ({ ...a })); // Lưu bản gốc để so sánh
  } catch (error) {
    assignedEmployees.value = [];
    initialAssignments.value = [];
  }
};

// Lọc nhân viên
const filterEmployees = (resetPage = false) => {
  if (!Array.isArray(allEmployees.value)) {
    filteredEmployees.value = [];
    return;
  }

  let result = allEmployees.value.map(emp => ({...emp}));
  
  // Lọc theo từ khóa
  if (employeeFilter.keyword) {
    const keyword = employeeFilter.keyword.toLowerCase();
    result = result.filter(emp => {
      const fullName = `${emp.first_name || ''} ${emp.last_name || ''}`.toLowerCase();
      const workMail = (emp.work_mail || '').toLowerCase();
      return fullName.includes(keyword) || workMail.includes(keyword);
    });
  }
  
  // Lọc theo khu vực
  if (employeeFilter.area) {
    result = result.filter(emp => emp.area === employeeFilter.area);
  }
  
  // Lọc theo tình trạng khả dụng
  if (showOnlyAvailable.value) {
    result = result.filter(emp => getEmployeeAvailability(emp));
  }

  console.log('Check filtered employees with skills:', result.map(emp => ({
    name: `${emp.first_name} ${emp.last_name}`,
    skills: emp.skills
  })));
  

  result.sort((a, b) => {
    // Lấy thông tin trạng thái và khu vực
    const aAvailable = getEmployeeAvailability(a);
    const bAvailable = getEmployeeAvailability(b);
    const orderArea = props.order?.customer_details?.area || '';
    const aSameArea = a.area === orderArea;
    const bSameArea = b.area === orderArea;
    
    // Tính điểm cho nhân viên a và b
    // - Sẵn sàng + cùng khu vực: 3 điểm
    // - Chỉ sẵn sàng: 2 điểm
    // - Chỉ cùng khu vực: 1 điểm
    // - Không đáp ứng gì: 0 điểm
    
    let aScore = 0;
    let bScore = 0;
    
    if (aAvailable && aSameArea) aScore = 3;
    else if (aAvailable) aScore = 2;
    else if (aSameArea) aScore = 1;
    
    if (bAvailable && bSameArea) bScore = 3;
    else if (bAvailable) bScore = 2;
    else if (bSameArea) bScore = 1;
    
    // So sánh điểm
    if (aScore !== bScore) {
      return bScore - aScore; // Sắp xếp theo điểm giảm dần
    }
    
    // // Nếu cùng điểm, sắp xếp theo tên
    // const aName = `${a.first_name || ''} ${a.last_name || ''}`;
    // const bName = `${b.first_name || ''} ${b.last_name || ''}`;
    // return aName.localeCompare(bName);
  });

  
  
  filteredEmployees.value = result;
  
  if (resetPage) {
    pagination.currentPage = 1;
  }
};

// Check if an employee is already assigned
const isEmployeeAssigned = (employeeId) => {
  if (!employeeId) return false;
  
  return assignedEmployees.value.some(
    assignment => {
      const assignedId = assignment.employee?.id || assignment.employee;
      return assignedId === employeeId;
    }
  );
};

// Assign employee to the order
const assignEmployee = (employee) => {
  if (!props.order) return;
  
  // Kiểm tra employee có tồn tại không
  if (!employee) {
    ElMessage.error('Không tìm thấy thông tin nhân viên');
    return;
  }
  
  // Lấy ID của employee
  const employeeId = employee.id || employee._id;
  
  if (!employeeId) {
    ElMessage.error('ID nhân viên không hợp lệ');
    return;
  }
  
  if (isEmployeeAssigned(employeeId)) {
    ElMessage.warning('Nhân viên này đã được phân công.');
    return;
  }
  
  ElMessageBox.confirm(
    `Bạn có chắc chắn muốn phân công nhân viên ${employee.first_name || ''} ${employee.last_name || ''} cho đơn hàng này?`,
    'Xác nhận phân công',
    {
      confirmButtonText: 'Xác nhận',
      cancelButtonText: 'Hủy',
      type: 'info'
    }
  ).then(() => {
    // Use order's preferred times as default
    const assignment = {
      id: `temp-${Date.now()}`, // Temporary ID for UI
      employee: employee,
      order: props.order.id,
      start_time: props.order.preferred_start_time,
      end_time: props.order.preferred_end_time,
      status: 'assigned'
    };
    
    assignedEmployees.value.push(assignment);
    ElMessage.success('Đã thêm nhân viên vào danh sách phân công.');
  }).catch(() => {
    // User cancelled
  });
};

// Remove assignment
const removeAssignment = (assignmentId) => {
  ElMessageBox.confirm(
    'Bạn có chắc chắn muốn hủy phân công nhân viên này?',
    'Xác nhận hủy phân công',
    {
      confirmButtonText: 'Xác nhận',
      cancelButtonText: 'Hủy',
      type: 'warning'
    }
  ).then(() => {
    assignedEmployees.value = assignedEmployees.value.filter(
      assignment => assignment.id !== assignmentId
    );
    ElMessage.success('Đã hủy phân công nhân viên.');
  }).catch(() => {
    // User cancelled
  });
};

// Cập nhật giờ kết thúc dựa vào giờ bắt đầu
const updateAssignmentEndTime = (assignment) => {
  // Mặc định thời gian làm việc là 4 giờ
  if (assignment.start_time) {
    const startTime = new Date(assignment.start_time);
    const endTime = new Date(startTime);
    endTime.setHours(startTime.getHours() + 4);
    assignment.end_time = endTime;
  }
};

// Reset phân công
const resetAssignments = async () => {
  ElMessageBox.confirm(
    'Bạn có chắc chắn muốn đặt lại tất cả phân công?',
    'Xác nhận đặt lại',
    {
      confirmButtonText: 'Xác nhận',
      cancelButtonText: 'Hủy',
      type: 'warning'
    }
  ).then(async () => {
    // Xóa tất cả assignment của order trên backend
    try {
      // Lặp qua tất cả assignment hiện tại và gọi API xóa
      for (const assignment of assignedEmployees.value) {
        if (assignment.id && !assignment.id.toString().startsWith('temp-')) {
          await AssignmentService.deleteAssignment(assignment.id);
        }
      }
      assignedEmployees.value = [];
      ElMessage.success('Đã đặt lại danh sách phân công.');
      // Sau khi xóa, cập nhật lại danh sách từ backend
      await fetchAssignedEmployees();
    } catch (error) {
      ElMessage.error('Không thể đặt lại phân công.');
    }
  }).catch((error) => {
    console.log('User cancelled reset:', error);
  });
};

// Save all assignments
const saveAssignments = async () => {
  if (!props.order) return;
  try {
    const orderId = props.order.id;

    // 1. Xác định các assignment đã bị xóa
    const currentIds = assignedEmployees.value.map(a => a.id);
    const deletedAssignments = initialAssignments.value.filter(a => !currentIds.includes(a.id));

    // 2. Xóa các assignment này trên backend
    for (const assignment of deletedAssignments) {
      if (assignment.id && !assignment.id.toString().startsWith('temp-')) {
        await AssignmentService.deleteAssignment(assignment.id);
      }
    }

    // 3. Thêm mới các assignment mới
    const newAssignments = assignedEmployees.value
      .filter(a => a.id.toString().startsWith('temp-'))
      .map(a => ({
        employee: a.employee.id,
        order: orderId,
        start_time: a.start_time,
        end_time: a.end_time,
        assigned_time: new Date().toISOString(),
        status: 'assigned',
        work_hours: calculateWorkHours(a.start_time, a.end_time),
        cost: 0
      }));

    if (newAssignments.length > 0) {
      await AssignmentService.createAssignments(orderId, newAssignments);
    }

    await OrderService.updateOrderStatus(orderId, 'confirmed');
    ElMessage.success('Phân công nhân viên thành công!');
    await fetchAssignedEmployees();
  } catch (error) {
    ElMessage.error('Không thể lưu phân công nhân viên.');
  }
};

// Thêm hàm tính work_hours
const calculateWorkHours = (start, end) => {
  if (!start || !end) return 4; // Giá trị mặc định
  const hours = (new Date(end) - new Date(start)) / (1000 * 60 * 60);
  return Math.round(hours * 100) / 100; // Làm tròn 2 chữ số thập phân
};

watch(() => props.order, (newOrder) => {
  if (newOrder) {
    fetchAssignedEmployees();
  }
}, { immediate: true });

onMounted(() => {
  fetchAllEmployees();
});
</script> 