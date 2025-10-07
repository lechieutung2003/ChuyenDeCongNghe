import os
import sys
import django
import random
from datetime import time, timedelta, datetime
from decimal import Decimal

# Thêm đường dẫn để có thể import từ dự án Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.base')
django.setup()

from faker import Faker
from django.utils import timezone
from oauth.models import Role, User
from hr.models import Office, Group
from businesses.models import Employee
from common.constants import Gender
from oauth.constants import AccountStatus
from hr.models.skill import Skill, EmployeeSkill
from django.db import transaction
from django.contrib.auth.hashers import make_password
from oauth2_provider.models import AbstractApplication
from oauth.models import Application
from core.settings.base import (
    BUSINESS_CLIENT_ID,
    BUSINESS_CLIENT_SECRET,
    ECOMMERCE_CLIENT_ID,
    ECOMMERCE_CLIENT_SECRET,
    SECRET_KEY
)

fake = Faker('vi_VN')  # Sử dụng locale Việt Nam

SKILL_NAMES = [
    "Deep", "Regular"
]

# Danh sách các quận/huyện tại Đà Nẵng
DA_NANG_DISTRICTS = [
    'Hải Châu', 'Thanh Khê', 'Sơn Trà', 'Ngũ Hành Sơn', 
    'Liên Chiểu', 'Cẩm Lệ', 'Hòa Vang'
]

# Danh sách các phường tại Đà Nẵng theo quận
DA_NANG_WARDS = {
    'Hải Châu': ['Hải Châu 1', 'Hải Châu 2', 'Thạch Thang', 'Thanh Bình', 
                 'Thuận Phước', 'Bình Hiên', 'Bình Thuận', 'Hòa Cường Bắc', 
                 'Hòa Cường Nam', 'Hòa Thuận Đông', 'Hòa Thuận Tây', 'Nam Dương', 'Phước Ninh'],
    'Thanh Khê': ['Tam Thuận', 'Thanh Khê Đông', 'Thanh Khê Tây', 'Xuân Hà', 
                  'Tân Chính', 'Chính Gián', 'Vĩnh Trung', 'Thạc Gián', 'An Khê', 'Hòa Khê'],
    'Sơn Trà': ['An Hải Bắc', 'An Hải Đông', 'An Hải Tây', 'Mân Thái', 
                'Thọ Quang', 'Nại Hiên Đông', 'Phước Mỹ'],
    'Ngũ Hành Sơn': ['Mỹ An', 'Khuê Mỹ', 'Hòa Hải', 'Hòa Quý'],
    'Liên Chiểu': ['Hòa Hiệp Bắc', 'Hòa Hiệp Nam', 'Hòa Khánh Bắc', 
                   'Hòa Khánh Nam', 'Hòa Minh'],
    'Cẩm Lệ': ['Hòa Thọ Đông', 'Hòa Thọ Tây', 'Hòa An', 'Hòa Phát', 
               'Hòa Xuân', 'Khuê Trung'],
    'Hòa Vang': ['Hòa Bắc', 'Hòa Liên', 'Hòa Ninh', 'Hòa Sơn', 'Hòa Nhơn', 
                'Hòa Phong', 'Hòa Châu', 'Hòa Tiến', 'Hòa Phước', 'Hòa Khương', 'Hòa Phú']
}

def create_applications(user):
    """Tạo ứng dụng OAuth2 cho admin nếu chưa có"""
    # Business app
    if not Application.objects.filter(client_id=BUSINESS_CLIENT_ID).exists():
        Application.objects.create(
            client_id=BUSINESS_CLIENT_ID,
            client_type="confidential",
            authorization_grant_type="password",
            client_secret=BUSINESS_CLIENT_SECRET,
            name="Amoz Business",
            algorithm=AbstractApplication.RS256_ALGORITHM,
            scope="__all__",
            skip_authorization=True,
            type=Application.APPLICATION_TYPE_SYSTEM,
            user=user
        )
        print("Đã tạo ứng dụng OAuth2 cho Business")
    # Ecommerce app
    if not Application.objects.filter(client_id=ECOMMERCE_CLIENT_ID).exists():
        Application.objects.create(
            client_id=ECOMMERCE_CLIENT_ID,
            client_type="confidential",
            authorization_grant_type="password",
            client_secret=ECOMMERCE_CLIENT_SECRET,
            name="Amoz Ecommerce",
            algorithm=AbstractApplication.RS256_ALGORITHM,
            scope="__all__",
            skip_authorization=True,
            type=Application.APPLICATION_TYPE_SYSTEM,
            user=user
        )
        print("Đã tạo ứng dụng OAuth2 cho Ecommerce")

