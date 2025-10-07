from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from businesses.models import Employee
from businesses.serializers import EmployeeSerializer
from base.pagination import CustomPagination, StandardPagination, SmallPagination

User = get_user_model()


class PaginationTestCase(APITestCase):
    """Test pagination functionality for Employee API"""
    
    def setUp(self):
        """Create test data"""
        self.client = APIClient()
        
        # Create test user
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        
        # Create 25 test employees
        self.employees = []
        for i in range(25):
            employee = Employee.objects.create(
                first_name=f'Employee {i}',
                last_name=f'Test {i}',
                work_mail=f'employee{i}@test.com',
                area=f'Department {i % 3}',  # 3 departments
                status=1,
                salary=50000 + (i * 1000)
            )
            self.employees.append(employee)
    
    def test_default_pagination(self):
        """Test default pagination settings"""
        response = self.client.get('/api/employees/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertIn('count', response.data)
        self.assertIn('page', response.data)
        self.assertIn('page_size', response.data)
        self.assertIn('num_pages', response.data)
        self.assertIn('links', response.data)
        
        # Check pagination structure
        self.assertEqual(response.data['count'], 25)  # Total items
        self.assertEqual(len(response.data['results']), 12)  # Default page size
        self.assertEqual(response.data['page'], 1)  # First page
        self.assertEqual(response.data['num_pages'], 3)  # 25/12 = 3 pages
    
    def test_custom_page_size(self):
        """Test custom page size parameter"""
        response = self.client.get('/api/employees/?page_size=10')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 10)
        self.assertEqual(response.data['page_size'], 10)
        self.assertEqual(response.data['num_pages'], 3)  # 25/10 = 3 pages
    
    def test_specific_page(self):
        """Test accessing specific page"""
        response = self.client.get('/api/employees/?page=2&page_size=10')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 10)
        self.assertEqual(response.data['page'], 2)
        
        # Check navigation links
        self.assertIsNotNone(response.data['links']['previous'])
        self.assertIsNotNone(response.data['links']['next'])
    
    def test_last_page(self):
        """Test last page with fewer items"""
        response = self.client.get('/api/employees/?page=3&page_size=10')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 5)  # 25 - (2*10) = 5
        self.assertEqual(response.data['page'], 3)
        
        # Check navigation links
        self.assertIsNotNone(response.data['links']['previous'])
        self.assertIsNone(response.data['links']['next'])
    
    def test_invalid_page(self):
        """Test invalid page number"""
        response = self.client.get('/api/employees/?page=999')
        
        # Should return last available page or empty result
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_pagination_with_filtering(self):
        """Test pagination combined with filtering"""
        # Filter by department and paginate
        response = self.client.get('/api/employees/?area=Department 1&page_size=5')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Should only contain employees from Department 1
        for employee in response.data['results']:
            self.assertEqual(employee['area'], 'Department 1')
        
        # Count should reflect filtered results
        expected_count = Employee.objects.filter(area='Department 1').count()
        self.assertEqual(response.data['count'], expected_count)
    
    def test_pagination_with_search(self):
        """Test pagination with search functionality"""
        response = self.client.get('/api/employees/?search=Employee 1&page_size=5')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Should contain employees matching search
        for employee in response.data['results']:
            self.assertIn('1', employee['first_name'])
    
    def test_pagination_with_ordering(self):
        """Test pagination with ordering"""
        response = self.client.get('/api/employees/?ordering=-salary&page_size=5')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check if results are ordered by salary descending
        salaries = [emp['salary'] for emp in response.data['results'] if emp.get('salary')]
        self.assertEqual(salaries, sorted(salaries, reverse=True))
    
    def test_max_page_size_limit(self):
        """Test page size limit enforcement"""
        response = self.client.get('/api/employees/?page_size=500')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should be limited to max_page_size (100)
        self.assertLessEqual(len(response.data['results']), 100)
    
    def test_negative_page_size(self):
        """Test negative page size handling"""
        response = self.client.get('/api/employees/?page_size=-10')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should use default page size
        self.assertGreater(len(response.data['results']), 0)
    
    def test_zero_page_size(self):
        """Test zero page size handling"""
        response = self.client.get('/api/employees/?page_size=0')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should use minimum page size (1) or default
        self.assertGreater(len(response.data['results']), 0)


