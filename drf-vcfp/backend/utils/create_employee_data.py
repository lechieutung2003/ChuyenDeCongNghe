import os
import sys
import django
import random
from datetime import date, time
from decimal import Decimal

# Thiết lập Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.base')
django.setup()

from businesses.models import Employee
from oauth.models import User, Role
from oauth.constants import AccountStatus
from common.constants import Gender
from hr.models import Office
from django.db import transaction

def create_sample_employees(num_employees=30):
    """Tạo dữ liệu nhân viên dịch vụ dọn dẹp nhà cửa tại Đà Nẵng"""
    
    print(f"Tạo {num_employees} nhân viên dịch vụ dọn dẹp nhà cửa...")
    
    # Tạo office đơn giản nếu chưa có
    office, created = Office.objects.get_or_create(
        name="Công ty dịch vụ dọn dẹp Đà Nẵng",
        defaults={
            'address': "123 Trần Phú, Hải Châu, Đà Nẵng"
        }
    )
    if created:
        print("Đã tạo văn phòng mới")
    
    # Tạo roles đơn giản cho dịch vụ dọn dẹp (sử dụng field 'name' thay vì 'code')
    roles_data = [
        'Nhân viên dọn dẹp',
        'Trưởng nhóm dọn dẹp', 
        'Nhân viên chuyên sâu',
    ]
    
    roles = []
    for role_name in roles_data:
        role, created = Role.objects.get_or_create(
            name=role_name,
            defaults={
                'description': f'Vai trò {role_name} trong dịch vụ dọn dẹp nhà cửa'
            }
        )
        roles.append(role)
        if created:
            print(f"Đã tạo role: {role_name}")
    
    # Dữ liệu tên Việt Nam
    first_names = ['Nguyễn', 'Trần', 'Lê', 'Phạm', 'Hoàng', 'Phan', 'Vũ', 'Võ', 'Đặng', 'Bùi']
    last_names = [
        'Văn Minh', 'Thị Lan', 'Văn Hùng', 'Thị Mai', 'Văn Long', 'Thị Hoa',
        'Văn Dũng', 'Thị Nga', 'Văn Tuấn', 'Thị Linh', 'Văn Khoa', 'Thị Thảo',
        'Văn Đức', 'Thị Vân', 'Văn Phong', 'Thị Yến'
    ]
    
    # Các quận ở Đà Nẵng
    areas_danang = [
        'Hải Châu',
        'Thanh Khê', 
        'Sơn Trà',
        'Ngũ Hành Sơn',
        'Liên Chiểu',
        'Cẩm Lệ',
        'Hòa Vang'
    ]
    
    employees_to_create = []
    
    try:
        with transaction.atomic():
            for i in range(num_employees):
                first_name = random.choice(first_names)
                last_name = random.choice(last_names)
                
                # Giờ làm việc từ 7h-17h hoặc 8h-18h
                start_hour = random.choice([7, 8])
                end_hour = start_hour + 8  # 8 tiếng làm việc thực tế (không tính nghỉ trưa)
                
                # Tính số giờ làm việc trong ngày
                daily_hours = end_hour - start_hour
                
                # Lương theo giờ (25,000 - 80,000 VND/giờ tùy vào vai trò)
                hourly_rate_ranges = {
                    'Nhân viên dọn dẹp': (25000, 40000),      # 25k-40k/giờ
                    'Trưởng nhóm dọn dẹp': (50000, 70000),    # 50k-70k/giờ
                    'Nhân viên chuyên sâu': (45000, 65000),   # 45k-65k/giờ
                }
                
                # Chọn role trước để tính lương
                selected_role = random.choice(roles)
                min_rate, max_rate = hourly_rate_ranges.get(selected_role.name, (30000, 50000))
                hourly_salary = random.randint(min_rate, max_rate)
                
                employee = Employee(
                    first_name=first_name,
                    last_name=last_name,
                    office=office,
                    work_mail=f"nhanvien{i+1:03d}@dondep-danang.vn",
                    phone=f"090{random.randint(1000000, 9999999)}",
                    gender=random.choice([Gender.MALE, Gender.FEMALE]),
                    date_of_birth=date(
                        random.randint(1985, 2005),  # Tuổi từ 19-39
                        random.randint(1, 12),
                        random.randint(1, 28)
                    ),
                    join_date=date(
                        random.randint(2020, 2024),
                        random.randint(1, 12),
                        random.randint(1, 28)
                    ),
                    status=random.choice([AccountStatus.ACTIVE, AccountStatus.ACTIVE, AccountStatus.ACTIVE, AccountStatus.DEACTIVE]),  # 75% active
                    
                    # Thông tin dịch vụ dọn dẹp
                    area=random.choice(areas_danang),
                    working_start_time=time(start_hour, 0),
                    working_end_time=time(end_hour, 0),
                    completed_orders_count=random.randint(10, 200),  # Số nhà đã dọn dẹp
                    salary=Decimal(str(hourly_salary)),  # Lương theo giờ (VND/giờ)
                    total_hours_worked=Decimal(str(daily_hours))  # Số giờ làm việc trong ngày
                )
                employees_to_create.append((employee, selected_role))
            
            # Bulk create employees
            employees_only = [emp[0] for emp in employees_to_create]
            created_employees = Employee.objects.bulk_create(employees_only)
            print(f"Đã tạo {len(created_employees)} nhân viên")
            
            # Thêm roles cho employees (phải làm sau khi có ID)
            print("Đang thêm roles cho nhân viên...")
            for i, employee in enumerate(created_employees):
                selected_role = employees_to_create[i][1]
                employee.roles.set([selected_role])
            
            print("Đã thêm roles cho tất cả nhân viên")
            
            # Hiển thị một vài nhân viên mẫu
            print("\nNhân viên đã tạo:")
            for emp in created_employees[:5]:
                role_names = ', '.join([role.name for role in emp.roles.all()])
                daily_income = float(emp.salary) * float(emp.total_hours_worked)
                print(f"- {emp.first_name} {emp.last_name} | {emp.area} | {role_names}")
                print(f"  Lương: {emp.salary:,} VND/giờ | {emp.total_hours_worked}h/ngày | Thu nhập/ngày: {daily_income:,.0f} VND")
                
    except Exception as e:
        print(f"Lỗi khi tạo dữ liệu: {e}")
        import traceback
        traceback.print_exc()

