<template>
  <div class="about-page">
    <section class="stripe white">
      <div class="container">
        <div class="content-header">
          <h2 class="section-title">{{ t("orders_page_title") }}</h2>
          <p class="section-subtitle">{{ t("orders_page_subtitle") }}</p>
        </div>

        <!-- Tabs -->
        <div class="tabs-container">
          <div class="tabs">
            <button
              v-for="tab in tabs"
              :key="tab.status"
              @click="activeTab = tab.status"
              :class="['tab-button', { active: activeTab === tab.status }]"
            >
              {{ tab.name }}
              <span
                v-if="getOrderCountByStatus(tab.status) > 0"
                class="tab-badge"
              >
                {{ getOrderCountByStatus(tab.status) }}
              </span>
            </button>
          </div>
        </div>

        <div class="search-container">
          <div class="search-wrapper">
            <div class="search-input-group">
              <div class="search-icon">🔍</div>
              <input
                type="text"
                v-model="searchQuery"
                :placeholder="t('search_orders_placeholder')"
                class="search-input"
                @input="handleSearch"
              />
              <button
                v-if="searchQuery"
                @click="clearSearch"
                class="clear-search-btn"
                title="Xóa tìm kiếm"
              >
                ✕
              </button>
            </div>
          </div>
          <div
            v-if="
              searchQuery &&
              filteredAndSearchedOrders.length !== filteredOrders.length
            "
            class="search-results-info"
          >
            {{
              t("search_results_found", {
                count: filteredAndSearchedOrders.length,
              })
            }}
          </div>
        </div>

        <div v-if="loading" class="loading-state">
          <div class="loading-text">{{ t("orders_loading") }}</div>
        </div>

        <div v-else class="content-body">
          <div v-if="error" class="error-message">{{ error }}</div>

          <div
            v-if="filteredAndSearchedOrders.length"
            class="orders-table-wrapper"
          >
            <table class="orders-table">
              <thead>
                <tr>
                  <th>{{ t("orders_table_service") }}</th>
                  <th>{{ t("orders_table_area") }}</th>
                  <th>{{ t("orders_table_start_time") }}</th>
                  <th>{{ t("orders_table_end_time") }}</th>
                  <th>{{ t("orders_table_estimated_price") }}</th>
                  <th>{{ t("orders_table_status") }}</th>
                  <th>{{ t("orders_table_note") }}</th>
                  <th>{{ t("orders_table_created_at") || "Thời gian tạo" }}</th>
                  <th>{{ t("orders_table_actions") }}</th>
                  <th
                    v-if="activeTab === 'completed' || activeTab === 'rejected'"
                  >
                    {{
                      activeTab === "completed"
                        ? t("orders_table_feedback")
                        : t("orders_table_reject_reason")
                    }}
                  </th>
                </tr>
              </thead>
              <tbody>
                <template v-for="order in paginatedOrders" :key="order.id">
                  <tr class="order-row">
                    <td>{{ order.service_details?.name }}</td>
                    <td>{{ formatArea(order.area_m2) }}</td>
                    <td>{{ formatDateTime(order.preferred_start_time) }}</td>
                    <td>{{ formatDateTime(order.preferred_end_time) }}</td>
                    <td>
                      {{
                        order.cost_confirm
                          ? formatPrice(order.cost_confirm)
                          : t("orders_price_tbd")
                      }}
                    </td>
                    <td>
                      <span
                        :class="['status-badge', getStatusClass(order.status)]"
                        >{{ getStatusText(order.status) }}</span
                      >
                    </td>
                    <td>{{ order.note || t("orders_note_none") }}</td>
                    <td>{{ formatDateTime(order.created_at) }}</td>
                    <td>
                      <div class="action-buttons">
                        <!-- Edit button for pending orders -->
                        <RouterLink
                          v-if="order.status === 'pending'"
                          :to="`/dss/customer-orders/edit/${order.id}`"
                          class="action-btn edit-order"
                          :title="t('orders_action_edit')"
                        >
                          {{ t("orders_action_edit") }}
                        </RouterLink>

                        <!-- Invoice button for non-rejected orders -->
                        <button
                          v-if="order.status !== 'rejected'"
                          @click="viewInvoice(order)"
                          class="action-btn view-invoice"
                          :title="t('orders_action_invoice')"
                        >
                          {{ t("orders_action_invoice") }}
                        </button>

                        <span
                          v-if="order.status === 'rejected'"
                          class="no-actions-text"
                          >-</span
                        >
                      </div>
                    </td>
                    <!-- Cột feedback/admin log cho completed và rejected -->
                    <td
                      v-if="
                        activeTab === 'completed' || activeTab === 'rejected'
                      "
                    >
                      <button
                        @click="toggleOrderExpanded(order.id)"
                        class="action-btn"
                        :class="
                          activeTab === 'completed'
                            ? 'show-feedback'
                            : 'show-reject'
                        "
                      >
                        {{
                          expandedOrders.has(order.id)
                            ? activeTab === "completed"
                              ? t("orders_action_hide_feedback")
                              : t("orders_action_hide_reason")
                            : activeTab === "completed"
                            ? t("orders_action_show_feedback")
                            : t("orders_action_show_reason")
                        }}
                      </button>
                    </td>
                  </tr>

                  <!-- Expanded row cho feedback/admin log -->
                  <tr
                    v-if="
                      (activeTab === 'completed' || activeTab === 'rejected') &&
                      expandedOrders.has(order.id)
                    "
                    class="expanded-row"
                  >
                    <td
                      :colspan="
                        activeTab === 'completed' || activeTab === 'rejected'
                          ? 10
                          : 9
                      "
                      class="expanded-content"
                    >
                      <!-- Customer Feedback cho completed -->
                      <div
                        v-if="activeTab === 'completed'"
                        class="feedback-content"
                      >
                        <h4 class="expanded-title">
                          {{
                            t("orders_feedback_title", {
                              serviceName: order.service_details?.name,
                            })
                          }}
                        </h4>
                        <div
                          v-if="order.customer_feedback"
                          class="existing-feedback"
                        >
                          <div class="feedback-label">
                            {{ t("orders_feedback_label") }}
                          </div>
                          <div class="feedback-text">
                            {{ order.customer_feedback }}
                          </div>
                        </div>
                        <div v-else class="feedback-input-section">
                          <div class="feedback-label">
                            {{ t("orders_feedback_input_label") }}
                          </div>
                          <textarea
                            v-model="feedbackInputs[order.id]"
                            :placeholder="t('orders_feedback_placeholder')"
                            class="feedback-textarea"
                            rows="3"
                          ></textarea>
                          <button
                            @click="submitFeedback(order.id)"
                            class="submit-feedback-btn"
                            :disabled="!feedbackInputs[order.id]?.trim()"
                          >
                            {{ t("orders_feedback_submit") }}
                          </button>
                        </div>
                      </div>

                      <!-- Admin Log cho rejected -->
                      <div
                        v-else-if="activeTab === 'rejected'"
                        class="admin-log-content"
                      >
                        <h4 class="expanded-title">
                          {{
                            t("orders_reject_title", {
                              serviceName: order.service_details?.name,
                            })
                          }}
                        </h4>
                        <div v-if="order.admin_log" class="admin-log">
                          <div class="admin-log-label">
                            {{ t("orders_reject_label") }}
                          </div>
                          <div class="admin-log-text">
                            {{ order.admin_log }}
                          </div>
                        </div>
                        <div v-else class="no-admin-log">
                          <em>{{ t("orders_reject_none") }}</em>
                        </div>
                      </div>
                    </td>
                  </tr>
                </template>
              </tbody>
            </table>

            <!-- Pagination -->
            <div v-if="totalPages > 1" class="pagination-wrapper">
              <div class="pagination-info">
                {{ t("pagination_showing") }}
                {{ (currentPage - 1) * itemsPerPage + 1 }} -
                {{
                  Math.min(
                    currentPage * itemsPerPage,
                    filteredAndSearchedOrders.length
                  )
                }}
                {{ t("pagination_of") }} {{ filteredAndSearchedOrders.length }}
                {{ t("pagination_results") }}
              </div>
              <div class="pagination-controls">
                <button
                  @click="currentPage = currentPage - 1"
                  :disabled="currentPage <= 1"
                  class="pagination-btn"
                >
                  {{ t("pagination_previous") }}
                </button>

                <span v-for="page in totalPages" :key="page">
                  <button
                    @click="currentPage = page"
                    :class="[
                      'pagination-btn',
                      { active: currentPage === page },
                    ]"
                  >
                    {{ page }}
                  </button>
                </span>

                <button
                  @click="currentPage = currentPage + 1"
                  :disabled="currentPage >= totalPages"
                  class="pagination-btn"
                >
                  {{ t("pagination_next") }}
                </button>
              </div>
            </div>
          </div>

          <div v-else class="empty-state">
            <p>{{ getEmptyMessage() }}</p>
            <RouterLink to="/dss/orders/create" class="featured-cta">{{
              t("orders_empty_cta")
            }}</RouterLink>
          </div>
        </div>
      </div>
    </section>

    <!-- Modal Hóa đơn -->
    <div
      v-if="showInvoiceModal && selectedInvoice"
      class="modal-overlay"
      @click="closeInvoiceModal"
    >
      <div class="modal-content invoice-modal" @click.stop>
        <div class="modal-header">
          <h2>{{ t("invoice_title") }}</h2>
          <button class="close-btn" @click="closeInvoiceModal">×</button>
        </div>

        <div class="modal-body">
          <div class="invoice-header">
            <div class="invoice-title">{{ t("invoice_header_title") }}</div>
            <div class="invoice-number">
              {{
                t("invoice_number", { number: selectedInvoice.invoiceNumber })
              }}
            </div>
            <!-- <div class="invoice-date">
              <div>{{ t('invoice_issue_date', { date: selectedInvoice.issueDate }) }}</div>
              <div>{{ t('invoice_due_date', { date: selectedInvoice.dueDate }) }}</div>
            </div> -->
          </div>

          <div class="invoice-section">
            <h4>{{ t("invoice_service_details") }}</h4>
            <div class="service-details">
              <div class="info-row">
                <span>{{ t("invoice_service") }}</span>
                <span>{{ selectedInvoice.orderInfo.serviceName }}</span>
              </div>
              <div class="info-row">
                <span>{{ t("invoice_area") }}</span>
                <span>{{ selectedInvoice.orderInfo.area }} m²</span>
              </div>
              <div class="info-row">
                <span>{{ t("invoice_start_time") }}</span>
                <span>{{
                  formatDateTime(selectedInvoice.orderInfo.startTime)
                }}</span>
              </div>
              <div class="info-row">
                <span>{{ t("invoice_end_time") }}</span>
                <span>{{
                  formatDateTime(selectedInvoice.orderInfo.endTime)
                }}</span>
              </div>
              <div class="info-row">
                <span>{{ t("invoice_payment_method") }}</span>
                <span>{{ selectedInvoice.orderInfo.paymentMethod }}</span>
              </div>
              <div
                v-if="selectedInvoice.orderInfo.note !== t('orders_note_none')"
                class="info-row"
              >
                <span>{{ t("invoice_note") }}</span>
                <span>{{ selectedInvoice.orderInfo.note }}</span>
              </div>
            </div>
          </div>

          <div class="invoice-section">
            <h4>{{ t("invoice_payment_title") }}</h4>
            <div class="pricing-details">
              <div class="info-row">
                <span>{{ t("invoice_subtotal") }}</span>
                <span
                  >{{
                    selectedInvoice.pricing.subtotal.toLocaleString("vi-VN")
                  }}
                  VNĐ</span
                >
              </div>
              <div class="info-row">
                <span>{{ t("invoice_tax") }}</span>
                <span
                  >{{
                    selectedInvoice.pricing.tax.toLocaleString("vi-VN")
                  }}
                  VNĐ</span
                >
              </div>
              <div class="total-amount">
                <span
                  ><strong>{{ t("invoice_total") }}</strong></span
                >
                <span class="total-price"
                  ><strong
                    >{{
                      selectedInvoice.pricing.total.toLocaleString("vi-VN")
                    }}
                    VNĐ</strong
                  ></span
                >
              </div>
            </div>
          </div>
        </div>

        <div class="modal-footer">
          <button class="btn-download" @click="downloadInvoice">
            {{ t("invoice_download") }}
          </button>
          <button class="btn-close" @click="closeInvoiceModal">
            {{ t("invoice_close") }}
          </button>
        </div>
      </div>
    </div>

    <!-- Toast Notification -->
    <div v-if="showToast" :class="['toast-notification', toastType]">
      {{ toastMessage }}
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from "vue";
import { useI18n } from "vue-i18n";
import CustomerOrderService from "@/services/dss/users/customer";
import "@/assets/css/customer.css";

