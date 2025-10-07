from rest_framework import serializers
from ..models import Order, Assignment, DecisionLog
from ..models.customer import Customer, ServiceType
from businesses.serializers.employee import EmployeeShortSerializer
from businesses.serializers.employee import EmployeeShortSerializer
from .customer import CustomerSerializer, ServiceTypeSerializer

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class ServiceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceType
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    customer_details = CustomerSerializer(source='customer', read_only=True)
    service_details = ServiceTypeSerializer(source='service_type', read_only=True)
    
    class Meta:
        model = Order
        fields = '__all__'
        
    def to_representation(self, instance):
        try:
            representation = super().to_representation(instance)
            representation['customer_name'] = f"{instance.customer.name}" if instance.customer else ""
            return representation
        except ValueError as e:
            if "badly formed hexadecimal UUID string" in str(e):
                print(f"Lỗi UUID với order ID: {instance.id}")
                # Trả về một representation tạm thời
                return {
                    'id': str(instance.id),
                    'error': 'Dữ liệu không hợp lệ'
                }
            raise e

class OrderEmployeeSerializer(serializers.ModelSerializer):
    """Serializer cho employee chỉ có thể edit status"""
    
    class Meta:
        model = Order
        fields = ['status']  # Chỉ có status field
        
    def to_representation(self, instance):
        try:
            # Trả về full representation để frontend có đủ thông tin
            data = {
                'id': instance.id,
                'status': instance.status,
                'customer_name': f"{instance.customer.name}" if instance.customer else "",
                'area_m2': instance.area_m2,
                'requested_hours': instance.requested_hours,
                'preferred_start_time': instance.preferred_start_time,
                'preferred_end_time': instance.preferred_end_time,
                'estimated_hours': instance.estimated_hours,
                'cost_confirm': instance.cost_confirm,
                'note': instance.note,
                'created_at': instance.created_at,
                'customer': instance.customer.id if instance.customer else None,
                'service_type': instance.service_type.id if instance.service_type else None,
                'customer_details': CustomerSerializer(instance.customer).data if instance.customer else None,
                'service_details': ServiceTypeSerializer(instance.service_type).data if instance.service_type else None,
            }
            return data
        except ValueError as e:
            if "badly formed hexadecimal UUID string" in str(e):
                print(f"Lỗi UUID với order ID: {instance.id}")
                return {
                    'id': str(instance.id),
                    'error': 'Dữ liệu không hợp lệ'
                }
            raise e

class AssignmentSerializer(serializers.ModelSerializer):
    employee_details = EmployeeShortSerializer(source='employee', read_only=True)
    order_details = OrderSerializer(source='order', read_only=True)
    
    class Meta:
        model = Assignment
        fields = '__all__'

class DecisionLogSerializer(serializers.ModelSerializer):
    employee_details = EmployeeShortSerializer(source='employee', read_only=True)
    
    class Meta:
        model = DecisionLog
        fields = '__all__'