class PaginationClassTestCase(APITestCase):
    """Test different pagination classes"""
    
    def setUp(self):
        """Create test data"""
        self.client = APIClient()
        
        # Create 50 test employees
        for i in range(50):
            Employee.objects.create(
                first_name=f'Employee {i}',
                last_name=f'Test {i}',
                work_mail=f'employee{i}@test.com',
                area='IT',
                status=1
            )
    
    def test_custom_pagination_response_format(self):
        """Test CustomPagination response format"""
        response = self.client.get('/api/employees/')
        
        expected_keys = [
            'links', 'page', 'page_size', 'num_pages', 'count', 'results'
        ]
        
        for key in expected_keys:
            self.assertIn(key, response.data)
        
        # Check links structure
        self.assertIn('previous', response.data['links'])
        self.assertIn('next', response.data['links'])
    
    def test_pagination_navigation_links(self):
        """Test pagination navigation links"""
        # First page
        response = self.client.get('/api/employees/?page=1')
        self.assertIsNone(response.data['links']['previous'])
        self.assertIsNotNone(response.data['links']['next'])
        
        # Middle page
        response = self.client.get('/api/employees/?page=2')
        self.assertIsNotNone(response.data['links']['previous'])
        self.assertIsNotNone(response.data['links']['next'])
        
        # Last page (assuming 12 items per page, 50 total = 5 pages)
        response = self.client.get('/api/employees/?page=5')
        self.assertIsNotNone(response.data['links']['previous'])
        self.assertIsNone(response.data['links']['next'])


class PaginationPerformanceTestCase(APITestCase):
    """Test pagination performance with large datasets"""
    
    def setUp(self):
        """Create large test dataset"""
        self.client = APIClient()
        
        # Create 1000 test employees
        employees = []
        for i in range(1000):
            employees.append(Employee(
                first_name=f'Employee {i}',
                last_name=f'Test {i}',
                work_mail=f'employee{i}@test.com',
                area=f'Department {i % 10}',
                status=1,
                salary=50000 + (i * 100)
            ))
        
        Employee.objects.bulk_create(employees)
    
    def test_large_dataset_pagination(self):
        """Test pagination with large dataset"""
        import time
        
        start_time = time.time()
        response = self.client.get('/api/employees/?page=10&page_size=50')
        end_time = time.time()
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 50)
        self.assertEqual(response.data['count'], 1000)
        
        # Performance check (should complete within reasonable time)
        self.assertLess(end_time - start_time, 5.0)  # Less than 5 seconds
    
    def test_pagination_with_complex_filtering(self):
        """Test pagination with complex filtering on large dataset"""
        response = self.client.get(
            '/api/employees/?area=Department 5&salary__gte=60000&page_size=20'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify filtering worked correctly
        for employee in response.data['results']:
            self.assertEqual(employee['area'], 'Department 5')
            if employee.get('salary'):
                self.assertGreaterEqual(employee['salary'], 60000)


class PaginationEdgeCasesTestCase(APITestCase):
    """Test pagination edge cases"""
    
    def setUp(self):
        """Create minimal test data"""
        self.client = APIClient()
        
        # Create only 3 employees
        for i in range(3):
            Employee.objects.create(
                first_name=f'Employee {i}',
                last_name=f'Test {i}',
                work_mail=f'employee{i}@test.com',
                area='IT',
                status=1
            )
    
    def test_empty_dataset(self):
        """Test pagination with empty dataset"""
        Employee.objects.all().delete()
        
        response = self.client.get('/api/employees/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)
        self.assertEqual(len(response.data['results']), 0)
        self.assertEqual(response.data['num_pages'], 1)
    
    def test_single_item_dataset(self):
        """Test pagination with single item"""
        Employee.objects.all().delete()
        Employee.objects.create(
            first_name='Single Employee',
            work_mail='single@test.com',
            status=1
        )
        
        response = self.client.get('/api/employees/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['num_pages'], 1)
        self.assertIsNone(response.data['links']['previous'])
        self.assertIsNone(response.data['links']['next'])
    
    def test_page_size_larger_than_dataset(self):
        """Test page size larger than total items"""
        response = self.client.get('/api/employees/?page_size=100')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)  # All 3 items
        self.assertEqual(response.data['count'], 3)
        self.assertEqual(response.data['num_pages'], 1)