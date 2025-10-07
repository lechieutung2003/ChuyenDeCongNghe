"""
Tests for Employee filtering functionality
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework import status
from django.urls import reverse
from decimal import Decimal
from datetime import date, time

from ..models import Employee
from ..views import EmployeeViewSet
from ..filters import EmployeeFilter, EmployeeSearchFilter


User = get_user_model()


class EmployeeFilteringTestCase(APITestCase):
    """Test Employee filtering through API endpoints"""
    
    def setUp(self):
        """Set up test data"""
        # Create test users
        self.user1 = User.objects.create_user(
            email='john@test.com',
            first_name='John',
            last_name='Doe',
            password='testpass123'
        )
        
        self.user2 = User.objects.create_user(
            email='jane@test.com', 
            first_name='Jane',
            last_name='Smith',
            password='testpass123'
        )
        
        # Create test employees
        self.employee1 = Employee.objects.create(
            user=self.user1,
            first_name='John',
            last_name='Doe',
            work_mail='john.doe@company.com',
            area='IT',
            salary=Decimal('75000.00'),
            join_date=date(2023, 1, 15),
            working_start_time=time(9, 0),
            working_end_time=time(17, 0),
            completed_orders_count=25,
            status=1
        )
        
        self.employee2 = Employee.objects.create(
            user=self.user2,
            first_name='Jane',
            last_name='Smith',
            work_mail='jane.smith@company.com',
            area='HR',
            salary=Decimal('65000.00'),
            join_date=date(2023, 3, 10),
            working_start_time=time(8, 30),
            working_end_time=time(16, 30),
            completed_orders_count=18,
            status=1
        )
        
        self.employee3 = Employee.objects.create(
            first_name='Bob',
            last_name='Wilson',
            work_mail='bob.wilson@company.com',
            area='IT',
            salary=Decimal('85000.00'),
            join_date=date(2022, 11, 5),
            # No working hours set
            completed_orders_count=30,
            status=0
        )
    
    def test_search_filter(self):
        """Test search functionality"""
        url = reverse('employee-list')  # Adjust URL name as needed
        
        # Search by first name
        response = self.client.get(url, {'search': 'John'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['first_name'], 'John')
        
        # Search by area
        response = self.client.get(url, {'search': 'IT'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)  # John and Bob in IT
        
        # Search by email
        response = self.client.get(url, {'search': 'jane.smith'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['work_mail'], 'jane.smith@company.com')
    
    def test_area_filter(self):
        """Test area filtering"""
        url = reverse('employee-list')
        
        # Filter by IT area
        response = self.client.get(url, {'area': 'IT'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        
        # Filter by HR area
        response = self.client.get(url, {'area': 'HR'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['area'], 'HR')
    
    def test_salary_range_filter(self):
        """Test salary range filtering"""
        url = reverse('employee-list')
        
        # Filter by minimum salary
        response = self.client.get(url, {'salary__gte': '70000'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)  # John and Bob
        
        # Filter by maximum salary
        response = self.client.get(url, {'salary__lte': '70000'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)  # Jane
        
        # Filter by salary range
        response = self.client.get(url, {'salary__gte': '65000', 'salary__lte': '80000'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)  # John and Jane
    
    def test_join_date_filter(self):
        """Test join date filtering"""
        url = reverse('employee-list')
        
        # Filter by year
        response = self.client.get(url, {'join_date__year': '2023'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)  # John and Jane
        
        # Filter by date range
        response = self.client.get(url, {'join_date__gte': '2023-01-01'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
    
    def test_status_filter(self):
        """Test status filtering"""
        url = reverse('employee-list')
        
        # Filter by active status
        response = self.client.get(url, {'status': '1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        
        # Filter by no working hours status
        response = self.client.get(url, {'status': '0'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['first_name'], 'Bob')
    
    def test_working_hours_filter(self):
        """Test working hours filtering"""
        url = reverse('employee-list')
        
        # Filter employees with working hours
        response = self.client.get(url, {'has_working_hours': 'true'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)  # John and Jane
        
        # Filter employees without working hours
        response = self.client.get(url, {'has_working_hours': 'false'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)  # Bob
    
    def test_ordering(self):
        """Test result ordering"""
        url = reverse('employee-list')
        
        # Order by first name ascending
        response = self.client.get(url, {'ordering': 'first_name'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        self.assertEqual(results[0]['first_name'], 'Bob')
        self.assertEqual(results[1]['first_name'], 'Jane')
        self.assertEqual(results[2]['first_name'], 'John')
        
        # Order by salary descending
        response = self.client.get(url, {'ordering': '-salary'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        self.assertEqual(results[0]['first_name'], 'Bob')  # Highest salary
        self.assertEqual(results[1]['first_name'], 'John')
        self.assertEqual(results[2]['first_name'], 'Jane')  # Lowest salary
    
    def test_combined_filters(self):
        """Test combining multiple filters"""
        url = reverse('employee-list')
        
        # Combine area filter with search
        response = self.client.get(url, {
            'area': 'IT',
            'search': 'John',
            'ordering': 'first_name'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['first_name'], 'John')
        
        # Combine salary filter with area and ordering
        response = self.client.get(url, {
            'area': 'IT',
            'salary__gte': '80000',
            'ordering': '-join_date'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['first_name'], 'Bob')
    
    def test_pagination_with_filters(self):
        """Test pagination combined with filtering"""
        url = reverse('employee-list')
        
        # Test with page size
        response = self.client.get(url, {
            'area': 'IT',
            'page_size': '1',
            'page': '1'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertTrue('next' in response.data)
        
        # Test next page
        response = self.client.get(url, {
            'area': 'IT',
            'page_size': '1',
            'page': '2'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)


class EmployeeFilterSetTestCase(TestCase):
    """Test Employee FilterSet directly"""
    
    def setUp(self):
        """Set up test data"""
        self.employee1 = Employee.objects.create(
            first_name='Alice',
            last_name='Johnson',
            work_mail='alice@test.com',
            area='Marketing',
            salary=Decimal('60000.00'),
            join_date=date(2023, 6, 1),
            working_start_time=time(9, 0),
            working_end_time=time(17, 0),
            status=1
        )
        
        self.employee2 = Employee.objects.create(
            first_name='Charlie',
            last_name='Brown',
            work_mail='charlie@test.com',
            area='Sales',
            salary=Decimal('55000.00'),
            join_date=date(2023, 4, 15),
            status=0  # No working hours
        )
    
    def test_filter_search(self):
        """Test custom search filter method"""
        filter_set = EmployeeFilter({'search': 'Alice'}, queryset=Employee.objects.all())
        self.assertEqual(filter_set.qs.count(), 1)
        self.assertEqual(filter_set.qs.first().first_name, 'Alice')
        
        # Test search by email
        filter_set = EmployeeFilter({'search': 'charlie@test.com'}, queryset=Employee.objects.all())
        self.assertEqual(filter_set.qs.count(), 1)
        self.assertEqual(filter_set.qs.first().first_name, 'Charlie')
    
    def test_filter_computed_status(self):
        """Test computed status filter method"""
        # Filter employees with no working hours
        filter_set = EmployeeFilter({'computed_status': 0}, queryset=Employee.objects.all())
        self.assertEqual(filter_set.qs.count(), 1)
        self.assertEqual(filter_set.qs.first().first_name, 'Charlie')
        
        # Filter employees with working hours
        filter_set = EmployeeFilter({'computed_status': 1}, queryset=Employee.objects.all())
        self.assertEqual(filter_set.qs.count(), 1)
        self.assertEqual(filter_set.qs.first().first_name, 'Alice')
    
    def test_filter_has_working_hours(self):
        """Test working hours boolean filter"""
        # Filter employees with working hours
        filter_set = EmployeeFilter({'has_working_hours': True}, queryset=Employee.objects.all())
        self.assertEqual(filter_set.qs.count(), 1)
        self.assertEqual(filter_set.qs.first().first_name, 'Alice')
        
        # Filter employees without working hours
        filter_set = EmployeeFilter({'has_working_hours': False}, queryset=Employee.objects.all())
        self.assertEqual(filter_set.qs.count(), 1)
        self.assertEqual(filter_set.qs.first().first_name, 'Charlie')
    
    def test_salary_range_filters(self):
        """Test salary range filtering"""
        # Minimum salary filter
        filter_set = EmployeeFilter({'salary_min': 58000}, queryset=Employee.objects.all())
        self.assertEqual(filter_set.qs.count(), 1)
        self.assertEqual(filter_set.qs.first().first_name, 'Alice')
        
        # Maximum salary filter
        filter_set = EmployeeFilter({'salary_max': 58000}, queryset=Employee.objects.all())
        self.assertEqual(filter_set.qs.count(), 1)
        self.assertEqual(filter_set.qs.first().first_name, 'Charlie')


class EmployeeViewSetFilteringTestCase(TestCase):
    """Test EmployeeViewSet filtering using APIRequestFactory"""
    
    def setUp(self):
        """Set up test data and factory"""
        self.factory = APIRequestFactory()
        self.view = EmployeeViewSet()
        
        # Create test employee
        self.employee = Employee.objects.create(
            first_name='Test',
            last_name='Employee',
            work_mail='test@example.com',
            area='Engineering',
            salary=Decimal('70000.00'),
            status=1
        )
    
    def test_filter_queryset_method(self):
        """Test that filter_queryset method works"""
        # Create request with search parameter
        request = self.factory.get('/employees/', {'search': 'Test'})
        self.view.request = request
        
        # Get initial queryset
        queryset = self.view.get_queryset()
        
        # Apply filters
        filtered_queryset = self.view.filter_queryset(queryset)
        
        # Should find our test employee
        self.assertEqual(filtered_queryset.count(), 1)
        self.assertEqual(filtered_queryset.first().first_name, 'Test')
    
    def test_empty_filter_results(self):
        """Test filtering with no results"""
        request = self.factory.get('/employees/', {'search': 'NonExistent'})
        self.view.request = request
        
        queryset = self.view.get_queryset()
        filtered_queryset = self.view.filter_queryset(queryset)
        
        self.assertEqual(filtered_queryset.count(), 0)


# Performance tests
class EmployeeFilteringPerformanceTestCase(TestCase):
    """Test filtering performance with larger datasets"""
    
    @classmethod
    def setUpTestData(cls):
        """Create test data once for all tests"""
        # Create many employees for performance testing
        employees = []
        for i in range(100):
            employees.append(Employee(
                first_name=f'Employee{i}',
                last_name=f'Last{i}',
                work_mail=f'employee{i}@test.com',
                area='IT' if i % 2 == 0 else 'HR',
                salary=Decimal(str(50000 + (i * 1000))),
                status=1 if i % 3 != 0 else 0
            ))
        Employee.objects.bulk_create(employees)
    
    def test_search_performance(self):
        """Test search filter performance"""
        import time
        
        filter_set = EmployeeFilter({'search': 'Employee1'}, queryset=Employee.objects.all())
        
        start_time = time.time()
        result_count = filter_set.qs.count()
        end_time = time.time()
        
        # Should complete quickly (< 1 second for 100 records)
        self.assertLess(end_time - start_time, 1.0)
        self.assertGreater(result_count, 0)
    
    def test_complex_filter_performance(self):
        """Test complex filtering performance"""
        import time
        
        filter_params = {
            'area': 'IT',
            'salary_min': 60000,
            'salary_max': 90000,
            'status': 1
        }
        
        filter_set = EmployeeFilter(filter_params, queryset=Employee.objects.all())
        
        start_time = time.time()
        results = list(filter_set.qs)  # Force evaluation
        end_time = time.time()
        
        # Should complete quickly
        self.assertLess(end_time - start_time, 1.0)
        self.assertGreater(len(results), 0)


if __name__ == '__main__':
    import django
    from django.conf import settings
    from django.test.utils import get_runner
    
    # Configure Django settings if not already configured
    if not settings.configured:
        settings.configure(
            DEBUG=True,
            DATABASES={
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': ':memory:',
                }
            },
            INSTALLED_APPS=[
                'django.contrib.auth',
                'django.contrib.contenttypes',
                'rest_framework',
                'django_filters',
                'businesses',
            ],
            SECRET_KEY='test-secret-key'
        )
        django.setup()
    
    # Run tests
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(['__main__'])
    
    print(f"\n✅ Tests completed with {failures} failures")