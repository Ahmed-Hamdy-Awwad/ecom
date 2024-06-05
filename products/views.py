from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
import django_filters.rest_framework
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from django.db import transaction

from .serializers import (
    CreateCategorySerializer,
    CreateProductSerializer,
    GetCategorySerializer,
    GetProductSerializer,
    ProductImageSerializer,
    ProductPriceSerializer
)

from .models import Category, Product,ProductImage,ProductPrice


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
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, SearchFilter]
    search_fields = ('name', )
    filterset_fields = {'name': ['exact', 'in']}
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return GetCategorySerializer
        return CreateCategorySerializer
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        data = request.data
        try:
            data._mutable = True
        except (AttributeError) as error:
            print(str(error))
        data['created_by'] = request.user.id
        return super().create(request, *args, **kwargs)
    

class ProductViewSet(ModelViewSet):
    """Product View Set"""
    queryset = Product.objects.all()
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, SearchFilter]
    search_fields = ('name', 'seller__name','category__name',)
    filterset_fields = {
        'name': ['exact', 'in'],
        'seller__id':['exact','in'],
        'category__id': ['exact', 'in'],
        }
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return GetProductSerializer
        return CreateProductSerializer
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        data = request.data
        try:
            data._mutable = True
        except (AttributeError) as error:
            print(str(error))
        data['created_by'] = request.user.id
        return super().create(request, *args, **kwargs)
    


class ProductPriceViewSet(ModelViewSet):
    """Product Prices View Set"""
    queryset = ProductPrice.objects.all()
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, SearchFilter]
    search_fields = ('product__name', 'product__seller__name',)
    filterset_fields = {
        'product__id': ['exact', 'in'],
        'product__name': ['exact', 'in'],
        'product__seller__id':['exact','in']
        }
    permission_classes = [IsAuthenticated]
    serializer_class = ProductPriceSerializer
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        data = request.data
        try:
            data._mutable = True
        except (AttributeError) as error:
            print(str(error))
        data['created_by'] = request.user.id
        return super().create(request, *args, **kwargs)