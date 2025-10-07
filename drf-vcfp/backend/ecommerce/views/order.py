from base.views import BaseViewSet
from ..models import Order
from ..serializers import OrderSerializer

class OrderViewSet(BaseViewSet):
    queryset = Order.objects.all()
    search_map = {
        "customer_first_name": "icontains",
        "customer_last_name": "icontains"
    }
    serializer_class = OrderSerializer
    required_alternate_scopes = {
        "list": [["ecommerce:orders:view-mine"], ["ecommerce:orders:edit-mine"]],
        "retrieve": [["ecommerce:orders:view-mine"], ["ecommerce:orders:edit-mine"]],
        "create": [["ecommerce:orders:edit-mine"]],
        "update": [["ecommerce:orders:edit-mine"]],
        "destroy": [["ecommerce:orders:edit-mine"]]
    }