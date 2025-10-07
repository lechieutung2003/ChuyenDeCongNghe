<template>
  <!-- Thêm vào phần assignment tab -->
  <div class="mb-4">
    <el-button 
      type="primary"
      @click="getRecommendations"
      :loading="loadingRecommendations"
    >
      Gợi ý nhân viên phù hợp
    </el-button>
  </div>

  <!-- Dialog hiển thị đề xuất -->
  <el-dialog
    title="Nhân viên được đề xuất"
    v-model="recommendationDialog.visible"
    width="70%"
  >
    <el-table
      :data="recommendationDialog.recommendations"
      v-loading="recommendationDialog.loading"
    >
      <el-table-column label="Nhân viên">
        <template #default="{ row }">
          {{ row.employee.first_name }} {{ row.employee.last_name }}
        </template>
      </el-table-column>
      
      <el-table-column label="Độ phù hợp" width="120">
        <template #default="{ row }">
          <el-progress
            :percentage="row.score"
            :color="getMatchColor(row.score)"
          />
        </template>
      </el-table-column>
      
      <el-table-column label="Lý do phù hợp">
        <template #default="{ row }">
          <ul>
            <li v-for="(reason, index) in row.reasons" :key="index">
              {{ reason }}
            </li>
          </ul>
        </template>
      </el-table-column>
      
      <el-table-column label="Thao tác" width="120">
        <template #default="{ row }">
          <el-button
            type="primary"
            size="small"
            @click="assignEmployee(row.employee)"
            :disabled="isEmployeeAssigned(row.employee.id)"
          >
            Phân công
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </el-dialog>
</template>

<script setup>
// Thêm imports
import RecommendationService from '../../../services/dss/recommendation';

// Thêm reactive states
const recommendationDialog = reactive({
  visible: false,
  loading: false,
  recommendations: []
});

// Thêm methods
const getRecommendations = async () => {
  recommendationDialog.visible = true;
  recommendationDialog.loading = true;
  
  try {
    const recommendations = await RecommendationService.getRecommendations(route.params.id);
    recommendationDialog.recommendations = recommendations;
  } catch (error) {
    console.error('Lỗi khi lấy đề xuất:', error);
    ElMessage.error('Không thể lấy danh sách đề xuất.');
  } finally {
    recommendationDialog.loading = false;
  }
};

const getMatchColor = (score) => {
  if (score >= 80) return '#67c23a';
  if (score >= 60) return '#e6a23c';
  return '#f56c6c';
};
</script>