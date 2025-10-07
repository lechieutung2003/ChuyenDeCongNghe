from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from hr.serializers.full_user import FullUserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from hr.serializers.register_customer import RegisterCustomerSerializer
from hr.serializers.customer import CustomerSerializer
from rest_framework.permissions import AllowAny
from hr.models import Employee, Assignment
from hr.models.customer import Customer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from hr.serializers import AssignmentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from hr.models.order import Order
from hr.serializers.order import OrderSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class UserInfoAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        serializer = FullUserSerializer(user)
        return Response(serializer.data)


class CustomerInfoAPIView(APIView):
    """API để lấy thông tin chi tiết của customer từ bảng hr_customer"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            # Lấy user từ JWT token
            jwt_user = request.auth.user if hasattr(request, 'auth') and request.auth else request.user
            
            # Tìm customer bằng email hoặc user
            customer = None
            
            # Thử tìm customer bằng user relationship trước
            if hasattr(jwt_user, 'email') and jwt_user.email:
                try:
                    # Tìm real user trong database
                    real_user = User.objects.get(email=jwt_user.email)
                    customer = Customer.objects.get(user=real_user)
                except (User.DoesNotExist, Customer.DoesNotExist):
                    pass
            
            # Nếu chưa tìm thấy, thử tìm bằng email
            if not customer and hasattr(jwt_user, 'email') and jwt_user.email:
                try:
                    customer = Customer.objects.get(email=jwt_user.email)
                    
                    # Link customer với user nếu chưa có
                    if not customer.user:
                        try:
                            real_user = User.objects.get(email=jwt_user.email)
                            customer.user = real_user
                            customer.save()
                        except User.DoesNotExist:
                            pass
                            
                except Customer.DoesNotExist:
                    pass
            
            if not customer:
                return Response(
                    {"detail": "Customer profile not found"},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            serializer = CustomerSerializer(customer)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except Exception as e:
            print(f"Error in CustomerInfoAPIView: {e}")
            import traceback
            traceback.print_exc()
            
            return Response(
                {"detail": f"Error retrieving customer info: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class RegisterCustomerAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        print(f"Request data: {request.data}")  # Log data nhận được
        serializer = RegisterCustomerSerializer(data=request.data)
        if serializer.is_valid():
            customer = serializer.save()
            return Response(serializer.to_representation(customer), status=status.HTTP_201_CREATED)
        print(f"Serializer errors: {serializer.errors}")  # Log lỗi validation
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

