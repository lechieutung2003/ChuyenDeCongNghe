from base.views import BaseViewSet
from rest_framework import viewsets, permissions
from ..models import Order, Assignment, DecisionLog
from ..models.customer import Customer, ServiceType
from ..serializers.order import (
    OrderSerializer, OrderEmployeeSerializer, AssignmentSerializer, DecisionLogSerializer,
    CustomerSerializer, ServiceTypeSerializer
)
from rest_framework.decorators import action
from rest_framework.response import Response
from common.constants.http import Http
from django.db.models import Q
from hr.permissions import IsAdmin, IsEmployee, IsCustomer
from businesses.models.employee import EmployeeWorkingStatus
from rest_framework import status
from decimal import Decimal

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    def get_permissions(self):
        if self.request.user and self.request.user.is_staff:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

class ServiceTypeViewSet(viewsets.ModelViewSet):
    queryset = ServiceType.objects.all().order_by('id')
    serializer_class = ServiceTypeSerializer
    permission_classes = [permissions.IsAuthenticated]

class OrderViewSet(BaseViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    search_map = {
        "status": "iexact",
        "customer__name": "icontains",
        "note": "icontains",
    }
    required_alternate_scopes = {
        "create": [["roles:edit"]],
        "retrieve": [["roles:edit"], ["roles:view"]],
        "update": [["roles:edit"]],
        "destroy": [["roles:edit"]],
        "list": [["roles:edit"], ["roles:view"]],
        "get_assignments": [["roles:edit"], ["roles:view"]],
        "updateStatus": [["roles:edit"]],
        "update_admin_log": [["roles:edit"]],
        "complete": [["roles:edit"]]
    }

    def get_serializer_class(self):
        """Trả về serializer phù hợp dựa trên role của user"""
        user = self.request.user
        
        # Nếu là JWTUser, lấy User thật từ database
        if hasattr(user, 'id'):
            from oauth.models import User
            try:
                real_user = User.objects.get(id=user.id)
                
                # Check if user is employee
                if hasattr(real_user, 'employees') and real_user.employees.exists():
                    if self.action in ['update', 'partial_update']:
                        return OrderEmployeeSerializer
            except User.DoesNotExist:
                pass
        
        return OrderSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date:
            queryset = queryset.filter(preferred_start_time__gte=start_date)
        if end_date:
            queryset = queryset.filter(preferred_start_time__lte=end_date)
        
        user = self.request.user
        if user.is_staff:
            return queryset
        
        # Nếu là JWTUser, lấy User thật từ database
        if hasattr(user, 'id'):
            from oauth.models import User
            try:
                real_user = User.objects.get(id=user.id)
                if hasattr(real_user, 'employees') and real_user.employees.exists():
                    return queryset.filter(assignment__employee__user=real_user)
            except User.DoesNotExist:
                pass
        
        return queryset.none()

    def get_permissions(self):
        user = self.request.user
        if user.is_staff:
            return [permissions.IsAdminUser()]
        
        # Nếu là JWTUser, lấy User thật từ database
        if hasattr(user, 'id'):
            from oauth.models import User
            try:
                real_user = User.objects.get(id=user.id)
                if hasattr(real_user, 'employees') and real_user.employees.exists():
                    if self.action in ['list', 'retrieve', 'assignments']:
                        return [permissions.IsAuthenticated(), IsEmployee()]
                    elif self.action in ['update', 'partial_update']:
                        # Cho phép employee update (chỉ status thông qua OrderEmployeeSerializer)
                        return [permissions.IsAuthenticated(), IsEmployee()]
                    return [permissions.IsAdminUser()]
            except User.DoesNotExist:
                pass
        
        return super().get_permissions()

    @action(methods=[Http.HTTP_GET, Http.HTTP_POST], detail=True, url_path="assignments")
    def assignments(self, request, pk=None):
        order = self.get_object()
        
        if request.method == 'GET':
            assignments = Assignment.objects.filter(order=order)
            serializer = AssignmentSerializer(assignments, many=True)
            return Response(serializer.data)
            
        elif request.method == 'POST':
            created_assignments = []
            print("Received data:", request.data)  # Thêm log để debug
            
            for assignment_data in request.data:
                assignment_data['order'] = order.id
                serializer = AssignmentSerializer(data=assignment_data)
                print("Validating data:", assignment_data)  # Thêm log để debug
                
                if serializer.is_valid():
                    assignment = serializer.save()
                    employee = assignment.employee
                    employee.status = EmployeeWorkingStatus.INACTIVE
                    employee.save()
                    created_assignments.append(assignment)
                else:
                    print("Validation errors:", serializer.errors)  # Thêm log để debug
                    return Response(
                        {
                            "detail": "Dữ liệu không hợp lệ",
                            "errors": serializer.errors
                        }, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            result_serializer = AssignmentSerializer(created_assignments, many=True)
            return Response(result_serializer.data, status=status.HTTP_201_CREATED)
        
    @action(methods=['PATCH'], detail=True, url_path="updateStatus")
    def updateStatus(self, request, pk=None):
        """
        API endpoint để cập nhật trạng thái đơn hàng
        """
        order = self.get_object()
        old_status = order.status
        
        if 'status' not in request.data:
            return Response({"detail": "Missing status field"}, status=status.HTTP_400_BAD_REQUEST)
        
        new_status = request.data['status']
        valid_statuses = ['pending', 'confirmed', 'in_progress', 'completed', 'rejected']
        
        if new_status not in valid_statuses:
            return Response({"detail": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)
            
        order.status = new_status
        order.save()
        
        serializer = self.get_serializer(order)
        return Response(serializer.data)
    
    @action(methods=['PATCH'], detail=True, url_path="admin-log")
    def update_admin_log(self, request, pk=None):
        """
        API endpoint để cập nhật admin_log của đơn hàng
        """
        order = self.get_object()
        
        print("="*50)
        print(f"UPDATE ADMIN LOG REQUEST: Order ID={pk}")
        print(f"Request data: {request.data}")

        # Kiểm tra dữ liệu đầu vào
        if 'admin_log' not in request.data:
            # Kiểm tra xem có trường reason không (để tương thích với code cũ)
            if 'reason' in request.data:
                order.admin_log = request.data['reason']
            else:
                return Response(
                    {"detail": "Missing admin_log field"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            admin_log = request.data['admin_log']
            # Kiểm tra nếu admin_log là dict có chứa reason
            if isinstance(admin_log, dict) and 'reason' in admin_log:
                order.admin_log = admin_log['reason']
            else:
                # Lưu admin_log trực tiếp
                order.admin_log = admin_log
        
        # Lưu thay đổi
        order.save()
        
        print(f"Admin log updated for order {pk}")
        print(f"New log: {order.admin_log}")
        if 'status' in request.data:
            print(f"Status updated to: {order.status}")
        
        # Trả về đơn hàng đã cập nhật
        serializer = self.get_serializer(order)
        return Response(serializer.data)
    
    @action(methods=['POST'], detail=True, url_path="complete")
    def complete_order(self, request, pk=None):
        order = self.get_object()
        print(f"Completing order {order.id}")
        requested_hours = Decimal(str(order.requested_hours))  # Sửa ở đây
        print(f"Requested hours: {requested_hours}")
        assignments = Assignment.objects.filter(order=order)
        print(f"Found {assignments.count()} assignments")
        for assignment in assignments:
            employee = assignment.employee
            employee.total_hours_worked = (employee.total_hours_worked or Decimal('0')) + requested_hours
            employee.completed_orders_count = (employee.completed_orders_count or 0) + 1
            employee.status = EmployeeWorkingStatus.ACTIVE
            employee.save()
        assignments.delete()
        return Response({"detail": "Đã hoàn thành đơn hàng và cập nhật nhân viên."}, status=status.HTTP_200_OK)
    

class AssignmentViewSet(BaseViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    required_alternate_scopes = {
        "create": [["roles:edit"]],
        "retrieve": [["assignments:view"], ["roles:edit"]],
        "update": [["roles:edit"]],
        "destroy": [["roles:edit"]],
        "list": [["assignments:view"], ["roles:edit"]],
    }
