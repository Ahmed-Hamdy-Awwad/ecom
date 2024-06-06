from django.db import models
from django.contrib.auth.models import User

from users.models import Company


class Category(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="created_category"
    )


class Product(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="category_product"
    )
    seller = models.ForeignKey(Company, on_delete=models.CASCADE)
    stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="created_product"
    )


class ProductPrice(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_prices"
    )
    min_quantity = models.PositiveIntegerField(default=1)
    unit_price = models.FloatField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="created_product_price"
    )


def upload_to(instance, file_name):
    return f"uploads/products/{instance.id}/{file_name}"


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_images"
    )
    image = models.ImageField(upload_to=upload_to)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="created_product_image"
    )
