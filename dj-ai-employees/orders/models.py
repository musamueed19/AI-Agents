from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    in_stock = models.BooleanField(default=True)

    def __str__(self):
        return self.name




class Order(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("DISPATCHED", "Dispatched"),
        ("DELIVERED", "Delivered"),
        ("CANCELLED", "Cancelled"),
        ("REFUNDED", "Refunded"),
    ]

    # reference of user, whose is placing this order
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")


    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name="orders")
    product_name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    carrier = models.CharField(max_length=100, blank=True)
    tracking_number = models.CharField(max_length=100, blank=True)
    delivery_address = models.TextField(blank=True)
    created_at = models.DateTimeField() # auto_now_add=Trues
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"Order #{self.id} - {self.product_name} . {self.status}"



class RefundRequest(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
        ("REFUNDED", "Refunded"),
    ]
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="refund_requests")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="refund_requests")
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    created_at = models.DateTimeField() # auto_now_add=Trues
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"Refund for order #{self.order.id} - {self.status}"




# Django Fixtures Seed Data Command
# ============
# python3 manage.py loaddata ./orders/fixtures/seed_users_products_orders_refundrequests_data.json
# ============