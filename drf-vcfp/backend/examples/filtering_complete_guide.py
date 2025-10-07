# DJANGO REST FRAMEWORK FILTERING EXAMPLES
# Ví dụ về cách sử dụng filtering trong DRF

"""
=== CÁC LOẠI FILTERING TRONG DRF ===

1. BASIC QUERY PARAMETER FILTERING
2. DJANGO-FILTER BACKEND
3. SEARCH FILTER
4. ORDERING FILTER  
5. CUSTOM FILTER BACKENDS

"""

# ===== 1. BASIC QUERY PARAMETER FILTERING =====

# URL Examples:
# GET /api/employees/?first_name=John
# GET /api/employees/?area=IT
# GET /api/employees/?status=1

class BasicEmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    
    def get_queryset(self):
        """Manual filtering using query parameters"""
        queryset = super().get_queryset()
        
        # Filter by first name
        first_name = self.request.query_params.get('first_name')
        if first_name:
            queryset = queryset.filter(first_name__icontains=first_name)
        
        # Filter by area
        area = self.request.query_params.get('area')
        if area:
            queryset = queryset.filter(area__icontains=area)
        
        # Filter by status
        status = self.request.query_params.get('status')
        if status:
            queryset = queryset.filter(status=status)
            
        return queryset


# ===== 2. DJANGO-FILTER BACKEND =====

from django_filters.rest_framework import DjangoFilterBackend

class DjangoFilterEmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    filter_backends = [DjangoFilterBackend]
    
    # Simple field filtering
    filterset_fields = ['first_name', 'area', 'status', 'gender']
    
    # Advanced filtering with lookups
    filterset_fields = {
        'first_name': ['exact', 'icontains', 'istartswith'],
        'salary': ['exact', 'gte', 'lte'],
        'join_date': ['exact', 'year', 'month', 'gte', 'lte'],
        'area': ['exact', 'icontains'],
    }

# URL Examples với DjangoFilterBackend:
# GET /api/employees/?first_name__icontains=John
# GET /api/employees/?salary__gte=50000&salary__lte=100000
# GET /api/employees/?join_date__year=2023
# GET /api/employees/?area__icontains=IT


# ===== 3. SEARCH FILTER =====

from rest_framework import filters

class SearchEmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    filter_backends = [filters.SearchFilter]
    
    # Basic search fields
    search_fields = ['first_name', 'last_name', 'work_mail']
    
    # Advanced search with prefixes
    search_fields = [
        'first_name',          # icontains (default)
        'last_name',           # icontains
        '=work_mail',          # exact match
        '^first_name',         # istartswith
        '$area',               # iregex (regex)
        '@description',        # full-text search (PostgreSQL only)
        'user__email',         # related field search
    ]

# URL Examples với SearchFilter:
# GET /api/employees/?search=John
# GET /api/employees/?search=john@example.com
# GET /api/employees/?search=John Doe  (searches for both terms)


# ===== 4. ORDERING FILTER =====

class OrderingEmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    filter_backends = [filters.OrderingFilter]
    
    ordering_fields = ['first_name', 'last_name', 'join_date', 'salary']
    ordering = ['first_name']  # Default ordering

# URL Examples với OrderingFilter:
# GET /api/employees/?ordering=first_name
# GET /api/employees/?ordering=-salary        (descending)
# GET /api/employees/?ordering=first_name,join_date  (multiple fields)


# ===== 5. COMBINED FILTERING =====

class AdvancedEmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    
    # Django-filter
    filterset_fields = {
        'area': ['exact', 'icontains'],
        'status': ['exact'],
        'salary': ['gte', 'lte'],
        'join_date': ['year', 'month', 'gte', 'lte'],
    }
    
    # Search
    search_fields = ['first_name', 'last_name', '=work_mail']
    
    # Ordering
    ordering_fields = ['first_name', 'join_date', 'salary']
    ordering = ['-join_date']

# URL Examples kết hợp:
# GET /api/employees/?area__icontains=IT&search=John&ordering=-salary
# GET /api/employees/?salary__gte=50000&join_date__year=2023&search=manager


# ===== 6. CUSTOM FILTER SET =====

import django_filters

