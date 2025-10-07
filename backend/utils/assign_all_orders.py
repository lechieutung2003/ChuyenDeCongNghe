import os
import sys
import django
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.base')
django.setup()

from hr.models import Order, Assignment, DecisionLog
from businesses.models.employee import Employee
from django.db import transaction

EMPLOYEE_ID = "e651bc97a8364776919b635ee8f5fcc9"

# Hàm gán toàn bộ đơn hàng cho 1 employee và tạo decision log

def assign_all_orders_to_employee():
    employee = Employee.objects.get(id=EMPLOYEE_ID)
    orders = Order.objects.all()
    now = datetime.now()
    assignments = []
    decision_logs = []
    for order in orders:
        assignments.append(Assignment(
            order=order,
            employee=employee,
            assigned_time=now,
            status="assigned",
            work_hours=order.estimated_hours,
            cost=order.estimated_hours * 50000  # ví dụ cost = giờ * 50k
        ))
        decision_logs.append(DecisionLog(
            order=order,
            employee=employee,
            availability_score=10.0,
            skill_score=10.0,
            cost_score=10.0,
            workload_score=10.0,
            total_score=40.0,
            notes="Auto assigned for test"
        ))
    with transaction.atomic():
        Assignment.objects.bulk_create(assignments)
        DecisionLog.objects.bulk_create(decision_logs)
    print(f"Đã gán {len(assignments)} đơn hàng cho employee {employee.id} và tạo decision log.")

if __name__ == "__main__":
    assign_all_orders_to_employee()