// Apply role-based middleware
definePageMeta({
  middleware: "role-based",
});

const { t } = useI18n();

const orders = ref([]);
const loading = ref(false);
const error = ref("");
const activeTab = ref("pending");

// Modal hóa đơn
const showInvoiceModal = ref(false);
const selectedInvoice = ref(null);

// Feedback inputs cho completed orders
const feedbackInputs = ref({});

// Toast notification
const showToast = ref(false);
const toastMessage = ref("");
const toastType = ref("success"); // 'success' hoặc 'error'

// Expanded orders for feedback/admin log
const expandedOrders = ref(new Set());

// Pagination
const itemsPerPage = 5;
const currentPage = ref(1);

// Search functionality
const searchQuery = ref("");

// Computed property for filtered and searched orders
const filteredAndSearchedOrders = computed(() => {
  let filtered = orders.value.filter(
    (order) => order.status === activeTab.value
  );

  if (!searchQuery.value.trim()) {
    return filtered;
  }

  const query = searchQuery.value.toLowerCase().trim();

  return filtered.filter((order) => {
    return (
      order.service_details?.name?.toLowerCase().includes(query) ||
      order.id?.toLowerCase().includes(query) ||
      order.note?.toLowerCase().includes(query) ||
      order.cost_confirm?.toString().includes(query) ||
      order.area_m2?.toString().includes(query)
    );
  });
});

