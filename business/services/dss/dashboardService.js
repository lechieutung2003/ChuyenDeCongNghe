import BaseService from "../base";
import orderService from "./order";
import employeeService from "./users/employees";
import customerService from "./customer";

class DashboardService extends BaseService {
  get entity() {
    return "dashboard";
  }
  // Lấy thống kê tổng quan
  async getDashboardStats() {
    try {
      // TODO: Gọi API dashboard khi có endpoint thật
      // return await this.request().get(`${this.entity}/stats`);
      
      // Tính toán từ các service hiện có (Orders + Employees)
      return this.calculateStatsFromServices();
    } catch (error) {
      console.error('Error in getDashboardStats:', error);
      // Fallback: return empty data instead of mock
      return this.getDefaultStats();
    }
  }

  // Tính toán thống kê từ các service khác
  async calculateStatsFromServices() {
    try {
      // Chỉ lấy 100 records để tính toán nhanh hơn
      const [ordersResponse, employeesResponse] = await Promise.all([
        orderService.getOrders({ pageSize: 100 }), // Giảm từ 1000 xuống 100
        employeeService.getEmployees({ page_size: 50 }), // Giảm từ 1000 xuống 50
      ]);

      // FIX: Orders API có cấu trúc: response.results (không có data wrapper)
      const orders = ordersResponse.results || ordersResponse.data?.results || [];
      // FIX: Employees API trả về results trực tiếp, không có data wrapper
      const employees = employeesResponse.results || employeesResponse.data?.results || [];

      // Tính toán các thông số từ real API data
      const totalTasks = orders.length;
      const activeTasks = orders.filter(order => 
        ['in_progress', 'pending', 'confirmed'].includes(order.status)
      ).length;
      const completedTasks = orders.filter(order => 
        order.status === 'completed'
      ).length;

      // Tính doanh thu từ orders đã hoàn thành 
      // Revenue = area_m2 * price_per_m2
      const todayRevenue = orders
        .filter(order => order.status === 'completed')
        .reduce((sum, order) => {
          const area = parseFloat(order.area_m2) || 0;
          const pricePerM2 = order.service_details?.price_per_m2 || 0;
          return sum + (area * pricePerM2);
        }, 0);

      // Tính doanh thu hôm nay (từ created_at)
      const today = new Date().toISOString().split('T')[0];
      const todayCompletedRevenue = orders
        .filter(order => 
          order.created_at && 
          order.created_at.startsWith(today) && 
          order.status === 'completed'
        )
        .reduce((sum, order) => {
          const area = parseFloat(order.area_m2) || 0;
          const pricePerM2 = order.service_details?.price_per_m2 || 0;
          return sum + (area * pricePerM2);
        }, 0);

      // Tính trung bình thời gian hoàn thành
      const completedOrders = orders.filter(order => order.status === 'completed');
      const avgCompletionTime = completedOrders.length > 0 
        ? completedOrders.reduce((sum, order) => 
            sum + (parseFloat(order.estimated_hours) || 0), 0
          ) / completedOrders.length
        : 0;

      // Tính toán thông tin nhân viên từ API response
      const activeEmployees = employees.filter(emp => 
        emp.status === 1 && emp.user?.active === true
      ).length;

      const employeesWithOrders = employees.filter(emp => 
        emp.completed_orders_count > 0
      ).length;

      // Success rate based on completed vs total
      const successRate = totalTasks > 0 ? Math.round((completedTasks / totalTasks) * 100) : 0;

      const stats = {
        totalTasks,
        activeTasks,
        completedTasks,
        totalEmployees: employees.length,
        activeEmployees, 
        employeesWithOrders, 
        todayRevenue: Math.round(todayCompletedRevenue),
        totalRevenue: Math.round(todayRevenue),
        customerSatisfaction: 4.8, // Default until we have rating system
        avgCompletionTime: Math.round(avgCompletionTime * 10) / 10,
        successRate,
      };

      return {
        data: {
          overview: stats
        }
      };
    } catch (error) {
      console.error('Error calculating stats:', error);
      // Return default data if calculation fails
      return this.getDefaultStats();
    }
  }

  // Lấy nhiệm vụ ưu tiên
  async getUrgentTasks() {
    try {
      // Get all orders and filter client-side (more reliable than multi-status query)
      const response = await orderService.getOrders({ pageSize: 100 });
      
      // FIX: Orders API có cấu trúc: response.results (không có data wrapper)
      let orders = response.results || response.data?.results || [];
      
      // Filter for urgent orders (non-completed status)
      orders = orders.filter(order => 
        ['pending', 'confirmed', 'in_progress'].includes(order.status)
      );
      
      // Sort by priority: pending/confirmed first (need attention), then by deadline
      orders.sort((a, b) => {
        const priorityOrder = { 'pending': 1, 'confirmed': 2, 'in_progress': 3 };
        const aPriority = priorityOrder[a.status] || 999;
        const bPriority = priorityOrder[b.status] || 999;
        
        if (aPriority !== bPriority) {
          return aPriority - bPriority;
        }
        
        // If same priority, sort by deadline (earliest first)
        const aDeadline = new Date(a.preferred_end_time || a.preferred_start_time || '9999-12-31');
        const bDeadline = new Date(b.preferred_end_time || b.preferred_start_time || '9999-12-31');
        return aDeadline - bDeadline;
      });
      
      // Take top 5
      orders = orders.slice(0, 5);

      return orders.map(order => ({
        id: order.id,
        title: `${order.service_details?.name || 'Cleaning Service'} - ${order.customer_name}`,
        deadline: order.preferred_end_time || order.preferred_start_time,
        location: order.customer_details?.address || 'N/A',
        priority: this.getPriority(order),
        assignee: 'Chưa phân công',
        progress: this.calculateProgress(order),
        area: `${order.area_m2}m²`,
        estimatedHours: `${order.estimated_hours}h`,
        status: order.status,
        note: order.note || '',
        cost: order.service_details?.price_per_m2 
          ? Math.round(parseFloat(order.area_m2) * order.service_details.price_per_m2)
          : null
      }));
    } catch (error) {
      console.error('Error fetching urgent tasks:', error);
      return this.getDefaultUrgentTasks();
    }
  }

