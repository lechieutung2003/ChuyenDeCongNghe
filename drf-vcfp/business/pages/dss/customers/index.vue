<template>
  <div class="customer-list-container p-6">
    <div class="mb-4 flex justify-between items-center">
      <h1 class="text-xl font-bold">Quản lý Khách hàng</h1>
      <el-button type="primary" @click="router.push('/dss/customers/create')">
        <el-icon class="mr-1"><Plus /></el-icon>Thêm khách hàng
      </el-button>
    </div>

    <!-- Bộ lọc -->
    <el-card class="filter-card mb-4">
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <el-input
          v-model="filters.keyword"
          placeholder="Tìm theo tên, email, số điện thoại"
          clearable
          @keyup.enter="handleSearch"
        />
        <el-select v-model="filters.area" placeholder="Khu vực" clearable>
          <el-option label="Nội thành" value="urban" />
          <el-option label="Ngoại thành" value="suburban" />
        </el-select>
        <el-button type="primary" @click="handleSearch">Tìm kiếm</el-button>
        <el-button @click="resetFilters">Đặt lại</el-button>
      </div>
    </el-card>

    <!-- Bảng dữ liệu -->
    <el-table
      v-loading="loading"
      :data="paginatedCustomers"
      stripe
      class="w-full"
      size="small"
    >
      <el-table-column label="Tên khách hàng" prop="name" min-width="150" />
      <el-table-column label="Email" prop="email" min-width="200" />
      <el-table-column label="Số điện thoại" prop="phone" min-width="120" />
      <el-table-column label="Địa chỉ" prop="address" min-width="200" />
      <el-table-column label="Khu vực" min-width="100">
        <template #default="{ row }">
          {{ row.area === "urban" ? "Nội thành" : "Ngoại thành" }}
        </template>
      </el-table-column>
      <el-table-column label="Thao tác" width="200" fixed="right">
        <template #default="{ row }">
          <el-button-group>
            <el-button
              size="small"
              @click="router.push(`/dss/customers/${row.id}`)"
            >
              Chi tiết
            </el-button>
            <el-button size="small" type="danger" @click="handleDelete(row.id)">
              Xóa
            </el-button>
          </el-button-group>
        </template>
      </el-table-column>
    </el-table>

    <!-- Phân trang -->
    <div class="mt-4 flex justify-end">
      <el-pagination
        v-model:current-page="pagination.currentPage"
        v-model:page-size="pagination.pageSize"
        :page-sizes="[10, 20, 50, 100]"
        :total="filteredCustomers.length"
        layout="sizes, prev, pager, next"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import { ElMessage, ElMessageBox } from "element-plus";
import { Plus } from "@element-plus/icons-vue";
import customerService from "@/services/dss/customerService";

definePageMeta({
  layout: "dss",
  middleware: ["auth"],
});

const router = useRouter();
const loading = ref(false);
const customers = ref([]);

// Bộ lọc
const filters = reactive({
  keyword: "",
  area: "",
});

// Phân trang
const pagination = reactive({
  currentPage: 1,
  pageSize: 10,
});

// Lấy danh sách
const fetchCustomers = async () => {
  loading.value = true;
  try {
    const response = await customerService.getCustomers();
    console.log("API Response:", response); // Log để debug
    // Kiểm tra và đảm bảo response là một mảng
    if (Array.isArray(response)) {
      customers.value = response;
    } else if (response && Array.isArray(response.results)) {
      // Nếu API trả về dạng {results: [...]}
      customers.value = response.results;
    } else {
      console.error("Invalid response format:", response);
      customers.value = [];
    }
  } catch (error) {
    console.error("Error fetching customers:", error);
    customers.value = [];
    ElMessage.error("Lấy danh sách khách hàng thất bại");
  } finally {
    loading.value = false;
  }
};

// Lọc dữ liệu
const filteredCustomers = computed(() => {
  if (!Array.isArray(customers.value)) {
    console.warn("customers.value is not an array:", customers.value);
    return [];
  }
  return customers.value.filter((customer) => {
    if (!customer) return false;

    const keywordMatch =
      !filters.keyword ||
      (customer.name &&
        customer.name.toLowerCase().includes(filters.keyword.toLowerCase())) ||
      (customer.email &&
        customer.email.toLowerCase().includes(filters.keyword.toLowerCase())) ||
      (customer.phone && customer.phone.includes(filters.keyword));

    const areaMatch = !filters.area || customer.area === filters.area;

    return keywordMatch && areaMatch;
  });
});

// Phân trang
const paginatedCustomers = computed(() => {
  const start = (pagination.currentPage - 1) * pagination.pageSize;
  return filteredCustomers.value.slice(start, start + pagination.pageSize);
});

// Xử lý sự kiện
const handleSearch = () => {
  pagination.currentPage = 1;
};

const resetFilters = () => {
  filters.keyword = "";
  filters.area = "";
  pagination.currentPage = 1;
};

const handleSizeChange = (size) => {
  pagination.pageSize = size;
  pagination.currentPage = 1;
};

const handleCurrentChange = (page) => {
  pagination.currentPage = page;
};

const handleDelete = async (id) => {
  try {
    await ElMessageBox.confirm(
      "Bạn có chắc chắn muốn xóa khách hàng này?",
      "Xác nhận xóa",
      {
        type: "warning",
      }
    );

    await customerService.deleteCustomer(id);
    ElMessage.success("Xóa khách hàng thành công");
    fetchCustomers();
  } catch (error) {
    if (error !== "cancel") {
      console.error(error);
      ElMessage.error("Xóa khách hàng thất bại");
    }
  }
};

onMounted(() => {
  fetchCustomers();
});
</script>