// Computed property for paginated orders (updated to use search results)
const paginatedOrders = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  const end = start + itemsPerPage;
  return filteredAndSearchedOrders.value.slice(start, end);
});

// Computed property for total pages (updated to use search results)
const totalPages = computed(() => {
  return Math.ceil(filteredAndSearchedOrders.value.length / itemsPerPage);
});

// Watch for tab changes to reset pagination
watch(activeTab, () => {
  currentPage.value = 1;
});

// Watch for search changes to reset pagination
watch(searchQuery, () => {
  currentPage.value = 1;
});

// Tabs configuration
const tabs = computed(() => [
  { status: "pending", name: t("orders_tab_pending") },
  { status: "confirmed", name: t("orders_tab_confirmed") },
  { status: "in_progress", name: t("orders_tab_in_progress") },
  { status: "completed", name: t("orders_tab_completed") },
  { status: "rejected", name: t("orders_tab_rejected") },
]);

// Computed property to filter orders by active tab
const filteredOrders = computed(() => {
  return orders.value.filter((order) => order.status === activeTab.value);
});

// Get order count by status
const getOrderCountByStatus = (status) => {
  return orders.value.filter((order) => order.status === status).length;
};

// Get status display text
const getStatusText = (status) => {
  const statusMap = {
    pending: t("orders_status_pending"),
    confirmed: t("orders_status_confirmed"),
    rejected: t("orders_status_rejected"),
    in_progress: t("orders_status_in_progress"),
    completed: t("orders_status_completed"),
  };
  return statusMap[status] || status;
};