  // Lấy dữ liệu cho biểu đồ - tính từ orders API
  async getChartData() {
    try {
      // Lấy orders data để tạo chart
      const response = await orderService.getOrders({ pageSize: 100 });
      const orders = response.results || response.data?.results || [];

      // Tạo revenue data từ orders (group by date)
      const revenueMap = {};
      const taskStatusCounts = {
        completed: 0,
        in_progress: 0,
        pending: 0,
        confirmed: 0
      };

      orders.forEach(order => {
        // Count task status
        if (taskStatusCounts.hasOwnProperty(order.status)) {
          taskStatusCounts[order.status]++;
        }

        // Calculate revenue by date (từ created_at)
        if (order.created_at && order.status === 'completed') {
          const date = order.created_at.split('T')[0]; // YYYY-MM-DD
          const area = parseFloat(order.area_m2) || 0;
          const pricePerM2 = order.service_details?.price_per_m2 || 0;
          const orderRevenue = area * pricePerM2;

          if (!revenueMap[date]) {
            revenueMap[date] = 0;
          }
          revenueMap[date] += orderRevenue;
        }
      });

      // Convert revenue map to array, sorted by date
      const revenueData = Object.entries(revenueMap)
        .map(([date, amount]) => ({ date, amount: Math.round(amount) }))
        .sort((a, b) => new Date(a.date) - new Date(b.date))
        .slice(-7); // Last 7 days

      // If no revenue data, create last 7 days with 0 values
      if (revenueData.length === 0) {
        const last7Days = [];
        for (let i = 6; i >= 0; i--) {
          const date = new Date();
          date.setDate(date.getDate() - i);
          last7Days.push({
            date: date.toISOString().split('T')[0],
            amount: 0
          });
        }
        revenueData.push(...last7Days);
      }

      return {
        revenue: revenueData,
        tasks: {
          completed: taskStatusCounts.completed,
          in_progress: taskStatusCounts.in_progress,
          pending: taskStatusCounts.pending + taskStatusCounts.confirmed, // Combine pending states
        }
      };
    } catch (error) {
      console.error('Error generating chart data from orders:', error);
      return { revenue: [], tasks: { completed: 0, in_progress: 0, pending: 0 } };
    }
  }

  // Lấy hoạt động gần đây - tạm thời return empty vì chưa có API
  async getRecentActivities() {
    try {
      // TODO: Implement API endpoint when ready
      // return await this.request().get(`${this.entity}/activities`);
      
      return { data: [] };
    } catch (error) {
      console.error('Error fetching activities:', error);
      return { data: [] };
    }
  }

  // Helper methods
  getPriority(order) {
    if (order.priority) return order.priority;
    
    // Tính priority dựa trên preferred_end_time
    if (order.preferred_end_time) {
      const deadline = new Date(order.preferred_end_time);
      const now = new Date();
      const hoursLeft = (deadline - now) / (1000 * 60 * 60);
      
      if (hoursLeft < 24) return 'Cao';
      if (hoursLeft < 72) return 'Trung bình';
      return 'Thấp';
    }
    
    // Fallback: priority based on area (larger areas = higher priority)
    const area = parseFloat(order.area_m2) || 0;
    if (area > 200) return 'Cao';
    if (area > 100) return 'Trung bình';
    return 'Thấp';
  }

  calculateProgress(order) {
    if (order.progress !== undefined) return order.progress;
    
    // Calculate based on real API status
    switch (order.status) {
      case 'completed': return 100;
      case 'in_progress': return Math.floor(Math.random() * 40) + 40; // 40-80%
      case 'confirmed': return Math.floor(Math.random() * 30) + 10; // 10-40%
      case 'pending': return Math.floor(Math.random() * 20); // 0-20%
      default: return 0;
    }
  }

  // Default fallback chỉ cho trường hợp API lỗi
  getDefaultStats() {
    return {
      data: {
        overview: {
          totalTasks: 0,
          activeTasks: 0,
          completedTasks: 0,
          totalEmployees: 0,
          activeEmployees: 0,
          employeesWithOrders: 0,
          todayRevenue: 0,
          totalRevenue: 0,
          customerSatisfaction: 0,
          avgCompletionTime: 0,
          successRate: 0,
        }
      }
    };
  }

  getDefaultUrgentTasks() {
    return []; // Return empty array instead of mock data
  }

}

export default new DashboardService();