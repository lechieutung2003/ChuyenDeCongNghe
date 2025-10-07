# PAGINATION EXAMPLES

## 1. CÁC LOẠI PAGINATION TRONG DRF

### A. PageNumberPagination (Default)
```python
# URL: /api/employees/?page=2&page_size=10
from rest_framework.viewsets import ModelViewSet
from base.pagination import CustomPagination

class EmployeeViewSet(ModelViewSet):
    pagination_class = CustomPagination
    # Tự động pagination, không cần code thêm
```

### B. LimitOffsetPagination
```python
# URL: /api/employees/?limit=20&offset=40
from base.pagination import LimitOffsetCustomPagination

class EmployeeViewSet(ModelViewSet):
    pagination_class = LimitOffsetCustomPagination
```

### C. CursorPagination
```python
# URL: /api/employees/?cursor=cD0yMDIzLTA5LTE1
from base.pagination import CursorCustomPagination

class EmployeeViewSet(ModelViewSet):
    pagination_class = CursorCustomPagination
    # Model cần có field created_at hoặc updated_at
```

## 2. SỬ DỤNG PAGINATION TRONG VIEWSET

### Cách 1: Set pagination_class cho từng ViewSet
```python
class EmployeeViewSet(ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    pagination_class = CustomPagination  # Sử dụng pagination riêng
```

### Cách 2: Sử dụng pagination mặc định từ settings
```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'base.pagination.CustomPagination',
    'PAGE_SIZE': 12
}

class EmployeeViewSet(ModelViewSet):
    # Không cần khai báo pagination_class
    # Tự động sử dụng CustomPagination
    pass
```

### Cách 3: Tắt pagination cho ViewSet cụ thể
```python
class EmployeeViewSet(ModelViewSet):
    pagination_class = None  # Tắt pagination
```

## 3. CUSTOM RESPONSE FORMAT

### Response của CustomPagination:
```json
{
    "links": {
        "previous": "http://api.example.org/accounts/?page=1",
        "next": "http://api.example.org/accounts/?page=3"
    },
    "page": 2,
    "page_size": 12,
    "num_pages": 10,
    "count": 120,
    "results": [
        {
            "id": 1,
            "name": "Employee 1"
        }
    ]
}
```

### Response của LimitOffsetPagination:
```json
{
    "links": {
        "next": "http://api.example.org/accounts/?limit=20&offset=40",
        "previous": "http://api.example.org/accounts/?limit=20&offset=0"
    },
    "count": 120,
    "limit": 20,
    "offset": 20,
    "results": [...]
}
```

## 4. PAGINATION VỚI FILTERING & SEARCHING

```python
class EmployeeViewSet(ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['department', 'position']
    search_fields = ['first_name', 'last_name', 'email']
    ordering_fields = ['created_at', 'salary']

# URL: /api/employees/?page=2&page_size=10&department=IT&search=john&ordering=-salary
```

## 5. PAGINATION TRONG FUNCTION-BASED VIEWS

```python
from django.core.paginator import Paginator
from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.pagination import CustomPagination

@api_view(['GET'])
def employee_list(request):
    employees = Employee.objects.all()
    
    # Sử dụng DRF pagination
    paginator = CustomPagination()
    page = paginator.paginate_queryset(employees, request)
    
    if page is not None:
        serializer = EmployeeSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    serializer = EmployeeSerializer(employees, many=True)
    return Response(serializer.data)
```

## 6. PAGINATION VỚI PERMISSION & AUTHENTICATION

```python
class EmployeeViewSet(ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Chỉ hiển thị employees của department hiện tại
        user = self.request.user
        return Employee.objects.filter(department=user.department)
```

## 7. DYNAMIC PAGINATION

```python
class EmployeeViewSet(ModelViewSet):
    def get_paginator(self):
        # Thay đổi pagination dựa trên query param
        if self.request.query_params.get('mobile') == 'true':
            return SmallPagination()
        elif self.request.query_params.get('export') == 'true':
            return LargePagination()
        return CustomPagination()
```

## 8. PERFORMANCE OPTIMIZATION

```python
class OptimizedEmployeeViewSet(ModelViewSet):
    pagination_class = CustomPagination
    
    def get_queryset(self):
        # Sử dụng select_related và prefetch_related
        return Employee.objects.select_related(
            'department', 'position'
        ).prefetch_related(
            'skills', 'projects'
        )
```

## 9. TESTING PAGINATION

```python
from rest_framework.test import APITestCase

class PaginationTestCase(APITestCase):
    def test_employee_pagination(self):
        # Tạo 25 employees
        for i in range(25):
            Employee.objects.create(name=f'Employee {i}')
        
        response = self.client.get('/api/employees/?page=1&page_size=10')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 10)
        self.assertEqual(response.data['count'], 25)
        self.assertEqual(response.data['num_pages'], 3)
```

## 10. FRONTEND INTEGRATION

### JavaScript Example:
```javascript
// Fetch với pagination
async function fetchEmployees(page = 1, pageSize = 12) {
    const response = await fetch(`/api/employees/?page=${page}&page_size=${pageSize}`);
    const data = await response.json();
    
    return {
        employees: data.results,
        totalCount: data.count,
        currentPage: data.page,
        totalPages: data.num_pages,
        hasNext: !!data.links.next,
        hasPrevious: !!data.links.previous
    };
}
```

### React Hook Example:
```javascript
function useEmployeePagination() {
    const [employees, setEmployees] = useState([]);
    const [page, setPage] = useState(1);
    const [loading, setLoading] = useState(false);
    
    useEffect(() => {
        setLoading(true);
        fetchEmployees(page).then(data => {
            setEmployees(data.employees);
            setLoading(false);
        });
    }, [page]);
    
    return { employees, page, setPage, loading };
}
```