// Get status CSS class
const getStatusClass = (status) => {
  const classMap = {
    pending: "status-pending",
    confirmed: "status-confirmed",
    rejected: "status-rejected",
    in_progress: "status-in-progress",
    completed: "status-completed",
  };
  return classMap[status] || "";
};

// Get empty message based on active tab
const getEmptyMessage = () => {
  const messageMap = {
    pending: t("orders_empty_pending"),
    confirmed: t("orders_empty_confirmed"),
    rejected: t("orders_empty_rejected"),
    in_progress: t("orders_empty_in_progress"),
    completed: t("orders_empty_completed"),
  };
  return messageMap[activeTab.value] || t("orders_empty_pending");
};

const formatDateTime = (datetime) => {
  return datetime ? new Date(datetime).toLocaleString() : "";
};

const formatPrice = (price) => {
  return new Intl.NumberFormat("vi-VN", {
    style: "currency",
    currency: "VND",
  }).format(price);
};

// Hàm format diện tích để hiển thị số nguyên khi không có phần thập phân
const formatArea = (area) => {
  if (!area && area !== 0) return "";
  const num = parseFloat(area);
  return num % 1 === 0 ? num.toString() : num.toString();
};

const fetchOrders = async () => {
  loading.value = true;
  error.value = "";
  try {
    const res = await CustomerOrderService.getOrders();
    console.log("API Response:", res);
    console.log("Type of response:", typeof res);

    // Xử lý nhiều format response khác nhau
    let ordersData = [];
    if (Array.isArray(res)) {
      ordersData = res;
    } else if (res.results && Array.isArray(res.results)) {
      ordersData = res.results;
    } else if (res.data && Array.isArray(res.data)) {
      ordersData = res.data;
    } else {
      console.warn("Unexpected response format:", res);
      ordersData = [];
    }

    orders.value = ordersData;
    console.log("Orders after processing:", orders.value);
    console.log("Orders length:", orders.value.length);
  } catch (e) {
    console.error("Error fetching orders:", e);
    error.value = "Không thể tải danh sách đơn hàng: " + e.message;
  } finally {
    loading.value = false;
  }
};