def update_existing_employees():
    """Cập nhật lại dữ liệu employees đã có trong database"""
    print("Đang cập nhật dữ liệu employees hiện có...")
    
    employees = Employee.objects.all()
    if not employees.exists():
        print("Không có nhân viên nào trong database. Chạy tạo dữ liệu mới.")
        return
    
    # Định nghĩa lương theo giờ theo vai trò
    hourly_rate_ranges = {
        'Nhân viên dọn dẹp': (25000, 40000),      # 25k-40k/giờ
        'Trưởng nhóm dọn dẹp': (50000, 70000),    # 50k-70k/giờ
        'Nhân viên chuyên sâu': (45000, 65000),   # 45k-65k/giờ
    }
    
    updated_count = 0
    
    try:
        with transaction.atomic():
            for employee in employees:
                # Tính số giờ làm việc trong ngày từ working_start_time và working_end_time
                if employee.working_start_time and employee.working_end_time:
                    start_hour = employee.working_start_time.hour
                    end_hour = employee.working_end_time.hour
                    daily_hours = end_hour - start_hour
                    
                    # Đảm bảo giờ làm việc hợp lý (6-10 giờ/ngày)
                    if daily_hours <= 0 or daily_hours > 12:
                        daily_hours = 8  # Default 8 giờ
                else:
                    daily_hours = 8  # Default nếu không có thời gian
                
                # Xác định lương theo vai trò
                employee_roles = employee.roles.all()
                if employee_roles.exists():
                    role_name = employee_roles.first().name
                    min_rate, max_rate = hourly_rate_ranges.get(role_name, (30000, 50000))
                else:
                    min_rate, max_rate = (25000, 40000)  # Default cho nhân viên thường
                
                hourly_salary = random.randint(min_rate, max_rate)
                
                # Cập nhật
                employee.salary = Decimal(str(hourly_salary))  # Lương theo giờ
                employee.total_hours_worked = Decimal(str(daily_hours))  # Giờ làm việc/ngày
                employee.save()
                
                updated_count += 1
        
        print(f"Đã cập nhật {updated_count} nhân viên")
        
        # Hiển thị một vài nhân viên sau khi cập nhật
        print("\nNhân viên sau khi cập nhật:")
        for emp in employees[:5]:
            role_names = ', '.join([role.name for role in emp.roles.all()])
            daily_income = float(emp.salary) * float(emp.total_hours_worked)
            print(f"- {emp.first_name} {emp.last_name} | {emp.area} | {role_names}")
            print(f"  Lương: {emp.salary:,} VND/giờ | {emp.total_hours_worked}h/ngày | Thu nhập/ngày: {daily_income:,.0f} VND")
            
    except Exception as e:
        print(f"Lỗi khi cập nhật dữ liệu: {e}")
        import traceback
        traceback.print_exc()

