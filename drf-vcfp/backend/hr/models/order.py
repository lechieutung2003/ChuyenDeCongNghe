from django.db import models
from base.models import TimeStampedModel
from .customer import Customer, ServiceType
from businesses.models.employee import Employee
from hr.models.skill import Skill

class Order(TimeStampedModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE)
    area_m2 = models.DecimalField(max_digits=10, decimal_places=2)
    requested_hours = models.DecimalField(max_digits=5, decimal_places=2)
    preferred_start_time = models.DateTimeField()
    preferred_end_time = models.DateTimeField()
    estimated_hours = models.DecimalField(max_digits=5, decimal_places=2)
    cost_confirm = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=20)
    note = models.TextField(blank=True, null=True)
    
    # Feedback và log sau khi hoàn thành đơn hàng
    customer_feedback = models.TextField(
        blank=True, 
        null=True,
        help_text="Phản hồi của khách hàng sau khi hoàn thành dịch vụ"
    )
    admin_log = models.TextField(
        blank=True,
        null=True,
        help_text="Ghi chú của admin về đơn hàng"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "hr_order"

class Assignment(TimeStampedModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    assigned_time = models.DateTimeField()
    status = models.CharField(max_length=20)
    work_hours = models.DecimalField(max_digits=5, decimal_places=2)
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = "hr_assignment"

class DecisionLog(TimeStampedModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    availability_score = models.DecimalField(max_digits=5, decimal_places=2)
    skill_score = models.DecimalField(max_digits=5, decimal_places=2)
    cost_score = models.DecimalField(max_digits=5, decimal_places=2)
    workload_score = models.DecimalField(max_digits=5, decimal_places=2)
    total_score = models.DecimalField(max_digits=5, decimal_places=2)
    computed_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "hr_decision_log"
