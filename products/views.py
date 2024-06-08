from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
import django_filters.rest_framework
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db import transaction

from .serializers import (
    CreateCategorySerializer,
    CreateProductSerializer,
    GetCategorySerializer,
    GetProductSerializer,
    ProductImageSerializer,
    ProductPriceSerializer,
)
import json
from .models import Category, Product, ProductImage, ProductPrice


# class CategoryAPIView(APIView):
#     def post(self, request):
#         serializer = CreateCategorySerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(created_by=request.user)  # pass current user
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def get(self, request, pk=None):
#         if pk:
#             try:
#                 category = Category.objects.get(pk=pk)
#                 serializer = GetCategorySerializer(category)
#                 return Response(serializer.data)
#             except Category.DoesNotExist:
#                 return Response({"error": "Category not found"},
#                                 status=status.HTTP_404_NOT_FOUND)
#         else:
#             categories = Category.objects.all()
#             serializer = GetCategorySerializer(categories, many=True)
#             return Response(serializer.data)


# class ProductAPIView(APIView):
#     def post(self, request):
#         serializer = CreateProductSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(created_by=request.user)  # pass current user
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryViewSet(ModelViewSet):
    """Category View Set"""

    queryset = Category.objects.all()
    filter_backends = [
        django_filters.rest_framework.DjangoFilterBackend, SearchFilter]
    search_fields = ("name",)
    filterset_fields = {"name": ["exact", "in"]}
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return GetCategorySerializer
        return CreateCategorySerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return AllowAny
        return super().get_permissions()

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        data = request.data
        try:
            data._mutable = True
        except AttributeError as error:
            print(str(error))
        data["created_by"] = request.user.id
        return super().create(request, *args, **kwargs)


class ProductViewSet(ModelViewSet):
    """Product View Set"""

    queryset = Product.objects.all()
    filter_backends = [
        django_filters.rest_framework.DjangoFilterBackend, SearchFilter]
    search_fields = (
        "name",
        "seller__name",
        "category__name",
    )
    filterset_fields = {
        "name": ["exact", "in"],
        "seller__id": ["exact", "in"],
        "category__id": ["exact", "in"],
        "category__name": ["exact", "in"],
    }
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return GetProductSerializer
        return CreateProductSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        data = request.data

        product_prices_data = data.get("product_prices")
        if product_prices_data and isinstance(product_prices_data, str):
            product_prices_data = request.data.getlist("product_prices")

        try:
            data._mutable = True
        except AttributeError as error:
            print(str(error))
        data["created_by"] = request.user.id

        response = super().create(request, *args, **kwargs)
        if response.status_code == 201:
            product_images_data = request.data.getlist("product_images")

            new_product_prices = []

            for product_price_data in product_prices_data:
                if isinstance(product_price_data, str):
                    product_price_data = json.loads(product_price_data)
                    print("product_price_data", product_price_data)

                new_product_prices.append(
                    ProductPrice(
                        product_id=response.data.get("id"),
                        created_by=request.user,
                        **product_price_data,
                    )
                )
            ProductPrice.objects.bulk_create(new_product_prices)

            new_product_images = []
            for product_image_data in product_images_data:
                new_product_images.append(
                    ProductImage(
                        product_id=response.data.get("id"),
                        created_by=request.user,
                        image=product_image_data,
                    )
                )
            ProductImage.objects.bulk_create(new_product_images)
        return response


class ProductPriceViewSet(ModelViewSet):
    """Product Prices View Set"""

    queryset = ProductPrice.objects.all()
    filter_backends = [
        django_filters.rest_framework.DjangoFilterBackend, SearchFilter]
    search_fields = (
        "product__name",
        "product__seller__name",
    )
    filterset_fields = {
        "product__id": ["exact", "in"],
        "product__name": ["exact", "in"],
        "product__seller__id": ["exact", "in"],
    }
    permission_classes = [IsAuthenticated]
    serializer_class = ProductPriceSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        data = request.data
        try:
            data._mutable = True
        except AttributeError as error:
            print(str(error))
        data["created_by"] = request.user.id
        return super().create(request, *args, **kwargs)
