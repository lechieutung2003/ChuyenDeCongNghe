"""
Django Filters for Employee management
"""
import django_filters
from django.db.models import Q
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters as drf_filters

from ..models import Employee
from oauth.models import User


class EmployeeFilter(django_filters.FilterSet):
    """
    Advanced filtering for Employee model using django-filter
    """
    
    # Text search across multiple fields
    search = django_filters.CharFilter(
        method='filter_search',
        help_text="Search across first_name, last_name, work_mail, phone, area"
    )
    
    # Area filtering with multiple options
    area = django_filters.CharFilter(
        field_name='area',
        lookup_expr='icontains',
        help_text="Filter by work area (case insensitive)"
    )
    
    # Status filtering with choices
    status = django_filters.ChoiceFilter(
        field_name='status',
        choices=Employee._meta.get_field('status').choices,
        help_text="Filter by working status"
    )
    
    # Computed status filtering (custom method)
    computed_status = django_filters.NumberFilter(
        method='filter_computed_status',
        help_text="Filter by computed working status (0=no hours, 1=active, 2=inactive)"
    )
    
    # Date range filters
    join_date_after = django_filters.DateFilter(
        field_name='join_date',
        lookup_expr='gte',
        help_text="Filter employees who joined after this date"
    )
    
    join_date_before = django_filters.DateFilter(
        field_name='join_date', 
        lookup_expr='lte',
        help_text="Filter employees who joined before this date"
    )
    
    # Age range filters (using date_of_birth)
    born_after = django_filters.DateFilter(
        field_name='date_of_birth',
        lookup_expr='gte',
        help_text="Filter employees born after this date"
    )
    
    born_before = django_filters.DateFilter(
        field_name='date_of_birth',
        lookup_expr='lte',
        help_text="Filter employees born before this date"
    )
    
    # Salary range filters
    salary_min = django_filters.NumberFilter(
        field_name='salary',
        lookup_expr='gte',
        help_text="Minimum salary filter"
    )
    
    salary_max = django_filters.NumberFilter(
        field_name='salary',
        lookup_expr='lte',
        help_text="Maximum salary filter"
    )
    
    # Working hours filters
    has_working_hours = django_filters.BooleanFilter(
        method='filter_has_working_hours',
        help_text="Filter employees with/without working hours set"
    )
    
    # Performance filters
    min_orders = django_filters.NumberFilter(
        field_name='completed_orders_count',
        lookup_expr='gte',
        help_text="Filter by minimum completed orders"
    )
    
    max_hours = django_filters.NumberFilter(
        field_name='total_hours_worked',
        lookup_expr='lte',
        help_text="Filter by maximum hours worked"
    )
    
    # Gender filter
    gender = django_filters.ChoiceFilter(
        field_name='gender',
        choices=[
            ('male', 'Male'),
            ('female', 'Female'),
            ('other', 'Other'),
        ],
        help_text="Filter by gender"
    )
    
    # Multiple area selection
    areas = django_filters.BaseInFilter(
        field_name='area',
        lookup_expr='in',
        help_text="Filter by multiple areas (comma-separated)"
    )
    
    # User-related filters
    has_user_account = django_filters.BooleanFilter(
        field_name='user',
        lookup_expr='isnull',
        exclude=True,
        help_text="Filter employees with/without user accounts"
    )
    
    class Meta:
        model = Employee
        fields = {
            'first_name': ['exact', 'icontains', 'istartswith'],
            'last_name': ['exact', 'icontains', 'istartswith'],  
            'work_mail': ['exact', 'icontains'],
            'personal_mail': ['exact', 'icontains'],
            'phone': ['exact', 'icontains'],
            'area': ['exact', 'icontains'],
            'status': ['exact'],
            'join_date': ['exact', 'gte', 'lte', 'year', 'month'],
            'date_of_birth': ['exact', 'gte', 'lte', 'year'],
            'salary': ['exact', 'gte', 'lte', 'isnull'],
            'completed_orders_count': ['exact', 'gte', 'lte'],
            'total_hours_worked': ['exact', 'gte', 'lte'],
            'gender': ['exact'],
        }
    
    def filter_search(self, queryset, name, value):
        """
        Custom search filter across multiple fields
        """
        if not value:
            return queryset
            
        return queryset.filter(
            Q(first_name__icontains=value) |
            Q(last_name__icontains=value) |
            Q(work_mail__icontains=value) |
            Q(phone__icontains=value) |
            Q(area__icontains=value)
        )
    
    def filter_computed_status(self, queryset, name, value):
        """
        Filter by computed working status
        """
        if value == 0:
            # No working hours set
            return queryset.filter(
                Q(working_start_time__isnull=True) | 
                Q(working_end_time__isnull=True)
            )
        elif value in [1, 2]:
            # Has working hours - actual status will be computed in serializer
            return queryset.filter(
                working_start_time__isnull=False,
                working_end_time__isnull=False
            )
        return queryset
    
    def filter_has_working_hours(self, queryset, name, value):
        """
        Filter employees with or without working hours
        """
        if value is True:
            return queryset.filter(
                working_start_time__isnull=False,
                working_end_time__isnull=False
            )
        elif value is False:
            return queryset.filter(
                Q(working_start_time__isnull=True) | 
                Q(working_end_time__isnull=True)
            )
        return queryset