def show_statistics():
    """Hiển thị thống kê nhân viên"""
    print("\n=== THỐNG KÊ NHÂN VIÊN DỊCH VỤ DỌN DẸP ===")
    
    total = Employee.objects.count()
    active = Employee.objects.filter(status=AccountStatus.ACTIVE).count()
    
    print(f"Tổng nhân viên: {total}")
    print(f"Đang hoạt động: {active}")
    print(f"Tạm nghỉ: {total - active}")
    
    print("\nThống kê theo khu vực:")
    areas = ['Hải Châu', 'Thanh Khê', 'Sơn Trà', 'Ngũ Hành Sơn', 'Liên Chiểu', 'Cẩm Lệ', 'Hòa Vang']
    for area in areas:
        count = Employee.objects.filter(area=area).count()
        if count > 0:
            print(f"  {area}: {count} nhân viên")
    
    # Thống kê theo vai trò
    print("\nThống kê theo vai trò:")
    roles = Role.objects.filter(name__icontains='dọn dẹp')
    for role in roles:
        count = role.employees.count()
        if count > 0:
            print(f"  {role.name}: {count} nhân viên")
    
    # Thống kê lương theo giờ
    from django.db.models import Avg, Min, Max
    salary_stats = Employee.objects.aggregate(
        avg=Avg('salary'),
        min=Min('salary'), 
        max=Max('salary')
    )
    if salary_stats['avg']:
        print(f"\nThống kê lương theo giờ:")
        print(f"  Trung bình: {salary_stats['avg']:,.0f} VND/giờ")
        print(f"  Thấp nhất: {salary_stats['min']:,.0f} VND/giờ")
        print(f"  Cao nhất: {salary_stats['max']:,.0f} VND/giờ")
    
    # Thống kê thu nhập theo ngày
    print(f"\nThống kê thu nhập ước tính theo ngày:")
    for emp in Employee.objects.all()[:3]:
        daily_income = float(emp.salary) * float(emp.total_hours_worked)
        role_name = emp.roles.first().name if emp.roles.exists() else "Chưa có vai trò"
        print(f"  {emp.first_name} {emp.last_name} ({role_name}): {daily_income:,.0f} VND/ngày")

def clean_data():
    """Xóa dữ liệu cũ"""
    print("Đang xóa dữ liệu cũ...")
    
    # Xóa employees
    employee_count = Employee.objects.count()
    Employee.objects.all().delete()
    
    # Xóa roles dọn dẹp
    role_count = Role.objects.filter(name__icontains='dọn dẹp').count()
    Role.objects.filter(name__icontains='dọn dẹp').delete()
    
    # Xóa office dọn dẹp
    office_count = Office.objects.filter(name__icontains='dọn dẹp').count()
    Office.objects.filter(name__icontains='dọn dẹp').delete()
    
    print(f"Đã xóa {employee_count} nhân viên, {role_count} vai trò, {office_count} văn phòng")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Tạo dữ liệu nhân viên dịch vụ dọn dẹp')
    parser.add_argument('--count', type=int, default=30, help='Số lượng nhân viên')
    parser.add_argument('--reset', action='store_true', help='Xóa dữ liệu cũ')
    parser.add_argument('--update', action='store_true', help='Cập nhật dữ liệu hiện có')
    parser.add_argument('--stats', action='store_true', help='Xem thống kê')
    
    args = parser.parse_args()
    
    if args.reset:
        clean_data()
    
    if args.update:
        update_existing_employees()
        show_statistics()
    elif args.stats:
        show_statistics()
    else:
        create_sample_employees(args.count)
        show_statistics()