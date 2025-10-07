import os
import sys
import django
import random
import uuid
from datetime import datetime, timedelta

# Thiết lập Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.base')
django.setup()

from hr.models import Order, Customer, ServiceType
from django.db import transaction

def create_sample_customers():
    """Tạo dữ liệu khách hàng mẫu chỉ ở Đà Nẵng nếu chưa có"""
    if not Customer.objects.exists():
        print("Tạo dữ liệu khách hàng mẫu...")
        districts = [
            "Hải Châu", "Thanh Khê", "Sơn Trà", "Ngũ Hành Sơn", "Liên Chiểu"
        ]
        customers = [
            Customer(
                id=uuid.uuid4(),
                name=f"Nguyễn Văn {chr(65+i)}",
                phone=f"09{i+1}0000{i+1}00",
                email=f"customer{i+1}@example.com",
                password="password123",  # Nên hash trong thực tế
                address=f"123 Đường {chr(65+i)}, Quận {districts[i % len(districts)]}, Đà Nẵng",
                area=["urban", "suburban", "vip"][i % 3]
            ) for i in range(5)
        ]
        Customer.objects.bulk_create(customers)
        print(f"Đã tạo {len(customers)} khách hàng")
    else:
        print("Đã có dữ liệu khách hàng, bỏ qua bước tạo")
    return list(Customer.objects.all())

def create_sample_service_types():
    """Tạo dữ liệu loại dịch vụ mẫu nếu chưa có"""
    if not ServiceType.objects.exists():
        print("Tạo dữ liệu loại dịch vụ mẫu...")
        service_types = [
            ServiceType(
                id=uuid.uuid4(),
                name="Vệ sinh nhà ở",
                price_per_m2=50000,
                cleaning_rate_m2_per_h=30
            ),
            ServiceType(
                id=uuid.uuid4(),
                name="Vệ sinh văn phòng",
                price_per_m2=40000,
                cleaning_rate_m2_per_h=40
            ),
            ServiceType(
                id=uuid.uuid4(),
                name="Vệ sinh kính cao tầng",
                price_per_m2=70000,
                cleaning_rate_m2_per_h=20
            )
        ]
        ServiceType.objects.bulk_create(service_types)
        print(f"Đã tạo {len(service_types)} loại dịch vụ")
    else:
        print("Đã có dữ liệu loại dịch vụ, bỏ qua bước tạo")
    return list(ServiceType.objects.all())

def create_sample_orders(num_orders=20):
    """Tạo dữ liệu đơn hàng mẫu"""
    try:
        customers = create_sample_customers()
        service_types = create_sample_service_types()
        
        if not customers or not service_types:
            print("Thiếu dữ liệu khách hàng hoặc dịch vụ. Dừng lại.")
            return

        print(f"Bắt đầu tạo {num_orders} đơn hàng mẫu...")

        statuses = ['pending', 'confirmed', 'in_progress', 'completed', 'cancelled']
        orders_to_create = []
        start_date = datetime(2025, 9, 1)

        for i in range(num_orders):
            customer = random.choice(customers)
            service_type = random.choice(service_types)

            days_offset = random.randint(0, 29)
            hours_offset = random.randint(8, 16)
            minutes_offset = random.choice([0, 15, 30, 45])

            preferred_start_time = start_date + timedelta(days=days_offset, hours=hours_offset, minutes=minutes_offset)

            area_m2 = random.uniform(50, 350)
            cleaning_rate = service_type.cleaning_rate_m2_per_h
            estimated_hours = area_m2 / cleaning_rate
            requested_hours = estimated_hours * random.uniform(0.9, 1.2)
            preferred_end_time = preferred_start_time + timedelta(hours=requested_hours)

            if days_offset < 15:
                status = random.choice(['completed', 'cancelled', 'in_progress'])
            else:
                status = random.choice(['pending', 'confirmed'])

            notes = [
                f"Khách yêu cầu làm sạch kỹ phòng {random.choice(['khách', 'ngủ', 'bếp'])}",
                "Khách có thú cưng, cần chú ý",
                "Yêu cầu sử dụng chất tẩy rửa không mùi",
                "Khách muốn có hóa đơn VAT",
                "Cần mang theo thang để lau cửa sổ",
                "Khách đặt thêm dịch vụ lau kính",
                "Cần 2 nhân viên để hoàn thành nhanh hơn",
                "Khách yêu cầu đến đúng giờ",
                "Khách cần hoàn thành trước 12h",
                "Khu vực có nhiều đồ dễ vỡ, cần cẩn thận"
            ]

            order = Order(
                id=uuid.uuid4(),
                customer=customer,
                service_type=service_type,
                area_m2=area_m2,
                requested_hours=round(requested_hours, 2),
                preferred_start_time=preferred_start_time,
                preferred_end_time=preferred_end_time,
                estimated_hours=round(estimated_hours, 2),
                status=status,
                note=random.choice(notes)
            )
            orders_to_create.append(order)

        with transaction.atomic():
            created_orders = Order.objects.bulk_create(orders_to_create)
            print(f"Đã tạo thành công {len(created_orders)} đơn hàng")

            print("\nMột số đơn hàng:")
            for order in created_orders[:5]:
                print(f"- {order.id} | {order.customer.name} | {order.service_type.name} | {order.status}")

    except Exception as e:
        print(f"Lỗi khi tạo dữ liệu đơn hàng: {e}")
        import traceback; traceback.print_exc()

def reset_data():
    """Xóa toàn bộ dữ liệu hiện có và tạo mới từ đầu"""
    try:
        Order.objects.all().delete()
        Customer.objects.all().delete()
        ServiceType.objects.all().delete()
        print("Đã xóa toàn bộ dữ liệu thành công.")
        return True
    except Exception as e:
        print(f"Lỗi khi xóa dữ liệu: {e}")
        import traceback; traceback.print_exc()
        return False

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Tạo dữ liệu mẫu cho Order')
    parser.add_argument('--count', type=int, default=20)
    parser.add_argument('--reset', action='store_true')
    args = parser.parse_args()

    reset_data()
    create_sample_orders(args.count)