class EmployeeFilter(django_filters.FilterSet):
    # Custom filters
    name = django_filters.CharFilter(method='filter_full_name')
    salary_range = django_filters.RangeFilter(field_name='salary')
    age_range = django_filters.NumericRangeFilter(method='filter_age')
    
    # Date filters
    joined_after = django_filters.DateFilter(field_name='join_date', lookup_expr='gte')
    joined_before = django_filters.DateFilter(field_name='join_date', lookup_expr='lte')
    
    class Meta:
        model = Employee
        fields = {
            'area': ['exact', 'icontains'],
            'status': ['exact'],
            'gender': ['exact'],
        }
    
    def filter_full_name(self, queryset, name, value):
        return queryset.filter(
            Q(first_name__icontains=value) | Q(last_name__icontains=value)
        )
    
    def filter_age(self, queryset, name, value):
        if value:
            today = timezone.now().date()
            start_date = today - timedelta(days=365 * value.stop)
            end_date = today - timedelta(days=365 * value.start)
            return queryset.filter(date_of_birth__range=[start_date, end_date])
        return queryset

class CustomFilterEmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = EmployeeFilter

# URL Examples với Custom FilterSet:
# GET /api/employees/?name=John
# GET /api/employees/?salary_range_min=40000&salary_range_max=80000
# GET /api/employees/?age_range_min=25&age_range_max=40


# ===== 7. CUSTOM FILTER BACKEND =====

class PermissionFilterBackend(filters.BaseFilterBackend):
    """
    Filter that only allows users to see their own objects.
    """
    def filter_queryset(self, request, queryset, view):
        if request.user.is_staff:
            return queryset  # Staff can see all
        return queryset.filter(user=request.user)

class UserSpecificEmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    filter_backends = [PermissionFilterBackend, DjangoFilterBackend]
    filterset_fields = ['area', 'status']


# ===== 8. SETTINGS CONFIGURATION =====

# settings.py
"""
# Global filter backends
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ]
}

# Install django-filter
INSTALLED_APPS = [
    ...
    'django_filters',
    ...
]

# Filter settings
FILTERS_DEFAULT_LOOKUP_EXPR = 'icontains'
"""


# ===== 9. URL EXAMPLES SUMMARY =====

"""
BASIC FILTERING:
GET /api/employees/?first_name=John&area=IT

DJANGO-FILTER:
GET /api/employees/?first_name__icontains=John
GET /api/employees/?salary__gte=50000&salary__lte=100000
GET /api/employees/?join_date__year=2023

SEARCH:
GET /api/employees/?search=John Doe
GET /api/employees/?search=manager

ORDERING:
GET /api/employees/?ordering=first_name
GET /api/employees/?ordering=-salary,join_date

COMBINED:
GET /api/employees/?area__icontains=IT&search=John&ordering=-salary&salary__gte=50000

PAGINATION + FILTERING:
GET /api/employees/?page=1&page_size=10&area=IT&search=John&ordering=-join_date
"""


# ===== 10. REAL WORLD EXAMPLE =====

class RealWorldEmployeeViewSet(viewsets.ModelViewSet):
    """
    Real-world employee viewset with comprehensive filtering
    """
    serializer_class = EmployeeSerializer
    
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
        PermissionFilterBackend,  # Custom permission filter
    ]
    
    # Advanced django-filter configuration
    filterset_class = EmployeeFilter
    
    # Search configuration
    search_fields = [
        'first_name',
        'last_name',
        '=work_mail',
        'area',
        'phone',
        'user__email',
    ]
    
    # Ordering configuration
    ordering_fields = [
        'first_name',
        'last_name',
        'join_date',
        'salary',
        'completed_orders_count',
        'created_at',
    ]
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Custom queryset with additional business logic"""
        queryset = Employee.objects.exclude(
            roles__name__in=["Super Administrator"]
        ).select_related('user', 'office').prefetch_related('roles')
        
        # Add computed fields or additional filters
        return queryset

# ===== TESTING FILTERS =====

"""
# Test filtering in Django shell
python manage.py shell

from businesses.views import EmployeeViewSet
from rest_framework.test import APIRequestFactory

factory = APIRequestFactory()
view = EmployeeViewSet()

# Test search
request = factory.get('/employees/?search=John')
view.request = request
filtered_qs = view.filter_queryset(view.get_queryset())
print(filtered_qs.count())

# Test django-filter
request = factory.get('/employees/?salary__gte=50000')
view.request = request  
filtered_qs = view.filter_queryset(view.get_queryset())
print(filtered_qs.count())
"""