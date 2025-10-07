<template>
  <div>
    <!-- Phần hiển thị khuyến nghị khi bật DSS -->
    <div v-if="useDSS" class="bg-blue-50 p-4 rounded mb-4">
      <div class="flex justify-between items-center">
        <span class="font-medium">Top nhân viên phù hợp nhất</span>
        <el-button
          type="primary"
          size="small"
          @click="$emit('get-recommendations')"
          :loading="loadingRecommendations"
        >
          <i class="el-icon-refresh mr-1"></i> Cập nhật đề xuất
        </el-button>
      </div>
      
      <el-table
        v-if="recommendations.length > 0"
        :data="paginatedRecommendations"
        style="width: 100%"
        class="mt-4"
      >
        <el-table-column label="Xếp hạng" width="80">
          <template #default="{ $index }">
            {{ (dssLocalPagination.currentPage - 1) * dssLocalPagination.pageSize + $index + 1 }}
          </template>
        </el-table-column>
        
        <el-table-column label="Nhân viên" width="300">
          <template #default="{ row }">
            <div class="flex items-center">
              <el-avatar 
                :size="32" 
                :src="row.employee?.avatar_url || ''" 
                class="mr-2"
              />
              <div>
                <div>{{ row.employee?.first_name || '' }} {{ row.employee?.last_name || '' }}</div>
                <div class="text-gray-500 text-sm">{{ row.employee?.area || 'Không có khu vực' }}</div>
              </div>
            </div>
          </template>
        </el-table-column>

        <el-table-column label="Độ phù hợp" width="150">
          <template #default="{ row }">
            <div>
              <!-- Hiển thị thanh progress không có text -->
              <el-progress 
                :percentage="(row.score || 0)"
                :color="getMatchColor((row.score || 0))"
                :show-text="false"
              />
              <!-- Hiển thị điểm số dạng score/100 -->
              <div class="text-center text-xs text-gray-600 mt-1">
                {{ Math.round(row.score || 0) }}/100
              </div>
            </div>
          </template>
        </el-table-column>

        <el-table-column width="auto" />

        <el-table-column label="Lý do phù hợp" width="450">
          <template #default="{ row }">
            <ul class="list-disc list-inside">
              <li v-for="(reason, index) in (row.reasons || [])" 
                  :key="index" 
                  class="text-sm text-gray-600"
              >
                {{ reason }}
              </li>
            </ul>
          </template>
        </el-table-column>

        <el-table-column label="Thao tác" width="120" align="center">
          <template #default="{ row }">
            <el-button
              type="primary"
              size="small"
              @click="assignEmployee(row.employee)"
              :disabled="!row.employee || isEmployeeAssigned(row.employee?.id)"
            >
              Phân công
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <div v-if="recommendations.length > dssLocalPagination.pageSize" class="flex justify-center mt-4">
        <el-pagination
          v-model:currentPage="dssLocalPagination.currentPage"
          :page-size="dssLocalPagination.pageSize"
          :total="recommendations.length"
          layout="total, prev, pager, next"
          @current-change="handleDSSCurrentChange"
        />
      </div>

      <el-empty 
        v-else-if="!loadingRecommendations"
        description="Chưa có đề xuất nào"
      >
        <template #description>
          <p>Chưa có đề xuất nào. Nhấn vào nút 'Cập nhật đề xuất' để tìm nhân viên phù hợp.</p>
        </template>
        <el-button type="primary" @click="$emit('get-recommendations')">Tìm nhân viên phù hợp</el-button>
      </el-empty>
    </div>

    <!-- Bảng danh sách nhân viên (thủ công) -->
    <div class="mb-6" v-if="!useDSS">
      <!-- Công cụ tìm kiếm và lọc nhân viên -->
      <!-- <div class="mb-4">
          <div class="grid grid-cols-2 gap-4">
          <el-input 
              v-model="localEmployeeFilter.keyword" 
              placeholder="Tìm theo tên" 
              clearable
              @input="filterChanged"
          >
              <template #prefix>
              <i class="el-icon-search"></i>
              </template>
          </el-input>
          
          <el-select 
              v-model="localEmployeeFilter.area" 
              placeholder="Lọc theo khu vực" 
              clearable
              @change="filterChanged"
          >
              <el-option 
              v-for="area in availableAreas" 
              :key="area" 
              :label="area" 
              :value="area"
              />
          </el-select>
          </div>
      </div> -->
      
      <el-table 
        :data="paginatedEmployees" 
        border 
        v-loading="loadingEmployees"
        row-class-name="employee-row"
      >
        <el-table-column prop="id" label="Mã NV" width="140" sortable />
        <el-table-column label="Tên nhân viên" sortable>
          <template #default="{ row }">
            {{ row.first_name }} {{ row.last_name }}
          </template>
        </el-table-column>
        <el-table-column prop="area" label="Khu vực" width="120" sortable />
        <el-table-column label="Kỹ năng" width="200">
          <template #default="{ row }">
            <el-tag 
              v-for="skill in (row.skills || []).slice(0, 2)" 
              :key="skill" 
              size="small" 
              class="mr-1"
            >
              {{ skill }}
            </el-tag>
            <el-tooltip 
              v-if="(row.skills || []).length > 2" 
              :content="(row.skills || []).slice(2).join(', ')"
            >
              <el-tag size="small" type="info">+{{ (row.skills || []).length - 2 }}</el-tag>
            </el-tooltip>
            <span v-if="!row.skills || !row.skills.length" class="text-gray-400 text-sm">
              Không có kỹ năng
            </span>
            <!-- Thêm log debug để xem dữ liệu -->
            <div class="d-none">{{ console.log('Row data:', row) }}</div>
          </template>
        </el-table-column>
        <el-table-column label="Trạng thái" width="120">
          <template #default="{ row }">
            <el-tag 
              :type="getEmployeeAvailability(row) ? 'success' : 'danger'" 
              size="small"
            >
              {{ getEmployeeAvailability(row) ? 'Sẵn sàng' : 'Bận' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="Thao tác" width="120" align="center">
          <template #default="{ row }">
            <el-button 
              type="primary" 
              size="small" 
              @click="assignEmployee(row)"
              :disabled="isEmployeeAssigned(row.id)"
            >
              {{ isEmployeeAssigned(row.id) ? 'Đã phân công' : 'Phân công' }}
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <div class="flex justify-center mt-4">
        <el-pagination
          v-model:currentPage="localPagination.currentPage"
          :page-size="localPagination.pageSize"
          :total="filteredEmployees.length"
          layout="total, prev, pager, next"
          @current-change="handleCurrentChange"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, watch } from 'vue';

const props = defineProps({
  order: Object,
  useDSS: Boolean,
  recommendations: Array,
  loadingRecommendations: Boolean,
  loadingEmployees: Boolean,
  allEmployees: Array,
  filteredEmployees: Array,
  employeeFilter: Object,
  pagination: Object,
  showOnlyAvailable: Boolean,
  availableAreas: Array
});

console.log('Nhân viên:', props.filteredEmployees);

const emit = defineEmits(['assign-employee', 'get-recommendations', 'filter-employees']);

// Local copies of reactive objects to avoid mutating props
const localEmployeeFilter = reactive({
  keyword: props.employeeFilter?.keyword || '',
  area: props.employeeFilter?.area || ''
});

const localPagination = reactive({
  currentPage: props.pagination?.currentPage || 1,
  pageSize: props.pagination?.pageSize || 4
});

const dssLocalPagination = reactive({
  currentPage: 1,
  pageSize: 4
});

// Keep local filters in sync with props
watch(() => props.employeeFilter, (newFilter) => {
  if (newFilter) {
    localEmployeeFilter.keyword = newFilter.keyword;
    localEmployeeFilter.area = newFilter.area;
  }
}, { deep: true });

watch(() => props.pagination, (newPagination) => {
  if (newPagination) {
    localPagination.currentPage = newPagination.currentPage;
    localPagination.pageSize = newPagination.pageSize;
  }
}, { deep: true });

// Reset DSS pagination when recommendations change
watch(() => props.recommendations, () => {
  dssLocalPagination.currentPage = 1;
});

// Computed properties
const paginatedEmployees = computed(() => {
  if (!Array.isArray(props.filteredEmployees)) return [];
  
  const start = (localPagination.currentPage - 1) * localPagination.pageSize;
  const end = start + localPagination.pageSize;
  return props.filteredEmployees.slice(start, end);
});

// Computed property để phân trang cho recommendations
const paginatedRecommendations = computed(() => {
  if (!Array.isArray(props.recommendations)) return [];
  
  const start = (dssLocalPagination.currentPage - 1) * dssLocalPagination.pageSize;
  const end = start + dssLocalPagination.pageSize;
  return props.recommendations.slice(start, end);
});

// Methods
const getMatchColor = (score) => {
  if (score >= 80) return '#67c23a';  // Xanh lá
  if (score >= 60) return '#e6a23c';  // Cam
  return '#f56c6c';  // Đỏ
};

const getEmployeeAvailability = (employee) => {
  return employee.status === 1;
};

const isEmployeeAssigned = (employeeId) => {
  // This would typically check against the assignedEmployees prop
  // For demo purposes, returning false
  return false;
};

const assignEmployee = (employee) => {
  emit('assign-employee', employee);
};

const handleCurrentChange = (currentPage) => {
  localPagination.currentPage = currentPage;
  // You might want to emit an event to update pagination in parent
};

// Thêm xử lý cho phân trang DSS
const handleDSSCurrentChange = (currentPage) => {
  dssLocalPagination.currentPage = currentPage;
};

const filterChanged = () => {
  // Emit event to parent to handle filtering
  emit('filter-employees', localEmployeeFilter, true);
};
</script>

<style scoped>
.employee-row:hover {
  background-color: #f5f7fa;
}
</style>