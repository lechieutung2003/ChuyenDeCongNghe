from hr.models import Employee, Assignment
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from hr.serializers import AssignmentSerializer
from hr.models.order import Order
from hr.serializers.order import OrderSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from hr.serializers.full_user import FullUserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from hr.serializers.register_customer import RegisterCustomerSerializer
from rest_framework.permissions import AllowAny
from hr.models import Employee, Assignment
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from hr.serializers import AssignmentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

class SimpleCreateOrderAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerOrdersAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = getattr(request.user, "id", None)
        if not user_id:
            return Response({"detail": "Không xác định được user"}, status=403)

        from hr.models.customer import Customer
        from hr.models import Order
        try:
            customer = Customer.objects.get(user_id=user_id)
        except Customer.DoesNotExist:
            return Response({"detail": "User không phải là customer"}, status=403)

        orders = Order.objects.filter(customer=customer)
        from hr.serializers.order import OrderSerializer
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


class UpdateOrderFeedbackAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, order_id):
        user_id = getattr(request.user, "id", None)
        if not user_id:
            return Response({"detail": "Không xác định được user"}, status=403)

        from hr.models.customer import Customer
        try:
            customer = Customer.objects.get(user_id=user_id)
        except Customer.DoesNotExist:
            return Response({"detail": "User không phải là customer"}, status=403)

        try:
            order = Order.objects.get(id=order_id, customer=customer)
        except Order.DoesNotExist:
            return Response({"detail": "Không tìm thấy đơn hàng"}, status=404)

        # Chỉ cho phép cập nhật feedback cho đơn hàng đã hoàn thành
        if order.status != 'completed':
            return Response({
                "detail": "Chỉ có thể gửi phản hồi cho đơn hàng đã hoàn thành"
            }, status=400)

        customer_feedback = request.data.get('customer_feedback', '')
        if not customer_feedback.strip():
            return Response({"detail": "Phản hồi không được để trống"}, status=400)

        order.customer_feedback = customer_feedback.strip()
        order.save()

        from hr.serializers.order import OrderSerializer
        serializer = OrderSerializer(order)
        return Response(serializer.data)


class UpdateOrderAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        """Lấy thông tin chi tiết đơn hàng"""
        user_id = getattr(request.user, "id", None)
        if not user_id:
            return Response({"detail": "Không xác định được user"}, status=403)

        from hr.models.customer import Customer
        try:
            customer = Customer.objects.get(user_id=user_id)
        except Customer.DoesNotExist:
            return Response({"detail": "User không phải là customer"}, status=403)

        try:
            order = Order.objects.get(id=order_id, customer=customer)
        except Order.DoesNotExist:
            return Response({"detail": "Không tìm thấy đơn hàng"}, status=404)

        from hr.serializers.order import OrderSerializer
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def put(self, request, order_id):
        """Cập nhật thông tin đơn hàng (chỉ cho trạng thái pending)"""
        print(f"DEBUG: PUT request data: {request.data}")
        print(f"DEBUG: Order ID: {order_id}")
        
        user_id = getattr(request.user, "id", None)
        if not user_id:
            return Response({"detail": "Không xác định được user"}, status=403)

        from hr.models.customer import Customer
        try:
            customer = Customer.objects.get(user_id=user_id)
            print(f"DEBUG: Found customer: {customer.id}")
        except Customer.DoesNotExist:
            return Response({"detail": "User không phải là customer"}, status=403)

        try:
            order = Order.objects.get(id=order_id, customer=customer)
            print(f"DEBUG: Found order: {order.id}, status: {order.status}")
        except Order.DoesNotExist:
            return Response({"detail": "Không tìm thấy đơn hàng"}, status=404)
        
        # Chỉ cho phép cập nhật đơn hàng ở trạng thái pending
        if order.status != 'pending':
            return Response({
                "detail": "Chỉ có thể chỉnh sửa đơn hàng ở trạng thái chờ xác nhận"
            }, status=400)

        # Validate và cập nhật dữ liệu
        from hr.serializers.order import OrderSerializer
        
        # Tạo data dict với các fields cho phép update
        update_data = {}
        allowed_fields = [
            'service_type', 'area_m2', 'preferred_start_time', 
            'preferred_end_time', 'requested_hours', 'estimated_hours', 
            'cost_confirm', 'note'
        ]
        
        for field in allowed_fields:
            if field in request.data:
                value = request.data[field]
                # Convert datetime strings to proper format if needed
                if field in ['preferred_start_time', 'preferred_end_time']:
                    if isinstance(value, str):
                        from datetime import datetime
                        import pytz
                        try:
                            # Parse ISO format datetime
                            dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
                            update_data[field] = dt
                        except ValueError:
                            print(f"DEBUG: Invalid datetime format for {field}: {value}")
                            return Response({
                                "detail": f"Invalid datetime format for {field}"
                            }, status=400)
                    else:
                        update_data[field] = value
                elif field in ['area_m2', 'requested_hours', 'estimated_hours', 'cost_confirm']:
                    # Convert numeric fields
                    if value is not None and value != '':
                        try:
                            from decimal import Decimal
                            update_data[field] = Decimal(str(value))
                        except (ValueError, TypeError):
                            print(f"DEBUG: Invalid numeric format for {field}: {value}")
                            return Response({
                                "detail": f"Invalid numeric format for {field}"
                            }, status=400)
                    else:
                        if field == 'cost_confirm':
                            update_data[field] = None  # cost_confirm can be null
                        else:
                            print(f"DEBUG: Required field {field} is empty")
                            return Response({
                                "detail": f"Field {field} is required"
                            }, status=400)
                else:
                    update_data[field] = value
        
        print(f"DEBUG: Update data: {update_data}")
        
        serializer = OrderSerializer(order, data=update_data, partial=True)
        
        print(f"DEBUG: Serializer validation: {serializer.is_valid()}")
        if not serializer.is_valid():
            print(f"DEBUG: Serializer errors: {serializer.errors}")
            return Response({
                "detail": "Dữ liệu không hợp lệ",
                "errors": serializer.errors
            }, status=400)
        
        try:
            serializer.save()
            print(f"DEBUG: Order updated successfully")
            return Response(serializer.data)
        except Exception as e:
            print(f"DEBUG: Error saving order: {str(e)}")
            return Response({
                "detail": f"Lỗi khi lưu đơn hàng: {str(e)}"
            }, status=400)