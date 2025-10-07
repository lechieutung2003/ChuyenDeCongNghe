from hr.models import Employee, Assignment
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from hr.serializers import AssignmentSerializer

class EmployeeOrdersAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = getattr(request.user, "id", None)  # lấy user_id từ JWTUser
        if not user_id:
            return Response({"detail": "Không xác định được user"}, status=403)

        try:
            employee = Employee.objects.get(user_id=user_id)
        except Employee.DoesNotExist:
            return Response({"detail": "User không phải là nhân viên"}, status=403)

        # Kiểm tra role Staff
        is_staff_role = employee.roles.filter(name="Employee").exists()
        if not is_staff_role:
            return Response({"detail": "User không có role Staff"}, status=403)

        assignments = Assignment.objects.filter(employee=employee)
        serializer = AssignmentSerializer(assignments, many=True)
        return Response(serializer.data)
