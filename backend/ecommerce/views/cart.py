from base.views import BaseViewSet
from ..models import Cart
from ..serializers import CartSerializer

class CartViewSet(BaseViewSet):
    queryset = Cart.objects.all()
    search_map = {
        "customer__first_name": "icontains",
        "customer__last_name": "icontains"
    }
    serializer_class = CartSerializer
    required_alternate_scopes = {
        "list": [["ecommerce:orders:view-mine"], ["ecommerce:orders:edit-mine"]],
        "retrieve": [["ecommerce:orders:view-mine"], ["ecommerce:orders:edit-mine"]],
        "create": [["ecommerce:orders:edit-mine"]],
        "update": [["ecommerce:orders:edit-mine"]],
        "destroy": [["ecommerce:orders:edit-mine"]]
    }