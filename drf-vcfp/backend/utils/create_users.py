import os
import sys
import django
import uuid

# Thiết lập môi trường Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.base')
django.setup()

# Import models sau khi thiết lập Django
from django.db import transaction
from oauth.models import User, Role
from businesses.models import Employee
from django.contrib.auth.hashers import make_password
from oauth.constants import AccountStatus

def create_roles():
    """Tạo các roles cơ bản trong hệ thống"""
    roles_data = [
        {
            'name': 'Super Administrator',
            'description': 'Unlimited resources access.',
            'scope': '__all__'
        },
        {
            'name': 'Employee',
            'description': 'Regular employee with basic access.',
            'scope': 'employees:view'
        },
        {
            'name': 'Guest',
            'description': 'Guest user with limited access.',
            'scope': 'users:view-mine'
        }
    ]
    
    created_roles = []
    
    with transaction.atomic():
        for role_data in roles_data:
            role, created = Role.objects.update_or_create(
                name=role_data['name'],  # ✅ LOOKUP FIELD
                defaults={
                    'description': role_data['description'],
                    'scope': role_data['scope']
                }
            )
            created_roles.append(role)
            print(f"Role {'created' if created else 'updated'}: {role.name} (ID: {role.id})")
    
    print(f"\nTổng cộng {len(created_roles)} roles đã được tạo/cập nhật")
    return created_roles


def create_users_with_roles():
    create_roles()
    # Lấy role đã tồn tại trong database theo ID
    try:
        admin_role = Role.objects.get(name='Super Administrator')  # Super Administrator
        employee_role = Role.objects.get(name='Employee')  # Employee
        guest_role = Role.objects.get(name='Guest')  # Guest

        print(f"Tìm thấy roles: Admin({admin_role.name}), Employee({employee_role.name}), Guest({guest_role.name})")
    except Role.DoesNotExist:
        print("Không tìm thấy role theo ID, kiểm tra lại dữ liệu role trong database")
        return
    
    # 1. Tạo Admin User và Employee
    with transaction.atomic():
        # Tạo User
        admin_user, user_created = User.objects.update_or_create(
            email="admin@gmail.com",
            defaults={
                "password": make_password("123456"),
                "first_name": "Super", 
                "last_name": "Administrator",
                "is_staff": True,
                "is_superuser": True,
                "active": True
            }
        )
        
        # Tạo Employee và liên kết với Role
        admin_employee, emp_created = Employee.objects.update_or_create(
            work_mail="admin@gmail.com",
            defaults={
                "first_name": "Super",
                "last_name": "Administrator",
                "personal_mail": "admin@gmail.com",
                "status": AccountStatus.ACTIVE,
                "user": admin_user  # Liên kết với User
            }
        )
        
        # Liên kết Employee với Role
        admin_employee.roles.clear()  # Xóa các roles hiện tại nếu có
        admin_employee.roles.add(admin_role)
        print(f"Assigned roles: {[role.name for role in admin_employee.roles.all()]}")
        print([role.scope for role in admin_employee.roles.all()])
        admin_employee.save()
        
        print(f"Admin user {'created' if user_created else 'updated'} with ID: {admin_user.id}")
        print(f"Admin employee {'created' if emp_created else 'updated'} with ID: {admin_employee.id}")
    
    # 2. Tạo Regular Employee User và Employee
    with transaction.atomic():
        # Tạo User
        regular_user, user_created = User.objects.update_or_create(
            email="employee@gmail.com",
            defaults={
                "password": make_password("123456"),
                "first_name": "Regular", 
                "last_name": "Employee",
                "is_staff": True,
                "is_superuser": False,
                "active": True
            }
        )
        
        # Tạo Employee và liên kết với Role
        regular_employee, emp_created = Employee.objects.update_or_create(
            work_mail="employee@gmail.com",
            defaults={
                "first_name": "Regular",
                "last_name": "Employee",
                "personal_mail": "employee@gmail.com",
                "status": AccountStatus.ACTIVE,
                "user": regular_user  # Liên kết với User
            }
        )
        
        # Liên kết Employee với Role
        regular_employee.roles.clear()  # Xóa các roles hiện tại nếu có
        regular_employee.roles.add(employee_role)
        print(f"Assigned roles: {[role.name for role in regular_employee.roles.all()]}")
        print([role.scope for role in regular_employee.roles.all()])
        regular_employee.save()
        
        print(f"Employee user {'created' if user_created else 'updated'} with ID: {regular_user.id}")
        print(f"Employee profile {'created' if emp_created else 'updated'} with ID: {regular_employee.id}")
    
    # 3. Tạo Guest User và Employee (nhưng gắn role Guest)
    with transaction.atomic():
        # Tạo User
        guest_user, user_created = User.objects.update_or_create(
            email="guest@gmail.com",
            defaults={
                "password": make_password("123456"),
                "first_name": "Guest", 
                "last_name": "User",
                "is_staff": False,
                "is_superuser": False,
                "is_guest": True,
                "active": True
            }
        )
        
        # Tạo Employee và liên kết với Role
        guest_employee, emp_created = Employee.objects.update_or_create(
            work_mail="guest@gmail.com",
            defaults={
                "first_name": "Guest",
                "last_name": "User",
                "personal_mail": "guest@gmail.com",
                "status": AccountStatus.ACTIVE,
                "user": guest_user  # Liên kết với User
            }
        )
        
        # Liên kết Employee với Role
        guest_employee.roles.clear()  # Xóa các roles hiện tại nếu có
        guest_employee.roles.add(guest_role)
        print(guest_employee.roles)
        print(f"Assigned roles: {[role.name for role in guest_employee.roles.all()]}")
        print([role.scope for role in guest_employee.roles.all()])
        guest_employee.save()
        
        print(f"Guest user {'created' if user_created else 'updated'} with ID: {guest_user.id}")
        print(f"Guest employee {'created' if emp_created else 'updated'} with ID: {guest_employee.id}")

if __name__ == "__main__":
    create_users_with_roles()