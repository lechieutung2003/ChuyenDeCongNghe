from datetime import datetime, timedelta
from hr.models import EmployeeSkill, Skill
from ..models import employee
from hr.models import order
from django.db import models
from hr.models import Customer, ServiceType
from decimal import Decimal

class RecommendationService:
    @staticmethod
    def calculate_match_score(employee, order):
        print("================================")
        print(f"Calculating match score for employee: {employee.first_name}")
        print(f"Order details: {order}")
        
        score = 0

        # 1. Kiểm tra thời gian làm việc (30%)
        if RecommendationService.check_time_availability(employee, order):
            score += 30
        
        print(f"After time check: {score}")

        # 2. Kiểm tra khu vực (15%)
        order_area = None
        if hasattr(order, 'customer') and order.customer:
            order_area = getattr(order.customer, 'area', None)
        elif hasattr(order, 'customer_details') and order.customer_details:
            order_area = order.customer_details.get('area', None)

        if order_area and employee.area == order_area:
            score += 15
        
        print(f"After area check: {score}")

        # 3. Kiểm tra kỹ năng phù hợp (15%)
        required_skills = []
        if hasattr(order, 'service_type_id') and order.service_type_id:
            try:
                service_type = ServiceType.objects.get(id=order.service_type_id)
                if hasattr(service_type, 'name') and service_type.name:
                    required_skills = [service_type.name]
            except Exception as e:
                print(f"Error getting service type: {e}")
        
        employee_skills = []
        employee_skill_records = EmployeeSkill.objects.filter(employee=employee)
        if employee_skill_records:
            employee_skills = [es.skill.name for es in employee_skill_records]
            
        print("required_skills:", required_skills)
        print("employee_skills:", employee_skills)
        
        if required_skills and employee_skills:
            # Tìm kiếm từ khóa thay vì so khớp chính xác
            skill_match = False
            for req_skill in required_skills:
                # Tách từ khóa chính từ tên kỹ năng
                keywords = req_skill.lower().split()
                for emp_skill in employee_skills:
                    emp_skill_lower = emp_skill.lower()
                    # Kiểm tra từng từ khóa
                    for keyword in keywords:
                        if len(keyword) > 3 and keyword in emp_skill_lower:  # Chỉ kiểm tra từ khóa có ít nhất 4 ký tự
                            skill_match = True
                            break
                    if skill_match:
                        break
                if skill_match:
                    break
            
            if skill_match:
                score += 15
                print(f"Skill match found: {req_skill} matches with {emp_skill}")
            else:
                print(f"No skill match found between {required_skills} and {employee_skills}")
        
        print(f"After skill check: {score}")
        
        # 4. Kiểm tra mức lương (30%) - Nhân viên có mức lương thấp hơn được ưu tiên
        try:
            # Lấy mức lương của nhân viên
            employee_salary = getattr(employee, 'salary', 0) or 0
            
            # Lấy ra mức lương cao nhất và thấp nhất từ tất cả nhân viên
            from ..models.employee import Employee
            max_salary = Employee.objects.all().aggregate(max_salary=models.Max('salary'))['max_salary'] or 1
            min_salary = Employee.objects.all().aggregate(min_salary=models.Min('salary'))['min_salary'] or 0
            
            salary_range = max_salary - min_salary
            
            print("employee_salary:", employee_salary)
            print("max_salary:", max_salary)
            print("min_salary:", min_salary)
            
            # Tính điểm ngược: càng thấp lương thì điểm càng cao
            if salary_range > 0:  # Tránh chia cho 0
                # Công thức: 30 * (1 - (lương nhân viên - lương thấp nhất) / (lương cao nhất - lương thấp nhất))
                normalized_salary = (employee_salary - min_salary) / salary_range
                salary_score = round(30 * (1 - normalized_salary), 2)
                score += salary_score
                print("salary_score:", salary_score)
            else:
                # Nếu tất cả nhân viên có cùng mức lương
                score += 0  # 50% của 30 điểm
                print("salary_score (default):", 15)
        except Exception as e:
            print("Error calculating salary score:", e)
            score += 0  # 50% của 30 điểm

        # 5. Kiểm tra khối lượng công việc (10%)
        try:
            employee_completed_orders = int(getattr(employee, 'completed_orders_count', 0) or 0)
    
            from ..models.employee import Employee
            max_completed_orders = Employee.objects.all().order_by('-completed_orders_count').first()
            max_value = int(max_completed_orders.completed_orders_count if max_completed_orders else 0)
            
            if max_value > 0:
                normalized_score = 1 - (employee_completed_orders / max_value)
                experience_score = round(10 * normalized_score, 2)
                # Chuyển đổi thành Decimal trước khi cộng
                score += Decimal(str(experience_score))
            else:
                score += Decimal('0')
        except Exception as e:
            print("Error calculating workload score:", e)
            score += 0

        print("Final score:", score)
            
        return score

    @staticmethod
    def get_match_reasons(employee, order):
        reasons = []
        
        if RecommendationService.check_time_availability(employee, order):
            reasons.append("Có thể làm việc trong thời gian yêu cầu")
        
        # Lấy khu vực từ customer
        order_area = None
        if hasattr(order, 'customer') and order.customer:
            order_area = getattr(order.customer, 'area', None)
        elif hasattr(order, 'customer_details') and order.customer_details:
            order_area = order.customer_details.get('area', None)
        
        if order_area and employee.area == order_area:
            reasons.append("Làm việc trong cùng khu vực")
        
        # Kiểm tra kỹ năng
        required_skills = []
        if hasattr(order, 'service_type_id') and order.service_type_id:
            try:
                service_type = ServiceType.objects.get(id=order.service_type_id)
                if hasattr(service_type, 'name') and service_type.name:
                    required_skills = [service_type.name]
            except Exception as e:
                print(f"Error getting service type: {e}")
        
        employee_skills = []
        employee_skill_records = EmployeeSkill.objects.filter(employee=employee)
        if employee_skill_records:
            employee_skills = [es.skill.name for es in employee_skill_records]
        
        if required_skills and employee_skills:
            # Tìm kiếm kỹ năng phù hợp dựa trên từ khóa
            matching_skills = []
            matched_pairs = []
            
            for req_skill in required_skills:
                req_keywords = req_skill.lower().split()
                for emp_skill in employee_skills:
                    emp_skill_lower = emp_skill.lower()
                    # Kiểm tra từng từ khóa
                    for keyword in req_keywords:
                        if len(keyword) > 3 and keyword in emp_skill_lower:  # Chỉ kiểm tra từ khóa có ít nhất 4 ký tự
                            matched_pairs.append((req_skill, emp_skill))
                            if req_skill not in matching_skills:
                                matching_skills.append(req_skill)
                            break
            
            if matching_skills:
                # Hiển thị kỹ năng yêu cầu và kỹ năng tương ứng của nhân viên
                match_descriptions = []
                for req_skill, emp_skill in matched_pairs:
                    match_descriptions.append(f"{req_skill} (khớp với {emp_skill})")
                
                reasons.append(f"Có kỹ năng phù hợp: {', '.join(match_descriptions)}")
        
        # Kiểm tra mức lương
        try:
            employee_salary = getattr(employee, 'salary', 0) or 0
            from ..models.employee import Employee
            avg_salary = Employee.objects.all().aggregate(avg_salary=models.Avg('salary'))['avg_salary'] or 0
            
            if employee_salary <= avg_salary * Decimal('0.8'):
                reasons.append("Mức lương thấp, tối ưu chi phí")
            elif employee_salary <= avg_salary:
                reasons.append("Mức lương dưới mức trung bình")
        except Exception as e:
            print(f"Error checking salary: {e}")
        
        # Kiểm tra khối lượng công việc
        try:
            employee_completed_orders = getattr(employee, 'completed_orders_count', 0) or 0
            from ..models.employee import Employee
            avg_orders = Employee.objects.all().aggregate(avg_orders=models.Avg('completed_orders_count'))['avg_orders'] or 0
            
            if employee_completed_orders < avg_orders * 0.7:
                reasons.append("Khối lượng công việc thấp")
        except Exception as e:
            print(f"Error checking workload: {e}")
            
        return reasons

    @staticmethod
    def check_time_availability(employee, order):
        try:

            if not employee.working_start_time or not employee.working_end_time:
                return False

            order_start = order.preferred_start_time
            order_end = order.preferred_end_time
            
            emp_start = employee.working_start_time
            emp_end = employee.working_end_time
            
            order_start_time = order_start.time()
            order_end_time = order_end.time()
            
            if emp_start <= emp_end:
                print("1")
                return emp_start <= order_start_time and order_end_time <= emp_end
            else:
                print("2")
                return order_start_time >= emp_start or order_end_time <= emp_end

        except Exception as error:
            print("Error details:", error) 
            return False