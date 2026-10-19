from django.contrib import admin
from .models import Product, Order, RefundRequest
# Register your models here.



# Custom Product Model Admin
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "price", "category", "in_stock"]

# Custom Order Model Admin
class OrderAdmin(admin.ModelAdmin):
    list_display = ["user", "product_name", "amount", "status", "carrier", "tracking_number", "delivery_address", "created_at", "updated_at"]

# Custom Refund Request Model Admin
class RefundRequestAdmin(admin.ModelAdmin):
    list_display = ["order", "user", "reason", "status", "created_at", "updated_at"]


admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(RefundRequest, RefundRequestAdmin)