// Phương thức gửi feedback cho completed orders
const submitFeedback = async (orderId) => {
  const feedback = feedbackInputs.value[orderId]?.trim();
  if (!feedback) return;

  try {
    // Gọi API để cập nhật feedback
    await CustomerOrderService.updateOrderFeedback(orderId, feedback);

    // Cập nhật local data
    const order = orders.value.find((o) => o.id === orderId);
    if (order) {
      order.customer_feedback = feedback;
    }

    // Clear input
    feedbackInputs.value[orderId] = "";

    // Hiển thị thông báo thành công
    showToastMessage(t("orders_feedback_success"), "success");
  } catch (e) {
    console.error("Error submitting feedback:", e);
    showToastMessage(t("orders_feedback_error"), "error");
  }
};

// Hiển thị toast notification
const showToastMessage = (message, type = "success") => {
  toastMessage.value = message;
  toastType.value = type;
  showToast.value = true;

  // Tự động ẩn sau 3 giây
  setTimeout(() => {
    showToast.value = false;
  }, 3000);
};

// Toggle expanded state cho order
const toggleOrderExpanded = (orderId) => {
  if (expandedOrders.value.has(orderId)) {
    expandedOrders.value.delete(orderId);
  } else {
    expandedOrders.value.add(orderId);
  }
};

// Hàm xem hóa đơn
const viewInvoice = (order) => {
  const currentDate = new Date(order.created_at || new Date());
  // Sử dụng ID của đơn hàng làm invoiceNumber trực tiếp
  const invoiceNumber = order.id;

  // cost_confirm đã bao gồm VAT, cần tính ngược lại để lấy giá gốc
  const totalPrice = parseInt(order.cost_confirm) || 0;
  const subtotal = Math.round(totalPrice / 1.1); // Giá gốc (không bao gồm VAT)
  const tax = totalPrice - subtotal; // VAT = 10% của giá gốc

  selectedInvoice.value = {
    invoiceNumber,
    orderInfo: {
      serviceName: order.service_details?.name || "N/A",
      area: formatArea(order.area_m2),
      startTime: order.preferred_start_time,
      endTime: order.preferred_end_time,
      note: order.note || t("orders_note_none"),
      paymentMethod: t("payment_cash"),
    },
    pricing: {
      subtotal: subtotal,
      tax: tax,
      total: totalPrice,
    },
    // ueDate: currissentDate.toLocaleDateString('vi-VN'),
    // dueDate: new Date(currentDate.getTime() + 7 * 24 * 60 * 60 * 1000).toLocaleDateString('vi-VN')
  };

  showInvoiceModal.value = true;
};

const closeInvoiceModal = () => {
  showInvoiceModal.value = false;
  selectedInvoice.value = null;
};