def create_skills():
    """Tạo các kỹ năng mẫu nếu chưa có"""
    skills = []
    for name in SKILL_NAMES:
        skill, _ = Skill.objects.get_or_create(name=name)
        skills.append(skill)
    return skills

def assign_skills_to_employee(employee, skills):
    """Gán ngẫu nhiên kỹ năng cho nhân viên"""
    num_skills = random.randint(1, min(3, len(skills)))
    selected_skills = random.sample(skills, num_skills)
    for skill in selected_skills:
        EmployeeSkill.objects.get_or_create(employee=employee, skill=skill)

def create_mock_groups(num_groups=1):
    """
    Tạo dữ liệu mẫu cho bảng Group
    
    Args:
        num_groups (int): Số lượng nhóm cần tạo
    """
    print(f"Bắt đầu tạo {num_groups} nhóm mẫu...")
    
    groups_created = 0
    
    for i in range(num_groups):
        name = f"Nhóm {i+1} - {fake.company_suffix()}"
        
        try:
            # Kiểm tra tất cả các trường bắt buộc của Group
            group = Group.objects.create(
                name=name,
                # Bỏ 'description' vì model Group không có trường này
            )
            groups_created += 1
            print(f"Đã tạo nhóm: {name}")
        except Exception as e:
            print(f"Lỗi khi tạo nhóm {name}: {str(e)}")
    
    print(f"Đã tạo xong {groups_created} nhóm mẫu")
    return Group.objects.all()

def create_mock_office(groups=None):
    """
    Tạo 1 văn phòng mẫu
    
    Args:
        groups (QuerySet): Các nhóm có sẵn để gán cho văn phòng
    """
    print("Bắt đầu tạo văn phòng mẫu...")
    
    if groups is None or not groups.exists():
        groups = create_mock_groups()
    
    # Sử dụng quận Hải Châu cho văn phòng chính
    district = 'Hải Châu'
    ward = 'Hải Châu 1'
    name = "Văn phòng Dịch vụ Vệ sinh Đà Nẵng"
    address = f"123 Lê Lợi, Phường {ward}, Quận {district}, Đà Nẵng"
    
    try:
        office = Office.objects.create(
            name=name,
            established_date=fake.date_between(start_date="-5y", end_date="-1y"),
            email="office@cleaningservice.com",
            phone="0236.1234567",
            address=address,
            group=groups.first() if groups.exists() else None
        )
        print(f"Đã tạo văn phòng: {name} tại {district}, {ward}")
    except Exception as e:
        print(f"Lỗi khi tạo văn phòng {name}: {str(e)}")
        return None
    
    return office

def get_existing_roles():
    """
    Lấy các vai trò hiện có mà không tạo mới
    """
    # Kiểm tra xem các vai trò đã tồn tại chưa
    roles = Role.objects.all()
    
    if not roles.exists():
        print("Cảnh báo: Không tìm thấy vai trò nào trong hệ thống!")
    else:
        print(f"Đã tìm thấy {roles.count()} vai trò trong hệ thống:")
        for role in roles:
            print(f"- {role.name}")
    
    return roles

def create_super_admin(office, roles):
    """
    Tạo một Super Administrator giống init_data.py
    Args:
        office: Văn phòng làm việc của admin
        roles: Danh sách vai trò
    """
    print("Tạo tài khoản Super Administrator...")

    super_admin_email = "admin@gmail.com"
    super_admin_password = "123456"

    # Tạo hoặc lấy role Super Administrator
    role, _ = Role.objects.get_or_create(
        name="Super Administrator",
        defaults={
            "description": "Unlimited resources access.",
            "scope": "__all__",
        }
    )

    user = User.objects.filter(email=super_admin_email).first()
    employee = Employee.objects.filter(work_mail=super_admin_email).first()

    with transaction.atomic():
        if not user:
            user = User.objects.create(
                email=super_admin_email,
                password=make_password(super_admin_password, salt=SECRET_KEY),
                first_name="Super",
                last_name="Administrator",
                is_superuser=True,
                is_staff=True,
                active=True
            )
        if not employee:
            employee = Employee.objects.create(
                first_name="Super",
                last_name="Administrator",
                work_mail=super_admin_email,
                personal_mail=super_admin_email,
                status=AccountStatus.ACTIVE,
                user=user,
                office=office
            )
            employee.roles.add(role)
            employee.save()
        else:
            # Đảm bảo đã gán role nếu employee đã tồn tại
            employee.roles.add(role)
            employee.save()

    print(f"Đã tạo/gán vai trò Super Administrator cho: {employee}")
    print(f"role",role)
    print
    return employee

