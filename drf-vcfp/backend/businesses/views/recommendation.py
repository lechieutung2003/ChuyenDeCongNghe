from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from ..models import Employee
from hr.models import Order, Assignment
from hr.models import Customer
from ..serializers.recommendation import RecommendationSerializer
from ..services.recommendation import RecommendationService
import logging

logger = logging.getLogger(__name__)

class RecommendationViewSet(ViewSet):
    """
    ViewSet for employee recommendations for orders
    """

    required_alternate_scopes = {
        "create": [["roles:edit"]],
        "retrieve": [["roles:edit"], ["roles:view"]],
        "update": [["roles:edit"]],
        "destroy": [["roles:edit"]],
        "list": [["roles:edit"], ["roles:view"]],
        "get_recommendations": [["roles:edit"], ["roles:view"]],  # Thêm cái này  
    }

    @action(detail=True, methods=['get'], url_path='recommendations')
    def get_recommendations(self, request, pk=None):
        """
        Get recommended employees for an order based on various factors
        """
        try:
            logger.info(f"Getting recommendations for order: {pk}")
            order = Order.objects.get(id=pk)

            assigned_employee_ids = Assignment.objects.filter(
                order=order
            ).values_list('employee_id', flat=True)
            
            logger.info(f"Found {len(assigned_employee_ids)} already assigned employees")

            employees = Employee.objects.filter(
                status='1'
            ).exclude(
                id__in=assigned_employee_ids
            )
            
            logger.info(f"Found {len(employees)} active employees not yet assigned")
            
            recommendations = []
            
            for employee in employees:
                score = RecommendationService.calculate_match_score(employee, order)
                logger.info(f"Match score for employee {employee.first_name} {employee.last_name}: {score}")
                
                if score > 0:
                    recommendations.append({
                        'employee': employee,
                        'score': score,
                        'reasons': RecommendationService.get_match_reasons(employee, order)
                    })
            
            logger.info(f"Found {len(recommendations)} recommendations")
            
            # Sắp xếp theo điểm số từ cao xuống thấp
            recommendations.sort(key=lambda x: x['score'], reverse=True)
            
            serializer = RecommendationSerializer(recommendations, many=True)
            return Response(serializer.data)
            
        except Order.DoesNotExist:
            logger.warning(f"Order not found: {pk}")
            return Response({'error': 'Order not found'}, status=404)
        except Exception as e:
            logger.error(f"Error getting recommendations: {str(e)}", exc_info=True)
            return Response({'error': str(e)}, status=500)