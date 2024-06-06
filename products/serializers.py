from django.db import transaction

from rest_framework import serializers

from .models import Category, Product, ProductImage, ProductPrice


class CreateCategorySerializer(serializers.ModelSerializer):
    # created_by = serializers.SerializerMethodField()

    # def get_created_by(self):
    #     return self.context.get("created_by")

    class Meta:
        model = Category
        fields = "__all__"
        # extra_kwargs = {
        #     'created_by': {
        #         'read_only': True
        #     }
        # }


class GetCategorySerializer(serializers.ModelSerializer):
    created_by = serializers.SlugRelatedField(slug_field='username',
                                              read_only=True)

    class Meta:
        model = Category
        fields = "__all__"


class ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    class Meta:
        model = ProductImage
        exclude = ['created_by', 'created_at']


class ProductPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPrice
        exclude = ['created_by', 'created_at']


class CreateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
        # fields = [
        #     "name",
        #     "category",
        #     "seller",
        #     "stock",
        #     # "product_prices",
        #     # "product_images"
        # ]

    # @transaction.atomic()
    # def create(self, validated_data):
    #     print('validated_data', validated_data)
    #     product_prices_data = validated_data.pop('product_prices')
    #     product_images_data = validated_data.pop('product_images') # Need Testing

    #     print('product_prices_data',product_prices_data)
    #     product = Product.objects.create(**validated_data)

    #     new_product_prices = []
    #     for product_price_data in product_prices_data:
    #         new_product_prices.append(
    #         ProductPrice(product=product, created_by=product.created_by, **product_price_data,)
    #         )
    #     ProductPrice.objects.bulk_create(new_product_prices)

    #     new_product_images = []
    #     for product_image_data in product_images_data:
    #         new_product_images.append(ProductImage(product=product, created_by=product.created_by, **product_image_data))
    #     ProductImage.objects.bulk_create(new_product_images)
    #     return product


class GetProductSerializer(serializers.ModelSerializer):
    category = GetCategorySerializer()
    product_prices = ProductPriceSerializer(many=True)
    product_images = ProductImageSerializer(many=True)
    created_by = serializers.SlugRelatedField(slug_field='username',
                                              read_only=True)

    # def get_product_prices(self, product: Product):
    #     return ProductPrice.objects.filter(product=product)

    # def get_product_images(self, product: Product):
    #     return ProductPrice.objects.filter(product=product)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "category",
            "seller",
            "stock",
            "product_prices",
            "product_images",
            "created_by"
        ]
