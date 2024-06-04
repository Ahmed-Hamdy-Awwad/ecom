from django.db import models
from django.contrib.auth.models import User


class StampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,
                                   related_name='created_category')

    class Meta:
        abstract = True


class Category(StampedModel):
    name = models.CharField(max_length=100, null=True, blank=True)


class Product(StampedModel):
    name = models.CharField(max_length=100, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 related_name="category_product")
    stock = models.PositiveIntegerField(default=0)


class ProductPrice(StampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name="product_prices")
    min_quantity = models.PositiveIntegerField(default=1)
    unit_price = models.FloatField(null=False, blank=False)


class ProductImage(StampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name="product_images")
    image = models.ImageField()
