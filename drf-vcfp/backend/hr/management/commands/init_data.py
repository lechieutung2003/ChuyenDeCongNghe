from django.contrib.auth.hashers import make_password
from oauthlib.oauth2.rfc6749.utils import list_to_scope
from django.db import transaction
from django.db.models import Q
from core.settings.base import (
    SECRET_KEY,
    SUPER_ADMIN_EMAIL,
    SUPER_ADMIN_PASSWORD,
    BUSINESS_CLIENT_ID,
    BUSINESS_CLIENT_SECRET,
    ECOMMERCE_CLIENT_ID,
    ECOMMERCE_CLIENT_SECRET
)
from django.core.management.base import BaseCommand, CommandError
from oauth2_provider.models import AbstractApplication
from oauth.constants import AccountStatus
from oauth.models import Role, User, Application
from businesses.models import Employee
from ecommerce.models import Customer
from ecommerce.scopes import default_scopes as ecommerce_default_scopes


class Command(BaseCommand):
    help = "Init ecommerce data"

    def handle(self, *args, **options):
        user, employee, customer, emp_user, emp_profile, guest_user, guest_customer = self.create_accounts()
        self.create_applications(user=user)
        self.stdout.write(self.style.SUCCESS("Init data successfully"))
    
    @classmethod
    def create_applications(cls, user=None):
        # Console app, for employeese logging in
        console_app = Application.objects.filter(Q(client_id=BUSINESS_CLIENT_ID)).exists()
        if not console_app:
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
        # Ecommer app, for customers logging in
        ecomme_app = Application.objects.filter(Q(client_id=ECOMMERCE_CLIENT_ID)).exists()
        if not ecomme_app:
            ecommere_client_scopes = set(ecommerce_default_scopes.keys())
            Application.objects.create(
                client_id=ECOMMERCE_CLIENT_ID,
                client_type="confidential",
                authorization_grant_type="password",
                client_secret=ECOMMERCE_CLIENT_SECRET,
                name="Amoz Ecommerce",
                algorithm=AbstractApplication.RS256_ALGORITHM,
                scope=list_to_scope(ecommere_client_scopes),
                skip_authorization=True,
                type=Application.APPLICATION_TYPE_SYSTEM,
                user=user
            )
    
    @classmethod
    def create_accounts(cls):
        role, created = Role.objects.get_or_create(
            name="Super Administrator",
            description="Unlimited resources access.",
            scope="__all__",
        )
        user = User.objects.filter(email=SUPER_ADMIN_EMAIL).first()
        employee = Employee.objects.filter(work_mail=SUPER_ADMIN_EMAIL).first()
        customer = Customer.objects.filter(email=SUPER_ADMIN_EMAIL).first()
        with transaction.atomic():
            if not user:
                user = User.objects.create(
                    email=SUPER_ADMIN_EMAIL,
                    password=make_password(
                        SUPER_ADMIN_PASSWORD, salt=SECRET_KEY
                    ),
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
                    work_mail=SUPER_ADMIN_EMAIL,
                    personal_mail=SUPER_ADMIN_EMAIL,
                    status=AccountStatus.ACTIVE,
                    user=user
                )
                employee.roles.add(role)
                employee.save()
            if not customer:
                customer = Customer.objects.create(
                    first_name="Super",
                    last_name="Administrator",
                    email=SUPER_ADMIN_EMAIL,
                    status=AccountStatus.ACTIVE,
                    user=user
                )
        
        # Tạo thêm các roles mới
        employee_role, _ = Role.objects.get_or_create(
            name="Employee",
            description="Regular employee access",
            scope="users:view-mine users:edit-mine employees:view-mine employees:edit-mine tasks:view tasks:edit-mine",
        )
        
        guest_role, _ = Role.objects.get_or_create(
            name="Guest",
            description="Limited guest access",
            scope="users:view-mine users:edit-mine",
        )
        
        # Tạo Employee thông thường
        regular_employee_email = "employee@gmail.com"
        employee_user = User.objects.filter(email=regular_employee_email).first()
        employee_profile = Employee.objects.filter(work_mail=regular_employee_email).first()
        
        with transaction.atomic():
            if not employee_user:
                employee_user = User.objects.create(
                    email=regular_employee_email,
                    password=make_password("123456", salt=SECRET_KEY),
                    first_name="Regular",
                    last_name="Employee",
                    is_superuser=False,
                    is_staff=True,  # Vẫn cho phép đăng nhập admin site
                    active=True
                )
            if not employee_profile:
                employee_profile = Employee.objects.create(
                    first_name="Regular",
                    last_name="Employee",
                    work_mail=regular_employee_email,
                    personal_mail=regular_employee_email,
                    status=AccountStatus.ACTIVE,
                    user=employee_user
                )
                employee_profile.roles.add(employee_role)
                employee_profile.save()
        
        # Tạo Guest
        guest_email = "guest@gmail.com"
        guest_user = User.objects.filter(email=guest_email).first()
        guest_customer = Customer.objects.filter(email=guest_email).first()
        
        with transaction.atomic():
            if not guest_user:
                guest_user = User.objects.create(
                    email=guest_email,
                    password=make_password("123456", salt=SECRET_KEY),
                    first_name="Guest",
                    last_name="User",
                    is_superuser=False,
                    is_staff=False,
                    is_guest=True,
                    active=True
                )
            if not guest_customer:
                guest_customer = Customer.objects.create(
                    first_name="Guest",
                    last_name="User",
                    email=guest_email,
                    status=AccountStatus.ACTIVE,
                    user=guest_user
                )
        
        print(f"Employee created with ID: {employee_user.id if employee_user else 'None'}")
        print(f"Guest created with ID: {guest_user.id if guest_user else 'None'}")
        
        # Trả về kết quả ban đầu
        return user, employee, customer, employee_user, employee_profile, guest_user, guest_customer
