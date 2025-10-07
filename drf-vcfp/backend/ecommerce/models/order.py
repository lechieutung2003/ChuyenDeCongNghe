from django.db import models
from django.template.defaultfilters import slugify
from base.models import TimeStampedModel
from ..constants import PaymentMethod, PaymenStatus
from .customer import Customer

class Order(TimeStampedModel):
    customer =  models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        blank=True,
        related_name="orders",
    )
    customer_name = models.CharField(max_length=200, blank=True)
    company_name = models.CharField(max_length=255, blank=True)
    tax_code = models.CharField(max_length=15)
    payment_method = models.SmallIntegerField(choices=PaymentMethod.CHOICES, default=PaymentMethod.BANK_TRANSFER, blank=True)
    payment_status = models.SmallIntegerField(choices=PaymenStatus.CHOICES, default=PaymenStatus.INITIATED, blank=True)
    account_number = models.CharField(max_length=15)
    vat_rate = models.FloatField(default=0.0, blank=True)
    shipping_fee = models.FloatField(default=0.0, blank=True)
    shipping_status = models.SmallIntegerField(choices=PaymenStatus.CHOICES, default=PaymenStatus.INITIATED, blank=True)

    date = models.DateField(null=True)

    class Meta:
        db_table = "ecommerce_orders"
        ordering = ["-created_at"]