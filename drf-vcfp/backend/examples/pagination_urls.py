"""
URLs for pagination examples
Add these to your main urls.py or businesses/urls.py
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from examples.pagination_viewsets import (
    EmployeeStandardViewSet,
    EmployeeMobileViewSet,
    EmployeeExportViewSet,
    EmployeeLimitOffsetViewSet,
    EmployeeCursorViewSet,
    EmployeeDynamicViewSet,
    EmployeeNoPaginationViewSet,
    EmployeeConditionalViewSet,
    EmployeeCustomActionsViewSet,
    EmployeeOptimizedViewSet,
)

# Create router for pagination examples
pagination_router = DefaultRouter()

# Register different pagination ViewSets
pagination_router.register(r'employees-standard', EmployeeStandardViewSet, basename='employee-standard')
pagination_router.register(r'employees-mobile', EmployeeMobileViewSet, basename='employee-mobile')
pagination_router.register(r'employees-export', EmployeeExportViewSet, basename='employee-export')
pagination_router.register(r'employees-offset', EmployeeLimitOffsetViewSet, basename='employee-offset')
pagination_router.register(r'employees-cursor', EmployeeCursorViewSet, basename='employee-cursor')
pagination_router.register(r'employees-dynamic', EmployeeDynamicViewSet, basename='employee-dynamic')
pagination_router.register(r'employees-all', EmployeeNoPaginationViewSet, basename='employee-all')
pagination_router.register(r'employees-conditional', EmployeeConditionalViewSet, basename='employee-conditional')
pagination_router.register(r'employees-actions', EmployeeCustomActionsViewSet, basename='employee-actions')
pagination_router.register(r'employees-optimized', EmployeeOptimizedViewSet, basename='employee-optimized')

urlpatterns = [
    # Include pagination examples
    path('api/pagination-examples/', include(pagination_router.urls)),
]

"""
PAGINATION EXAMPLES USAGE:

1. Standard Pagination (20 items per page):
   GET /api/pagination-examples/employees-standard/
   GET /api/pagination-examples/employees-standard/?page=2&page_size=10

2. Mobile Pagination (10 items per page):
   GET /api/pagination-examples/employees-mobile/
   GET /api/pagination-examples/employees-mobile/?page=1&page_size=5

3. Export Pagination (50 items per page):
   GET /api/pagination-examples/employees-export/
   GET /api/pagination-examples/employees-export/?page=1&page_size=100

4. Limit/Offset Pagination:
   GET /api/pagination-examples/employees-offset/
   GET /api/pagination-examples/employees-offset/?limit=20&offset=40

5. Cursor Pagination:
   GET /api/pagination-examples/employees-cursor/
   GET /api/pagination-examples/employees-cursor/?cursor=cD0yMDIzLTA5LTE1

6. Dynamic Pagination:
   GET /api/pagination-examples/employees-dynamic/?type=mobile
   GET /api/pagination-examples/employees-dynamic/?type=export
   GET /api/pagination-examples/employees-dynamic/?type=offset

7. No Pagination:
   GET /api/pagination-examples/employees-all/

8. Conditional Pagination:
   GET /api/pagination-examples/employees-conditional/
   GET /api/pagination-examples/employees-conditional/?paginate=false

9. Custom Actions with Pagination:
   GET /api/pagination-examples/employees-actions/active_employees/
   GET /api/pagination-examples/employees-actions/recent_employees/
   GET /api/pagination-examples/employees-actions/department_summary/

10. Optimized Pagination:
    GET /api/pagination-examples/employees-optimized/

RESPONSE FORMATS:

CustomPagination Response:
{
    "links": {
        "previous": "http://api.example.org/employees/?page=1",
        "next": "http://api.example.org/employees/?page=3"
    },
    "page": 2,
    "page_size": 12,
    "num_pages": 10,
    "count": 120,
    "results": [...]
}

LimitOffsetPagination Response:
{
    "links": {
        "next": "http://api.example.org/employees/?limit=20&offset=40",
        "previous": "http://api.example.org/employees/?limit=20&offset=0"
    },
    "count": 120,
    "limit": 20,
    "offset": 20,
    "results": [...]
}

CursorPagination Response:
{
    "links": {
        "next": "http://api.example.org/employees/?cursor=cD0yMDIz",
        "previous": "http://api.example.org/employees/?cursor=bz0yMDIz"
    },
    "count": 25,
    "results": [...]
}
"""