from rest_framework import serializers

from .models import Category, Product, ProductImage, ProductPrice


class CreateBaseSerializer(serializers.ModelSerialzer):
    class Meta:
        exclude = ['created_by',]


class GetBaseSerializer(serializers.ModelSerialzer):
    created_by = serializers.SlugRelatedField(slug_field='username',
                                              read_only=True)


class CreateCategorySerializer(CreateBaseSerializer):
    class Meta:
        model = Category


class GetCategorySerializer(GetBaseSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductImageSerializer(serializers.Serializer):
    class Meta:
        model = ProductImage
        exclude = ['created_by', 'created_at']


class ProductPriceSerializer(serializers.Serializer):
    class Meta:
        model = ProductPrice
        exclude = ['created_by', 'created_at']


class CreateProductSerializer(CreateBaseSerializer):
    product_prices = ProductPriceSerializer(many=True)
    product_images = ProductImageSerializer(many=True)

    class Meta:
        model = Product
        fields = [
            "name",
            "category",
            "seller",
            "stock",
            "product_prices",
            "product_images"
        ]

    def create(self, validated_data):
        product_prices_data = validated_data.pop('product_prices')
        product_images_data = validated_data.pop('product_images')

        product = Product.objects.create(**validated_data)

        for product_price_data in product_prices_data:
            ProductPrice.objects.create(product=product, **product_price_data)

        for product_image_data in product_images_data:
            ProductImage.objects.create(product=product, **product_image_data)

        return product


class GetProductSerializer(GetBaseSerializer):
    product_prices = serializers.SerializerMethodField()
    product_images = serializers.SerializerMethodField()

    def get_product_prices(self, product: Product):
        return ProductPrice.objects.filter(product=product)

    def get_product_images(self, product: Product):
        return ProductPrice.objects.filter(product=product)

    class Meta:
        model = Product
        fields = [
            "name",
            "category",
            "seller",
            "stock",
            "product_prices",
            "product_images"
        ]