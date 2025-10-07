import json
from django.http import HttpResponse
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_406_NOT_ACCEPTABLE,
    HTTP_500_INTERNAL_SERVER_ERROR
)
from hr.models.customer import Customer
from hr.serializers.customer import CustomerSerializer

from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_nested_forms.utils import NestedForm
from oauthlib.oauth2.rfc6749.utils import list_to_scope
from oauth2_provider.views.mixins import OAuthLibMixin
from oauth2_provider.signals import app_authorized
from oauth2_provider.models import get_access_token_model
from django.contrib.auth import get_user_model
from common.constants import Http
from core.settings.base import (
    BUSINESS_CLIENT_ID,
    BUSINESS_CLIENT_SECRET,
)
from base.views.base import BaseViewSet
from base.services import Verification
from oauth.serializers import UserShortSerializer
from oauth.permissions import IsAdministrator
from ..models import Employee
from ..serializers import EmployeeSerializer
from ..services import EmployeeService
from django.db.models import Q
from django.core.paginator import Paginator
from rest_framework import status

User = get_user_model()
AccessToken = get_access_token_model()

class EmployeeViewSet(OAuthLibMixin, BaseViewSet):
    queryset = Employee.objects.exclude(roles__name__in=["Super Administrator"]).order_by('-created_at', 'first_name', 'last_name')
    serializer_class = EmployeeSerializer
    search_map = {
        "first_name": "icontains",
        "last_name": "icontains",
        "work_mail": "icontains",
        "area": "icontains",
    }
    required_alternate_scopes = {
        "create": [["admin:employees:edit"], ["employees:edit"]],
        "update": [["admin:employees:edit"], ["employees:view"]],
        "destroy": [["admin:employees:edit"], ["employees:edit"]],
        "invite": [["admin:employees:edit"], ["employees:edit"]],
        "list": [["admin:employees:view"], ["employees:view-mine"]],
        "retrieve": [["admin:employees:view"], ["employees:view-mine"]],
        "admin_update": [["admin:edit"], ["admin:view"]]  

    }

    def update(self, request, *args, **kwargs):
        # Kiểm tra quyền admin
        if not request.user.is_superuser:  # Hoặc kiểm tra scope admin
            return Response(
                {"detail": "You do not have permission to update skills."},
                status=HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)
    
    # get_queryset để handle JWTUser
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Kiểm tra user scopes từ token
        if hasattr(self.request, 'auth') and self.request.auth:
            token_scopes = self.request.auth.scope.split() if self.request.auth.scope else []
            
            # Nếu user chỉ có scope employees:view-mine
            if 'employees:view-mine' in token_scopes and 'employees:view' not in token_scopes and 'admin:employees:view' not in token_scopes:
                try:
                    # Lấy User từ JWTUser
                    jwt_user = self.request.auth.user
                    real_user = User.objects.get(email=jwt_user.email)
                    return queryset.filter(user=real_user)
                except User.DoesNotExist:
                    # Nếu không tìm thấy user, return empty queryset
                    return queryset.none()
        
        return queryset

    # Sửa indentation - đưa list ra ngoài create()
    def list(self, request, *args, **kwargs):
        """Override list method to handle pagination and filtering properly"""
        try:
            # Get filtered queryset
            queryset = self.get_queryset()
            
            # Apply additional filters from query params
            search = request.query_params.get('search')
            if search:
                queryset = queryset.filter(
                    Q(first_name__icontains=search) |
                    Q(last_name__icontains=search) |
                    Q(work_mail__icontains=search) |
                    Q(phone__icontains=search) |
                    Q(area__icontains=search)
                )
            
            area = request.query_params.get('area')
            if area:
                queryset = queryset.filter(area__icontains=area)
            computed_status = request.query_params.get('computed_status')
            if computed_status is not None and computed_status != '':
                try:
                    status_value = int(computed_status)
                    
                    if status_value == 0:
                        # No working hours set
                        queryset = queryset.filter(
                            Q(working_start_time__isnull=True) | 
                            Q(working_end_time__isnull=True)
                        )
                    elif status_value in [1, 2]:
                        # Has working hours, filter by computed status
                        # This will be handled by serializer computation
                        queryset = queryset.filter(
                            working_start_time__isnull=False,
                            working_end_time__isnull=False
                        )
                        # Additional filtering will happen in serializer
                        
                except (ValueError, TypeError):
                    pass
            
            status_filter = request.query_params.get('status')
            if status_filter is not None and status_filter != '' and not computed_status:
                try:
                    status_value = int(status_filter)
                    queryset = queryset.filter(status=status_value)
                except (ValueError, TypeError):
                    pass
            
            
            # Get pagination parameters
            try:
                page = int(request.query_params.get('page', 1))
                page_size = int(request.query_params.get('page_size', 10))
            except (ValueError, TypeError):
                page = 1
                page_size = 10
            
            # Ensure reasonable limits
            page_size = min(max(page_size, 1), 100)  # Between 1 and 100
            page = max(page, 1)  # At least 1
            
            # Apply pagination
            paginator = Paginator(queryset, page_size)
            
            try:
                page_obj = paginator.get_page(page)
            except Exception as e:
                print(f"Pagination error: {e}")
                page_obj = paginator.get_page(1)  # Fallback to first page
            
            # Serialize data with error handling
            try:
                serializer = self.get_serializer(page_obj, many=True)
                serialized_data = serializer.data
                if computed_status is not None and computed_status != '':
                    try:
                        status_value = int(computed_status)
                        if status_value in [1, 2]:
                            # Filter serialized data by computed_status
                            serialized_data = [
                                item for item in serialized_data 
                                if item.get('computed_status') == status_value
                            ]
                    except (ValueError, TypeError):
                        pass
            except Exception as e:
                print(f"Serialization error: {e}")
                # Fallback: serialize without computed fields
                serialized_data = []
                for employee in page_obj:
                    try:
                        emp_serializer = self.get_serializer(employee)
                        serialized_data.append(emp_serializer.data)
                    except Exception as emp_error:
                        print(f"Error serializing employee {employee.id}: {emp_error}")
                        # Add minimal employee data
                        serialized_data.append({
                            'id': str(employee.id),
                            'first_name': employee.first_name or '',
                            'last_name': employee.last_name or '',
                            'work_mail': employee.work_mail or '',
                            'area': employee.area or '',
                            'status': employee.status,
                            'is_currently_active': False,
                            'current_status_text': 'Status unavailable'
                        })
            
            return Response({
                'results': serialized_data,
                'count': paginator.count,
                'num_pages': paginator.num_pages,
                'current_page': page,
                'page_size': page_size,
                'has_next': page_obj.has_next(),
                'has_previous': page_obj.has_previous(),
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            print(f"Error in employee list: {e}")
            import traceback
            traceback.print_exc()
            
            return Response({
                'results': [],
                'count': 0,
                'num_pages': 0,
                'current_page': 1,
                'page_size': 10,
                'has_next': False,
                'has_previous': False,
                'error': f"Error loading employees: {str(e)}"
            }, status=status.HTTP_200_OK) 

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        print("Create Employee with data:", data)
        origin = request.META.get("HTTP_ORIGIN")
        print("Origin:", origin)
        content_type = request.content_type
        print("Content-Type:", content_type)
        if content_type is not None and 'form-data' in content_type:
            form = NestedForm(request.data)
            if form.is_nested():
                data = form.data

        email = data.get("work_mail")
        print("Employee email:", email)
        first_name = data.get("first_name")
        print("Employee first name:", first_name)
        last_name = data.get("last_name")
        print("Employee last name:", last_name)
        user = data.get("user", None)
        # only create user after they verify their email
        if user is not None:
            del data['user']
        try:
            user_id = User.objects.get(email=email).id.urn[9:]
        except User.DoesNotExist:
            user_id = None
        
        serializer = self.get_serializer(data=data)
        if serializer.is_valid(raise_exception=True):
            instance = serializer.save() 
            self.perform_create(serializer)
            self.clear_querysets_cache()
            try:
                employee_id = serializer.data.get('id')
                EmployeeService.verify_employee_email(
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    employee_id=employee_id,
                    user_id=user_id,
                    origin=origin
                )
            except Exception as e:
                print(e)
                Response({"message": _("There is an error occur.")}, status=HTTP_500_INTERNAL_SERVER_ERROR)
            response_serializer = self.get_serializer(instance)
            return Response(serializer.data, status=HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # Kiểm tra permission cho employees:view-mine
        if hasattr(request, 'auth') and request.auth:
            token_scopes = request.auth.scope.split() if request.auth.scope else []
            
            # Nếu user chỉ có scope employees:view-mine, chỉ cho xem profile của chính mình
            if 'employees:view-mine' in token_scopes and 'employees:view' not in token_scopes and 'admin:employees:view' not in token_scopes:
                try:
                    # ✅ Lấy User từ JWTUser
                    jwt_user = request.auth.user
                    real_user = User.objects.get(email=jwt_user.email)
                    
                    if instance.user != real_user:
                        return Response(
                            {"detail": "You do not have permission to view this employee."},
                            status=HTTP_403_FORBIDDEN
                        )
                except User.DoesNotExist:
                    return Response(
                        {"detail": "User not found."},
                        status=HTTP_404_NOT_FOUND
                    )
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(
    detail=False, 
    methods=[Http.HTTP_GET], 
    url_path="my-profile", 
    permission_classes=[IsAuthenticated]
    )
    def my_profile(self, request, *args, **kwargs):
        """Get current user's employee profile"""
        try:
            
            jwt_user = request.auth.user

            user_email = None
            user_id = None
            
            # Từ JWT user attributes
            if hasattr(jwt_user, 'email') and jwt_user.email:
                user_email = jwt_user.email
            
            # Từ JWT user id
            elif hasattr(jwt_user, 'id') and jwt_user.id:
                user_id = jwt_user.id
            
            # Từ JWT user username
            elif hasattr(jwt_user, 'username') and jwt_user.username:
                user_email = jwt_user.username  # Thường username = email
            
            # Từ access token
            elif hasattr(request.auth, 'user') and request.auth.user != jwt_user:
                real_token_user = request.auth.user
                if hasattr(real_token_user, 'email'):
                    user_email = real_token_user.email
            
            # Tìm User trong database
            real_user = None
            if user_email:
                try:
                    real_user = User.objects.get(email=user_email)
                except User.DoesNotExist:
                    print(f"User not found with email: {user_email}")
            elif user_id:
                try:
                    real_user = User.objects.get(id=user_id)
                    user_email = real_user.email
                except User.DoesNotExist:
                    print(f"User not found with ID: {user_id}")
            
            if not real_user:
                return Response(
                    {"detail": "Cannot determine user from JWT token"},
                    status=HTTP_404_NOT_FOUND
                )
            
            # Tìm employee bằng User object
            try:
                employee = Employee.objects.get(user=real_user)
                
                serializer = self.get_serializer(employee)
                return Response(serializer.data, status=HTTP_200_OK)
                
            except Employee.DoesNotExist:
                
                # Debug: Kiểm tra employees trong DB
                all_employees = Employee.objects.all()
                # print(f"Total employees in DB: {all_employees.count()}")
                for emp in all_employees[:5]:
                    user_info = f"User: {emp.user}" if emp.user else "User: None"
                    # print(f"  - Employee: {emp.work_mail}, {user_info}")
                
                # Alternative: Tìm employee bằng email
                try:
                    employee_by_email = Employee.objects.get(work_mail=user_email)
                    # print(f"Found employee by email: {employee_by_email.work_mail}")
                    
                    # Link employee với user nếu chưa có
                    if not employee_by_email.user:
                        employee_by_email.user = real_user
                        employee_by_email.save()
                        # print(f"Linked employee {employee_by_email.work_mail} with user {real_user.email}")
                    
                    serializer = self.get_serializer(employee_by_email)
                    return Response(serializer.data, status=HTTP_200_OK)
                    
                except Employee.DoesNotExist:
                    return Response(
                        {"detail": f"Employee profile not found for user: {user_email}"},
                        status=HTTP_404_NOT_FOUND
                    )
                
        except Exception as e:
            print(f"Error in my_profile: {e}")
            import traceback
            traceback.print_exc()
            
            return Response(
                {"detail": f"Error retrieving profile: {str(e)}"},
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    # ✅ Fix update_my_profile to be consistent
    @action(
        detail=False, 
        methods=["PATCH"], # Allow both PATCH and POST
        url_path="update-my-profile", 
        permission_classes=[IsAuthenticated]
    )
    def update_my_profile(self, request, *args, **kwargs):
        """Update current user's employee profile (chỉ cho phép sửa các trường cơ bản)"""
        try:
            print("==> update_my_profile called")
            # Lấy User từ JWTUser
            jwt_user = request.auth.user
            print(f"JWT user: {vars(jwt_user)}")
            print(f"JWT user email: {getattr(jwt_user, 'email', None)}")
            real_user = User.objects.get(email=jwt_user.email)
            print(f"Real user: {real_user}")

            # Tìm employee bằng real User hoặc email
            try:
                employee = Employee.objects.get(user=real_user)
                print(f"Found employee by user: {employee}")
            except Employee.DoesNotExist:
                print("Employee not found by user, try by work_mail")
                # Fallback: tìm bằng email
                employee = Employee.objects.get(work_mail=real_user.email)
                print(f"Found employee by work_mail: {employee}")
                # Link employee với user
                employee.user = real_user
                employee.save()
                print("Linked employee with user")

            # Chỉ cho phép update một số fields nhất định
            allowed_fields = [
                'first_name', 'last_name', 'personal_mail', 
                'phone', 'gender', 'date_of_birth',
                'area', 'working_start_time', 'working_end_time',
            ]
            print(f"Request data: {request.data}")
            update_data = {}
            for field in allowed_fields:
                if field in request.data:
                    update_data[field] = request.data[field]
            print(f"Update data: {update_data}")

            # Validate và update
            serializer = self.get_serializer(employee, data=update_data, partial=True)
            try:
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    print("Profile updated successfully")
                    return Response(serializer.data, status=HTTP_200_OK)
            except Exception as e:
                print(f"Serializer error: {e}")
                import traceback
                traceback.print_exc()
                return Response(
                    {"detail": f"Serializer error: {str(e)}"},
                    status=HTTP_400_BAD_REQUEST
                )

        except User.DoesNotExist as e:
            print(f"User.DoesNotExist: {e}")
            import traceback
            traceback.print_exc()
            return Response(
                {"detail": "User not found."},
                status=HTTP_404_NOT_FOUND
            )
        except Employee.DoesNotExist as e:
            print(f"Employee.DoesNotExist: {e}")
            import traceback
            traceback.print_exc()
            return Response(
                {"detail": "Employee profile not found."},
                status=HTTP_404_NOT_FOUND
            )
        except Exception as e:
            print(f"Error updating profile: {e}")
            import traceback
            traceback.print_exc()
            return Response(
                {"detail": f"Error updating profile: {str(e)}"},
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )
            
    @action(detail=True, methods=[Http.HTTP_POST], url_path="invite")
    def invite(self, request, *args, **kwargs):
        instance = self.get_object()  
        email = instance.work_mail
        first_name = instance.first_name
        last_name = instance.last_name
        employee_id = instance.id.urn[9:]
        origin = request.META.get("HTTP_ORIGIN")

        try:
            user_id = User.objects.get(email=email).id.urn[9:]
        except User.DoesNotExist:
            user_id = None
        
        try:
            EmployeeService.verify_employee_email(
                email=email,
                first_name=first_name,
                last_name=last_name,
                employee_id=employee_id,
                user_id=user_id,
                origin=origin
            )
            Response({"message": _("The invitation have been sent.")}, status=HTTP_200_OK)
        except Exception as e:
            print(e)
            Response({"message": _("There is an error occur.")}, status=HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({"message": _("The invitation have been sent.")}, status=HTTP_200_OK)
    
    @action(detail=False, methods=[Http.HTTP_POST], url_path="verify", permission_classes=[AllowAny], authentication_classes=[])
    def verify(self, request, *args, **kwargs):
        content_type = request.content_type
        data = request.data.copy()
        if content_type is not None and 'form-data' in content_type:
            form = NestedForm(request.data)
            if form.is_nested():
                data = form.data
        
        employee_id = data.get('employee_id', None)
        if employee_id is None:
            return Response(
                {"error": _("Invalid employee id.")},
                status=HTTP_406_NOT_ACCEPTABLE
            )
        else:
            del data['employee_id']

        user_id = data.get('user_id', None)
        if user_id is not None:
            del data['user_id']

        token = data.get('token', None)
        if token is not None:
            del data['token']

        password = data.get('password')
        if password is not None:
            del data['password']
        email = data.get('email')

        try:
            # Check if the token were isssued to the right people
            token_payload = Verification.decode_token(token)
            token_email = token_payload.get('email')
            if email is not None and token_email != email:
                return Response(
                    {"error": _("Invalid token")},
                    status=HTTP_406_NOT_ACCEPTABLE
                )
        except Exception as e:
            print(e)
            return Response(
                {"error": _("Invalid token")},
                status=HTTP_406_NOT_ACCEPTABLE,
            )
        try:
            employee = Employee.objects.get(pk=employee_id)
            # user, created = User.objects.get_or_create(defaults=None,**data)
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = User.objects.create(**data)
            if user is not None and password is not None:
                user.set_password(password)
                user.save()

            if employee is not None and user is not None:
                employee.user = user
                employee.save()
        except Exception as e:
            print(e)
            return Response(
                {"error": _("User not found.")},
                status=HTTP_404_NOT_FOUND
            )
        return Response({"message": _("Verified")}, status=HTTP_200_OK)
    
    @action(detail=False, methods=[Http.HTTP_POST], url_path="login", permission_classes=[AllowAny], authentication_classes=[])
    def login(self, request, pk=None):
        try:
            # user_name = request.POST.get("username")
            user_name = request.data.get("username")  # đọc từ JSON
            password = request.data.get("password")
            user = User.objects.prefetch_related("employees").get(email=user_name)
            
        except User.DoesNotExist:
            return Response(
                    {"error": _("The user does not exist.")},
                    status=HTTP_404_NOT_FOUND,
                )
        scopes = set()
        # Employee permissions
        if user.employees:
            employee = user.employees.first()
            if employee is not None:
                if employee.roles is not None:
                    for role in  employee.roles.all():
                        scopes = scopes.union(set(role.scopes.keys()))
           
        request.POST._mutable = True
        request.POST.update(
            {
                "grant_type": "password",
                "client_type": "confidential",
                "client_id": BUSINESS_CLIENT_ID,
                "client_secret": BUSINESS_CLIENT_SECRET
            }
        )
        if len(scopes) > 0:
            request.POST.update({"scope": list_to_scope(scopes)})

        url, headers, body, status = self.create_token_response(request)
        if status == 200:
            access_token = json.loads(body).get("access_token")
            if access_token is not None:
                token = AccessToken.objects.get(token=access_token)
                app_authorized.send(sender=self, request=request, token=token)
        response = HttpResponse(content=body, status=status)

        for k, v in headers.items():
            response[k] = v
        return response
   


    @action(detail=False, methods=[Http.HTTP_POST], url_path="refresh-token", permission_classes=[AllowAny], authentication_classes=[])
    def refreshToken(self, request):
        request.POST._mutable = True
        refresh_token =  request.POST.get("refresh_token")
        if not refresh_token or refresh_token == 'null':
            return Response(
                {"error": _("Invalid token")},
                status=HTTP_406_NOT_ACCEPTABLE,
            )
        request.POST.update(
            {
                "grant_type": "refresh_token",
                "client_id": BUSINESS_CLIENT_ID,
                "client_secret": BUSINESS_CLIENT_SECRET,
                "refresh_token": refresh_token,
            }
        )
        url, headers, body, status = self.create_token_response(request)
        if status == 200:
            access_token = json.loads(body).get("access_token")
            if access_token is not None:
                token =AccessToken.objects.get(token=access_token)
                app_authorized.send(sender=self, request=request, token=token)
        response = HttpResponse(content=body, status=status)

        for k, v in headers.items():
            response[k] = v
        return response

    @action(detail=False, methods=[Http.HTTP_POST], url_path="logout", permission_classes=[IsAuthenticated])
    def logout(self, request, pk=None):
        request.POST._mutable = True
        refresh_token = request.POST.get("refresh_token")
        access_token = request.POST.get("access_token")

        # revoke refresh_token first, to make user can not renew access_token
        request.POST.update(
            {
                "client_id": BUSINESS_CLIENT_ID,
                "client_secret": BUSINESS_CLIENT_SECRET,
                "token_type_hint": "refresh_token",
                "token": refresh_token,
            }
        )
        url, headers, body, status = self.create_revocation_response(request)
        if status != HTTP_200_OK:
            return Response(
                {"error": _("Can not revoke refresh token.")},
                status=HTTP_400_BAD_REQUEST,
            )

        # revoke access_token
        request.POST.update(
            {
                "token_type_hint": "access_token",
                "token": access_token,
            }
        )
        url, headers, body, status = self.create_revocation_response(request)
        if status != HTTP_200_OK:
            return Response(
                content={"error": _("Can not revoke access token.")},
                status=HTTP_400_BAD_REQUEST,
            )

        return Response({"message": _("Logout success!")}, status=HTTP_200_OK)
    
    @action(detail=False, methods=[Http.HTTP_POST], url_path="forgot_password", permission_classes=[AllowAny], authentication_classes=[])
    def forgot_password(self, request, *args, **kwargs):
        email = request.data.get("email")
        
        try:
            EmployeeService.send_forgot_password_email(email=email)
            return Response({"message": _("The link has been sent.")}, status=HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({"message": _("An error occurred.")}, status=HTTP_500_INTERNAL_SERVER_ERROR)
        
    
    
    
    @action(detail=False, methods=[Http.HTTP_POST], url_path="reset_password", permission_classes=[AllowAny], authentication_classes=[])
    def reset_password(self, request, *args, **kwargs):
        token = request.data.get("token")
        new_password = request.data.get("password")
        
        try:
            EmployeeService.set_password(token=token, new_password=new_password)
            return Response({"message": _("Password has been reset.")}, status=HTTP_200_OK)

        except ValueError as ve:
            return Response({"message": str(ve)}, status=HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(e)
            return Response({"message": _("An error occurred.")}, status=HTTP_500_INTERNAL_SERVER_ERROR)
        
            
    
    @action(detail=False, methods=["POST"], url_path="change-password", permission_classes=[AllowAny], authentication_classes=[])
    def change_password(self, request, *args, **kwargs):
        email = request.data.get("email")
        current_password = request.data.get("current_password")
        new_password = request.data.get("new_password")
        
        try:
            EmployeeService.change_password(email=email, current_password=current_password, new_password=new_password)
            return Response({"message": _("Password has been changed.")}, status=HTTP_200_OK)

        except ValueError as ve:
            return Response({"message": str(ve)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(e)
            return Response({"message": _("An error occurred.")}, status=HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=[Http.HTTP_GET], url_path="userinfo", permission_classes=[IsAuthenticated])
    def userinfo(self, request, *args, **kwargs):
        try:
            id = request.auth.user.id
            user = get_object_or_404(User.objects.all(), id=id)
            user_serializer= UserShortSerializer(user)
            user_data = user_serializer.data
            return Response(user_data, status=HTTP_200_OK)
        except Exception as e:
            return Response({"message": _("Business not found.")}, status=HTTP_404_NOT_FOUND)

    @action(detail=False, methods=[Http.HTTP_GET], url_path="scopes", permission_classes=[IsAdministrator])
    def scopes(self, request, pk=None):
        from oauth2_provider.scopes import get_scopes_backend
        scopes_backend = get_scopes_backend()
        all_scopes = scopes_backend.get_all_scopes()
        default_scopes = scopes_backend.get_default_scopes()
        # scopes = {name: desc for name, desc in all_scopes.items() if name in business_scopes}
        # default_scopes = [name for name in default_scopes if name in business_scopes]
        
        return Response({ "scopes" :all_scopes, "default_scopes": default_scopes }, status=HTTP_200_OK)
    
    @action(
        detail=True,  # detail=True để có thể truyền ID trong URL
        methods=["PATCH"], 
        url_path="admin-update", 
        permission_classes=[IsAuthenticated]
    )
    def admin_update(self, request, *args, **kwargs):
        """Admin action to update employee information"""
        try:
            print("==> admin_update called")
            print("Request data:", request.data)
            # Kiểm tra admin permissions
            if hasattr(request, 'auth') and request.auth:
                token_scopes = request.auth.scope.split() if request.auth.scope else []
                print("Token scopes:", token_scopes)
                # Kiểm tra scope admin
                required_scopes = ['admin:edit', 'admin:view']
                has_admin_permission = any(scope in token_scopes for scope in required_scopes)
                print("Has admin permission:", has_admin_permission)
                if not has_admin_permission:
                    return Response(
                        {"detail": "You do not have admin permission to perform this action."},
                        status=HTTP_403_FORBIDDEN
                    )
            
            # Lấy employee instance
            employee = self.get_object()
            print("Employee instance:", employee)

            # Fields mà admin được phép update
            admin_allowed_fields = [
                'first_name', 'last_name', 'personal_mail', 
                'phone', 'gender', 'date_of_birth', 'area', 
                'working_start_time', 'working_end_time', 
                'skills','status', 'office_id'
            ]
            
            # Lọc data chỉ lấy các fields được phép
            update_data = {}
            for field in admin_allowed_fields:
                if field in request.data:
                    update_data[field] = request.data[field]
            print("Update data:", update_data)
            
            # Validate và update
            serializer = self.get_serializer(employee, data=update_data, partial=True)
            print("Serializer initial data:", serializer.initial_data)
            if serializer.is_valid(raise_exception=True):
                print("Serializer validated data:", serializer.validated_data)
                serializer.save()
                print("Employee updated successfully")
                return Response(serializer.data, status=HTTP_200_OK)
                
        except Employee.DoesNotExist:
            print("Employee.DoesNotExist")
            return Response(
                {"detail": "Employee not found."},
                status=HTTP_404_NOT_FOUND
            )
        except Exception as e:
            print(f"Error in admin_update: {e}")
            import traceback
            traceback.print_exc()
            return Response(
                {"detail": f"Error updating employee: {str(e)}"},
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )