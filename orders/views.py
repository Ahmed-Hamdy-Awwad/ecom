"""Order Views"""
import django_filters.rest_framework
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from .serializers import OrderSerializer, GetOrderSerializer, OrderItemSerializer, GetOrderItemSerializer
from rest_framework.viewsets import ModelViewSet
from .models import Order, OrderItem


class OrderViewSet(ModelViewSet):
    """Order View Set"""
    queryset = Order.objects.all()
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, SearchFilter]
    search_fields = ()
    filterset_fields = {}
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return GetOrderSerializer
        return OrderSerializer
      
    def create(self, request, *args, **kwargs):
        data = request.data
        data._mutable = True
        data['created_by'] = request.user.id
        return super().create(request, *args, **kwargs)
    
class OrderItemViewSet(ModelViewSet):
    """Order Item View Set"""
    queryset = OrderItem.objects.all()
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, SearchFilter]
    search_fields = ()
    filterset_fields = {'order__id': ['exact', 'in']}
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return GetOrderItemSerializer
        return OrderItemSerializer
      
    def create(self, request, *args, **kwargs):
        data = request.data
        data._mutable = True
        data['created_by'] = request.user.id
        return super().create(request, *args, **kwargs)