def create_mock_employees(num_employees=10, office=None, admin=None):
    """
    Tạo dữ liệu mẫu cho bảng Employee
    
    Args:
        num_employees (int): Số lượng nhân viên cần tạo
        office: Văn phòng đã được tạo
        admin: Admin đã được tạo
    """
    print(f"Bắt đầu tạo {num_employees} nhân viên mẫu...")
    
    # Lấy danh sách Roles hiện có (không tạo mới)
    roles = get_existing_roles()
    
    if not roles.exists():
        print("Không thể tiếp tục vì không có vai trò nào trong hệ thống")
        return []
    
    # Sử dụng các quận tại Đà Nẵng
    areas = DA_NANG_DISTRICTS
    
    employees_created = 0
    all_employees = []
    
    # Thêm admin vào danh sách nhân viên nếu có
    if admin:
        all_employees.append(admin)
    
    # Tìm vai trò Employee
    employee_role = roles.filter(name__icontains="employee").first()
    if not employee_role:
        employee_role = roles.first()
        print(f"Không tìm thấy vai trò 'Employee', sử dụng vai trò '{employee_role.name}' làm mặc định")
    
    for i in range(num_employees):
        try:
            # Tạo User mới
            first_name = fake.first_name()
            last_name = fake.last_name()
            email = f"{first_name.lower()}.{last_name.lower()}{random.randint(1, 999)}@example.com"
            
            # Điều chỉnh theo cấu trúc của User trong dự án
            user = User.objects.create_user(
                email=email,
                password="password123",
                first_name=first_name,
                last_name=last_name,
                active=True
            )
            
            # Tạo thời gian làm việc
            start_hour = random.randint(7, 9)
            end_hour = random.randint(16, 18)
            working_start_time = time(hour=start_hour, minute=0)
            working_end_time = time(hour=end_hour, minute=0)
            
            # Tạo nhân viên mới
            employee = Employee(
                user=user,
                first_name=first_name,
                last_name=last_name,
                office=office,
                work_mail=email,
                personal_mail=fake.email(),
                date_of_birth=fake.date_of_birth(minimum_age=18, maximum_age=65),
                phone=fake.phone_number(),
                gender=random.choice([Gender.MALE, Gender.FEMALE]),
                join_date=fake.date_between(start_date="-5y", end_date="today"),
                status=AccountStatus.ACTIVE,
                area=random.choice(areas),
                working_start_time=working_start_time,
                working_end_time=working_end_time,
                completed_orders_count=random.randint(0, 100),
                salary=Decimal(random.uniform(5000000, 15000000)).quantize(Decimal("0.01")),
                total_hours_worked=Decimal(random.uniform(0, 1000)).quantize(Decimal("0.01"))
            )
            
            employee.save()
            all_employees.append(employee)
            
            # Gán vai trò Employee
            employee.roles.add(employee_role)
            
            employees_created += 1
            print(f"Đã tạo nhân viên {employee} ({employees_created}/{num_employees})")
            
        except Exception as e:
            print(f"Lỗi khi tạo nhân viên: {str(e)}")
    
    print(f"Đã tạo xong {employees_created} nhân viên mẫu")
    
    # Gán admin làm quản lý văn phòng
    if office and admin:
        office.manager = admin
        office.save()
        print(f"Đã gán {admin} làm quản lý cho {office.name}")
    
    return all_employees

def clear_data():
    """Xóa tất cả dữ liệu mẫu đã tạo"""
    EmployeeSkill.objects.all().delete()
    Skill.objects.all().delete()
    employee_count, _ = Employee.objects.all().delete()
    office_count, _ = Office.objects.all().delete()
    group_count, _ = Group.objects.all().delete()
    user_count, _ = User.objects.all().delete()
    print(f"Đã xóa {employee_count} nhân viên, {office_count} văn phòng và {group_count} nhóm, {user_count} người dùng.")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Tạo dữ liệu mẫu cho nhân viên và văn phòng")
    parser.add_argument("--employees", type=int, default=50, help="Số lượng nhân viên thường cần tạo")
    parser.add_argument("--clear", action="store_true", default=True, help="Xóa dữ liệu hiện có trước khi tạo mới")
    
    args = parser.parse_args()
    
    # Xóa dữ liệu cũ
    clear_data()

    skills = create_skills()
    
    # Tạo 1 nhóm
    groups = create_mock_groups(num_groups=1)
    
    # Tạo 1 văn phòng
    office = create_mock_office(groups)
    
    # Lấy danh sách vai trò
    roles = get_existing_roles()
    
    # Tạo 1 Super Administrator
    admin = create_super_admin(office, roles)

    create_applications(admin.user)
    
    # Tạo thêm nhân viên thường
    employees = create_mock_employees(num_employees=args.employees, office=office, admin=admin)
    
    for emp in employees:
        assign_skills_to_employee(emp, skills)

    print("Hoàn thành quá trình tạo dữ liệu mẫu!")