class EmployeeSearchFilter(drf_filters.SearchFilter):
    """
    Custom search filter for Employee with enhanced functionality
    """
    search_param = 'search'
    
    def get_search_fields(self, view, request):
        """
        Dynamic search fields based on user permissions or query params
        """
        base_fields = [
            'first_name',
            'last_name', 
            'work_mail',
            'area',
            'phone'
        ]
        
        # Add sensitive fields only for admin users
        if hasattr(request, 'user') and request.user and request.user.is_staff:
            base_fields.extend([
                'personal_mail',
                'user__email',
                'user__first_name',
                'user__last_name'
            ])
        
        # Allow admin-only deep search
        if request.query_params.get('deep_search') and request.user.is_superuser:
            base_fields.extend([
                'additional_information__value',
                'roles__name'
            ])
            
        return base_fields


class EmployeeOrderingFilter(drf_filters.OrderingFilter):
    """
    Custom ordering filter for Employee
    """
    ordering_param = 'ordering'
    
    def get_ordering(self, request, queryset, view):
        """
        Custom ordering logic
        """
        ordering = super().get_ordering(request, queryset, view)
        
        # Default ordering if none specified
        if not ordering:
            return ['-created_at', 'first_name', 'last_name']
            
        return ordering
    
    def get_valid_fields(self, queryset, view, context=None):
        """
        Restrict ordering fields based on user permissions
        """
        base_fields = [
            ('first_name', 'First Name'),
            ('last_name', 'Last Name'),
            ('work_mail', 'Work Email'),
            ('area', 'Work Area'),
            ('join_date', 'Join Date'),
            ('created_at', 'Created Date'),
            ('completed_orders_count', 'Completed Orders'),
            ('total_hours_worked', 'Total Hours'),
            ('status', 'Status'),
        ]
        
        # Add sensitive fields for admin users
        if hasattr(context, 'get') and context.get('request'):
            request = context['request']
            if hasattr(request, 'user') and request.user and request.user.is_staff:
                base_fields.extend([
                    ('salary', 'Salary'),
                    ('date_of_birth', 'Date of Birth'),
                    ('personal_mail', 'Personal Email'),
                ])
        
        return base_fields


# Custom filter backend for user-specific filtering
class UserSpecificFilterBackend(drf_filters.BaseFilterBackend):
    """
    Filter backend that restricts employees based on user permissions
    """
    
    def filter_queryset(self, request, queryset, view):
        """
        Filter queryset based on user permissions and scopes
        """
        # Check OAuth2 scopes
        if hasattr(request, 'auth') and request.auth:
            token_scopes = request.auth.scope.split() if request.auth.scope else []
            
            # If user only has view-mine scope, restrict to their own records
            if ('employees:view-mine' in token_scopes and 
                'employees:view' not in token_scopes and 
                'admin:employees:view' not in token_scopes):
                
                try:
                    jwt_user = request.auth.user
                    real_user = User.objects.get(email=jwt_user.email)
                    return queryset.filter(user=real_user)
                except User.DoesNotExist:
                    return queryset.none()
        
        # For regular Django users without OAuth
        elif hasattr(request, 'user') and request.user and not request.user.is_staff:
            # Non-staff users can only see their own employee record
            try:
                return queryset.filter(user=request.user)
            except:
                return queryset.none()
        
        return queryset


# Export filters for easy importing
__all__ = [
    'EmployeeFilter',
    'EmployeeSearchFilter', 
    'EmployeeOrderingFilter',
    'UserSpecificFilterBackend'
]