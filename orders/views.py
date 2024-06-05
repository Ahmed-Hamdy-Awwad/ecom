"""Order Views"""
import django_filters.rest_framework
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from .serializers import OrderSerializer, GetOrderSerializer, OrderItemSerializer, GetOrderItemSerializer
from rest_framework.viewsets import ModelViewSet
from .models import Order, OrderItem
from django.db import transaction


class OrderViewSet(ModelViewSet):
    """Order View Set"""
    queryset = Order.objects.all()
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, SearchFilter]
    search_fields = ('order_items__product__name','supplier__name','customer__name',)
    filterset_fields = {
        'supplier__name': ['exact', 'in'],
        'customer__name': ['exact', 'in'], 
        'order_items__product__category__id': ['exact', 'id']
        }
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return GetOrderSerializer
        return OrderSerializer
      
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        data = request.data
        try:
            data._mutable = True
        except (AttributeError) as error:
            print(str(error))
        data['created_by'] = request.user.id
        response = super().create(request, *args, **kwargs)
        if response.status_code ==201:
            # Bulk Create Order Items
            results = OrderItem.bulk_create_order_items(request.data.get('order_items'), response.data.get('id'), request.user.id)
        return response
    
class OrderItemViewSet(ModelViewSet):
    """Order Item View Set"""
    queryset = OrderItem.objects.all()
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, SearchFilter]
    search_fields = ('order__id','product__name',)
    filterset_fields = {
        'order__id': ['exact', 'in'],
        'product__name':['exact', 'in']
        }
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return GetOrderItemSerializer
        return OrderItemSerializer
      
    def create(self, request, *args, **kwargs):
        data = request.data
        try:
            data._mutable = True
        except (AttributeError) as error:
            print(str(error))
        data['created_by'] = request.user.id
        return super().create(request, *args, **kwargs)