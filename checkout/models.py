import uuid
from django.db import models
from django.db.models import Sum
from django.conf import settings
from decimal import Decimal

# Create your models here.

class Order(models.Model):
    order_number = models.CharField(max_length=32, null=False, editable=False)
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    country = models.CharField(max_length=40, null=False, blank=False)
    postcode = models.CharField(max_length=20, null=False, blank=False)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=False)
    county = models.CharField(max_length=80, null=True, blank=False)
    date = models.DateTimeField(auto_now_add=True)
    delivery_cost = models.DecimalField(max_digits=6, decimal_places=2, null=False, default=0)
    order_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)

    def _generate_order_number(self):
        """ Generate a random number """
        return uuid.uuid4().hex.upper()

    def update_total(self):
        """
        Update grand total each time a new line is added, 
        accounting for delivery cost.
        """
        aggregated_total = self.lineitems.aggregate(total=Sum('lineitem_total'))['total']
        # Ensure order_total is a Decimal
        self.order_total = Decimal(aggregated_total) if aggregated_total is not None else Decimal('0.00')
        
        # Convert threshold and percentage to Decimals as well
        free_delivery_threshold = Decimal(str(settings.FREE_DELIVERY_THRESHOLD))
        standard_delivery_percentage = Decimal(str(settings.STANDARD_DELIVERY_PERCENTAGE))
        
        if self.order_total < free_delivery_threshold:
            # Calculate delivery cost (divide by 100 to get a percentage)
            self.delivery_cost = self.order_total * standard_delivery_percentage / Decimal('100')
        else:
            self.delivery_cost = Decimal('0.00')
        
        self.grand_total = self.order_total + self.delivery_cost
        self.save()
    
    def save(self, *args, **kwargs):
        """ Override the original save method to set order number """
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.order_number

class OrderLineItem(models.Model):
    order = models.ForeignKey(Order, null=False, blank=False, on_delete=models.CASCADE, related_name='lineitems')
    artist = models.ForeignKey("user_profile.Artist", on_delete=models.CASCADE)
    commission_option = models.CharField(max_length=255, null=False, blank=False)
    details = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    lineitem_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False, editable=False)

    def __str__(self):
        return f"{self.commission_option} from {self.artist.artist_name} in Order {self.order.order_number}"

    def save(self, *args, **kwargs):
        """ Override the original save method to set order number """
        self.lineitem_total = self.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f'SKU {self.artist.sku} on order {self.order.order_number}'