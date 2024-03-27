from django.contrib import admin
from .models import Order, OrderItem
# Register your models here.
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Class To add Order to Admin panel"""

    search_fields = ("id","customer__name", "supplier__name",)
    list_display = (
        "id",
        "customer",
        "supplier",
        "created_at",
        "created_by"
    )

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """Class To add Order Item to Admin panel"""

    search_fields = ("order__id",) # Add product__name
    list_display = (
        "id",
        "order",
        # "product",
        "unit_price",
        "qty",
        "created_at",
        "created_by"
    )