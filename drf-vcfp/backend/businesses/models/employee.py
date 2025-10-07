from common.constants import Gender
from base.models import TimeStampedModel
from oauth.constants import AccountStatus
from oauth.models import User

from django.db import models
from oauth.models import Role  
from django.utils import timezone


def avatar_file(instance, filename):
    return  "\\".join(['employees', str(instance.id), filename])


class EmployeeWorkingStatus:
    """Working status choices for employees"""
    NO_WORKING_HOURS = 0
    ACTIVE = 1
    INACTIVE = 2
    
    CHOICES = [
        (NO_WORKING_HOURS, 'No working hours set'),
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive'),
    ]


class Employee(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="employees")
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    office = models.ForeignKey('hr.Office', on_delete=models.CASCADE, blank=True, related_name="employees",null=True)
    work_mail = models.EmailField(max_length=255, null=True)
    personal_mail = models.EmailField(max_length=255, null=True)
    date_of_birth = models.DateField(null=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    gender = models.CharField(max_length=20, choices=Gender.CHOICES, default=Gender.MALE, blank=True, null=True)
    avatar = models.ImageField(upload_to=avatar_file, max_length=255, blank=True, null=True)
    join_date = models.DateField(default=timezone.now)
    roles = models.ManyToManyField(Role, related_name="employees", null=True, blank=True)
    status = models.SmallIntegerField(
        choices=EmployeeWorkingStatus.CHOICES, 
        default=EmployeeWorkingStatus.NO_WORKING_HOURS, 
        help_text="Auto-computed working status based on working hours and current time"
    )    
    # Các trường mới được bổ sung
    area = models.CharField(max_length=100, null=True, blank=True, help_text="Khu vực làm việc của nhân viên")
    working_start_time = models.TimeField(null=True, blank=True, help_text="Giờ bắt đầu làm việc")
    working_end_time = models.TimeField(null=True, blank=True, help_text="Giờ kết thúc làm việc")
    completed_orders_count = models.PositiveIntegerField(default=0, help_text="Số lượng đơn hàng đã hoàn thành")
    salary = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, help_text="Mức lương")
    total_hours_worked = models.DecimalField(max_digits=8, decimal_places=2, default=0.00, help_text="Tổng số giờ làm việc")

    class Meta:
        db_table = "employees"

    @property
    def photo_value(self):
        return self.avatar

    @property
    def image_attr(self):
        return self.avatar
    
    @property
    def working_hours_per_day(self):
        """Tính số giờ làm việc trong ngày"""
        if self.working_start_time and self.working_end_time:
            start = timezone.datetime.combine(timezone.now().date(), self.working_start_time)
            end = timezone.datetime.combine(timezone.now().date(), self.working_end_time)
            diff = end - start
            return diff.total_seconds() / 3600  # Chuyển đổi sang giờ
        return 0
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.area or 'No Area'}"