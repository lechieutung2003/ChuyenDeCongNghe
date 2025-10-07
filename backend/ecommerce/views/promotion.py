from base.views import BaseViewSet
from ..models import Promotion
from ..serializers import PromotionSerializer


class PromotionViewSet(BaseViewSet):
    queryset = Promotion.objects.all()
    search_map = {
        "name__ogigin": "icontains",
        "description__ogigin": "icontains"
    }
    serializer_class = PromotionSerializer
    required_alternate_scopes = {
        "list": [["ecommerce:promotions:view"], ["ecommerce:promotions:edit"]],
        "retrieve": [["ecommerce:promotions:view"], ["ecommerce:promotions:edit"]],
        "create": [["ecommerce:promotions:edit"]],
        "update": [["ecommerce:promotions:edit"]],
        "destroy": [["ecommerce:promotions:edit"]]
    }