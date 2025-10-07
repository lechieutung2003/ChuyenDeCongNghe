<template>
  <div>
    <h4 class="text-md font-medium mb-2">Nhân viên đã phân công ({{ assignedEmployees.length }})</h4>
    <el-table 
      :data="assignedEmployees" 
      border 
      empty-text="Chưa có nhân viên được phân công"
    >
      <el-table-column prop="id" label="Mã gắn đơn" width="150" />
      <el-table-column label="Tên nhân viên">
        <template #default="{ row }">
          {{ row.employee.first_name }} {{ row.employee.last_name }}
        </template>
      </el-table-column>
      <el-table-column prop="employee.area" label="Khu vực" width="120" />
      <el-table-column label="Thời gian bắt đầu" width="180">
        <template #default="{ row }">
          <el-date-picker
            v-model="row.start_time"
            type="datetime"
            placeholder="Chọn thời gian"
            size="small"
            style="width: 160px"
            @change="updateAssignmentTime(row)"
          />
        </template>
      </el-table-column>
      <el-table-column label="Thời gian kết thúc" width="180">
        <template #default="{ row }">
          <el-date-picker
            v-model="row.end_time"
            type="datetime"
            placeholder="Chọn thời gian"
            size="small"
            style="width: 160px"
          />
        </template>
      </el-table-column>
      <el-table-column label="Thao tác" width="150" align="center">
        <template #default="{ row }">
          <el-button 
            type="danger" 
            size="small" 
            @click="removeAssignment(row.id)"
          >
            Hủy phân công
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <div class="mt-4 flex justify-between items-center">
      <div>
        <el-alert
          v-if="shouldShowWarning"
          title="Cảnh báo: Số lượng nhân viên được phân công có thể không đủ để hoàn thành đơn hàng đúng thời gian"
          type="warning"
          show-icon
          :closable="false"
          class="mb-3"
        />
      </div>
      <div>
        <el-button @click="resetAssignments">Đặt lại</el-button>
        <el-button 
          type="success" 
          @click="saveAssignments" 
          :disabled="assignedEmployees.length === 0"
        >
          Lưu phân công
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  order: {
    type: Object,
    required: true
  },
  assignedEmployees: {
    type: Array,
    required: true
  }
});

const emit = defineEmits([
  'remove-assignment', 
  'update-assignment-time', 
  'reset-assignments', 
  'save-assignments'
]);

const shouldShowWarning = computed(() => {
  if (!props.order || !props.assignedEmployees || props.assignedEmployees.length === 0) {
    return false;
  }
  // Check if there are fewer employees than needed based on estimated hours
  return props.assignedEmployees.length > 0 && 
         props.assignedEmployees.length < (props.order.estimated_hours / 4);
});

const removeAssignment = (assignmentId) => {
  emit('remove-assignment', assignmentId);
};

const updateAssignmentTime = (assignment) => {
  emit('update-assignment-time', assignment);
};

const resetAssignments = () => {
  emit('reset-assignments');
};

const saveAssignments = () => {
  emit('save-assignments');
};
</script>

<style scoped>
.assigned-employee-row {
  background-color: #f0f9eb;
}
</style>