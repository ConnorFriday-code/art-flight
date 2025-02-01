import uuid
from django.db import models
from django.db.models import Sum
from django.conf import settings
from user_profile.models import Artist

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
    street_address2 = models.CharField(max_length=80, null=False, blank=False)
    country = models.CharField(max_length=80, null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)
    delivery_cost = models.DecimalField(max_digits=6, decimal_places=2, null=False, default=0)
    order_total = models.DecimalField(max_length=10, decimal_places=2, null=False, default=0)
    grand_total = models.DecimalField(max_length=10, decimal_places=2, null=False, default=0)

class OrderLineItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    artist = models.ForeignKey("user_profile.Artist", on_delete=models.CASCADE)
    commission_option = models.CharField(max_length=255, null=False, blank=False)
    details = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    lineitem_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False, editable=False)

    def __str__(self):
        return f"{self.commission_option} from {self.artist.artist_name} in Order {self.order.order_number}"