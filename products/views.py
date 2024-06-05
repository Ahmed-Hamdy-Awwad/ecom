from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
    CreateCategorySerializer,
    CreateProductSerializer,
    GetCategorySerializer,
    GetProductSerializer,
)

from .models import Category


class CategoryAPIView(APIView):
    def post(self, request):
        serializer = CreateCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)  # pass current user
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk=None):
        if pk:
            try:
                category = Category.objects.get(pk=pk)
                serializer = GetCategorySerializer(category)
                return Response(serializer.data)
            except Category.DoesNotExist:
                return Response({"error": "Category not found"},
                                status=status.HTTP_404_NOT_FOUND)
        else:
            categories = Category.objects.all()
            serializer = GetCategorySerializer(categories, many=True)
            return Response(serializer.data)


class ProductAPIView(APIView):
    def post(self, request):
        serializer = CreateProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)  # pass current user
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
