from django.contrib import admin
from .models import Category, Product,ProductImage,ProductPrice
# Register your models here.
admin.site.register(Category)


class ProductImageInline(admin.StackedInline):
    model = ProductImage
    verbose_name_plural = "product_images"
    fk_name = "product"


class ProductPriceInline(admin.StackedInline):
    model = ProductPrice
    verbose_name_plural = "product_prices"
    fk_name = "product"


@admin.register(Product)
class Productdmin(admin.ModelAdmin):

    inlines = [
        ProductImageInline,
        ProductPriceInline
    ]