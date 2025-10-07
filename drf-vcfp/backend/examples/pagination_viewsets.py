"""
Demo ViewSets showing different pagination types
"""
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from base.pagination import (
    CustomPagination, 
    StandardPagination, 
    LargePagination,
    SmallPagination,
    LimitOffsetCustomPagination,
    CursorCustomPagination
)
from ..models import Employee
from ..serializers import EmployeeSerializer


# 1. ✅ STANDARD PAGE NUMBER PAGINATION
class EmployeeStandardViewSet(ModelViewSet):
    """
    Standard pagination với 20 items per page
    URL: /api/employees-standard/?page=2&page_size=10
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['area', 'status']
    search_fields = ['first_name', 'last_name', 'work_mail']


# 2. ✅ SMALL PAGINATION (FOR MOBILE)
class EmployeeMobileViewSet(ModelViewSet):
    """
    Small pagination cho mobile apps (10 items per page)
    URL: /api/employees-mobile/?page=1&page_size=5
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    pagination_class = SmallPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'last_name']


# 3. ✅ LARGE PAGINATION (FOR EXPORTS)
class EmployeeExportViewSet(ModelViewSet):
    """
    Large pagination cho data exports (50 items per page)
    URL: /api/employees-export/?page=1&page_size=100
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    pagination_class = LargePagination
    
    def list(self, request, *args, **kwargs):
        """Override list to add export information"""
        response = super().list(request, *args, **kwargs)
        response.data['export_info'] = {
            'suitable_for_export': True,
            'max_recommended_page_size': 500,
            'total_pages': response.data.get('num_pages', 1)
        }
        return response


# 4. ✅ LIMIT/OFFSET PAGINATION
class EmployeeLimitOffsetViewSet(ModelViewSet):
    """
    Limit/Offset pagination thay vì page number
    URL: /api/employees-offset/?limit=20&offset=40
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    pagination_class = LimitOffsetCustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['area', 'status', 'salary']


# 5. ✅ CURSOR PAGINATION (FOR REAL-TIME)
class EmployeeCursorViewSet(ModelViewSet):
    """
    Cursor pagination cho real-time data
    URL: /api/employees-cursor/?cursor=cD0yMDIzLTA5LTE1
    
    Note: Requires 'created_at' field in Employee model
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    pagination_class = CursorCustomPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'last_name']


# 6. ✅ DYNAMIC PAGINATION
class EmployeeDynamicViewSet(ModelViewSet):
    """
    Dynamic pagination dựa trên query parameters
    URL: /api/employees-dynamic/?type=mobile
    URL: /api/employees-dynamic/?type=export
    URL: /api/employees-dynamic/?type=api
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['area', 'status']
    search_fields = ['first_name', 'last_name', 'work_mail']
    
    def get_paginator_class(self):
        """Dynamic pagination based on query params"""
        pagination_type = self.request.query_params.get('type', 'default')
        
        pagination_map = {
            'mobile': SmallPagination,
            'export': LargePagination,
            'api': StandardPagination,
            'offset': LimitOffsetCustomPagination,
            'cursor': CursorCustomPagination,
            'default': CustomPagination,
        }
        
        return pagination_map.get(pagination_type, CustomPagination)
    
    @property
    def paginator(self):
        """Override paginator to use dynamic class"""
        if not hasattr(self, '_paginator'):
            pagination_class = self.get_paginator_class()
            self._paginator = pagination_class()
        return self._paginator


# 7. ✅ NO PAGINATION VIEWSET
class EmployeeNoPaginationViewSet(ModelViewSet):
    """
    ViewSet without pagination - returns all data
    URL: /api/employees-all/
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    pagination_class = None  # Disable pagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['first_name', 'last_name']
    ordering_fields = ['first_name', 'created_at']
    ordering = ['first_name']


# 8. ✅ CONDITIONAL PAGINATION
class EmployeeConditionalViewSet(ModelViewSet):
    """
    Conditional pagination - enable/disable based on conditions
    URL: /api/employees-conditional/?paginate=false
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['area', 'status']
    
    @property
    def paginator(self):
        """Conditional pagination"""
        # Disable pagination if explicitly requested
        if self.request.query_params.get('paginate', 'true').lower() == 'false':
            return None
        
        # Use different pagination for different user types
        if hasattr(self.request, 'user') and self.request.user.is_authenticated:
            if self.request.user.is_staff:
                return LargePagination()
            else:
                return SmallPagination()
        
        return CustomPagination()


# 9. ✅ CUSTOM ACTIONS WITH PAGINATION
class EmployeeCustomActionsViewSet(ModelViewSet):
    """
    ViewSet with custom actions using different pagination
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    pagination_class = CustomPagination
    
    @action(detail=False, methods=['get'])
    def active_employees(self, request):
        """Get active employees with small pagination"""
        queryset = Employee.objects.filter(status=1)
        
        # Use small pagination for this action
        page = SmallPagination().paginate_queryset(queryset, request)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return SmallPagination().get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def recent_employees(self, request):
        """Get recent employees with cursor pagination"""
        queryset = Employee.objects.filter(
            created_at__isnull=False
        ).order_by('-created_at')
        
        # Use cursor pagination for real-time data
        paginator = CursorCustomPagination()
        page = paginator.paginate_queryset(queryset, request)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def department_summary(self, request):
        """Get department summary without pagination"""
        from django.db.models import Count
        
        departments = Employee.objects.values('area').annotate(
            employee_count=Count('id')
        ).order_by('area')
        
        return Response({
            'departments': list(departments),
            'total_departments': departments.count(),
            'pagination': 'disabled'
        })


# 10. ✅ PERFORMANCE OPTIMIZED PAGINATION
class EmployeeOptimizedViewSet(ModelViewSet):
    """
    Performance optimized pagination with select_related
    """
    serializer_class = EmployeeSerializer
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['area', 'status']
    search_fields = ['first_name', 'last_name']
    
    def get_queryset(self):
        """Optimize queries with select_related and prefetch_related"""
        return Employee.objects.select_related(
            'user',  # If Employee has user relationship
        ).prefetch_related(
            'skills',  # If Employee has skills relationship
            'projects'  # If Employee has projects relationship
        ).order_by('-created_at')
    
    def list(self, request, *args, **kwargs):
        """Add performance metrics to response"""
        import time
        start_time = time.time()
        
        response = super().list(request, *args, **kwargs)
        
        end_time = time.time()
        response.data['performance'] = {
            'query_time': round(end_time - start_time, 3),
            'optimized': True,
            'items_per_page': len(response.data.get('results', []))
        }
        
        return response