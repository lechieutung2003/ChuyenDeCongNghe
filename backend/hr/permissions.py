from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff

class IsEmployee(permissions.BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'role') and request.user.role == 'employee'

class IsCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
        # Kiểm tra user có liên kết với Customer
        return hasattr(request.user, 'hr_customer') and request.user.hr_customer is not None
class IsEmployeeOrStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, "employee") or request.user.is_staff
