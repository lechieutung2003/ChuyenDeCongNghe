from django.db import models
from base.models import TimeStampedModel
from .product import Product

class Promotion(TimeStampedModel):
    name = models.CharField(max_length=120, blank=True)
    start = models.DateTimeField(blank=True)
    end = models.DateTimeField(blank=True)
    products = models.ManyToManyField(
        Product,
        through='PromotionItem',
        related_name="promotions",
        null=True,
        blank=True
    )

    class Meta:
        db_table = "ecommerce_promotions"
        ordering = ["-created_at"]