const downloadInvoice = () => {
  if (!selectedInvoice.value) return;

  const invoice = selectedInvoice.value;
  const htmlContent = `
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <title>${t("invoice_title")} ${invoice.invoiceNumber}</title>
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
        <div class="title">${t("invoice_header_title")}</div>
        <div class="invoice-number">${t("invoice_number", {
          number: invoice.invoiceNumber,
        })}</div>
        <div>${t("invoice_issue_date", { date: invoice.issueDate })} | ${t(
    "invoice_due_date",
    { date: invoice.dueDate }
  )}</div>
      </div>
      
      <div class="section">
        <h3>${t("invoice_service_details")}</h3>
        <div class="row"><span>${t("invoice_service")}</span><span>${
    invoice.orderInfo.serviceName
  }</span></div>
        <div class="row"><span>${t("invoice_area")}</span><span>${
    invoice.orderInfo.area
  } m²</span></div>
        <div class="row"><span>${t(
          "invoice_start_time"
        )}</span><span>${formatDateTime(
    invoice.orderInfo.startTime
  )}</span></div>
        <div class="row"><span>${t(
          "invoice_end_time"
        )}</span><span>${formatDateTime(invoice.orderInfo.endTime)}</span></div>
        <div class="row"><span>${t("invoice_payment_method")}</span><span>${
    invoice.orderInfo.paymentMethod
  }</span></div>
        ${
          invoice.orderInfo.note !== t("orders_note_none")
            ? `<div class="row"><span>${t("invoice_note")}</span><span>${
                invoice.orderInfo.note
              }</span></div>`
            : ""
        }
      </div>
      
      <div class="section">
        <h3>${t("invoice_payment_title")}</h3>
        <div class="row"><span>${t(
          "invoice_subtotal"
        )}</span><span>${invoice.pricing.subtotal.toLocaleString(
    "vi-VN"
  )} VNĐ</span></div>
        <div class="row"><span>${t(
          "invoice_tax"
        )}</span><span>${invoice.pricing.tax.toLocaleString(
    "vi-VN"
  )} VNĐ</span></div>
        <div class="total"><span>${t(
          "invoice_total"
        )}</span><span>${invoice.pricing.total.toLocaleString(
    "vi-VN"
  )} VNĐ</span></div>
      </div>
      
      <div style="text-align: center; margin-top: 30px; color: #666;">
        Cảm ơn bạn đã sử dụng dịch vụ!
      </div>
    </body>
    </html>
  `;

  const printWindow = window.open("", "_blank");
  if (printWindow) {
    printWindow.document.write(htmlContent);
    printWindow.document.close();
    printWindow.focus();
    printWindow.print();
    printWindow.onafterprint = () => printWindow.close();
  }
};

// Search functions
const handleSearch = () => {
  // Search được xử lý tự động qua computed property
  // Function này có thể dùng để thêm debounce sau này
};

const clearSearch = () => {
  searchQuery.value = "";
};

onMounted(fetchOrders);
</script>

<style scoped>
/* Search Container */
.search-container {
  margin: 20px 0;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
  border: 1px solid #e9ecef;
}

.search-wrapper {
  display: flex;
  gap: 15px;
  align-items: center;
  justify-content: center;
}

.search-input-group {
  position: relative;
  flex: 1;
  max-width: 500px;
  display: flex;
  align-items: center;
}

.search-icon {
  position: absolute;
  left: 12px;
  color: #6c757d;
  font-size: 16px;
  z-index: 1;
}

.search-input {
  width: 100%;
  padding: 12px 12px 12px 40px;
  border: 2px solid #dee2e6;
  border-radius: 8px;
  font-size: 14px;
  transition: all 0.3s ease;
  background: white;
}

.search-input:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.1);
}

.clear-search-btn {
  position: absolute;
  right: 8px;
  background: none;
  border: none;
  font-size: 18px;
  color: #6c757d;
  cursor: pointer;
  padding: 4px;
  border-radius: 50%;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.clear-search-btn:hover {
  background: #e9ecef;
  color: #495057;
}

.search-results-info {
  margin-top: 10px;
  padding: 8px 12px;
  background: #d1ecf1;
  color: #0c5460;
  border-radius: 4px;
  font-size: 14px;
  border: 1px solid #bee5eb;
}

.pagination-wrapper {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 20px;
  padding: 15px 0;
  border-top: 1px solid #e0e0e0;
}

.pagination-info {
  font-size: 14px;
  color: #666;
}

.pagination-controls {
  display: flex;
  gap: 8px;
  align-items: center;
}

.pagination-btn {
  padding: 8px 12px;
  border: 1px solid #ddd;
  background: white;
  color: #333;
  cursor: pointer;
  border-radius: 4px;
  font-size: 14px;
  transition: all 0.2s ease;
}

.pagination-btn:hover:not(:disabled) {
  background: #f5f5f5;
  border-color: #bbb;
}

.pagination-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.pagination-btn.active {
  background: #007bff;
  color: white;
  border-color: #007bff;
}

.pagination-btn.active:hover {
  background: #0056b3;
  border-color: #0056b3;
}

.action-buttons {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  align-items: center;
}

.action-btn {
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
  text-decoration: none;
  display: inline-block;
  text-align: center;
  min-width: 60px;
}

.action-btn.edit-order {
  background: #28a745;
  color: white;
}

.action-btn.edit-order:hover {
  background: #218838;
}

.action-btn.view-invoice {
  background: #007bff;
  color: white;
}

.action-btn.view-invoice:hover {
  background: #0056b3;
}

.no-actions-text {
  color: #999;
  font-style: italic;
  font-size: 12px;
}

/* Responsive design for search */
@media (max-width: 768px) {
  .search-input-group {
    max-width: 100%;
  }
}
</style>
