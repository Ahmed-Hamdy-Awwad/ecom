""" Orders Serializers """
from rest_framework import serializers
from .models import  Order, OrderItem


""" Orders """
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
    
class GetOrderSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %I:%M:%S %p")
    created_by = serializers.StringRelatedField()

    class Meta:
        model = Order
        fields = '__all__'


""" Order Items """
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'
    
class GetOrderItemSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %I:%M:%S %p")
    created_by = serializers.StringRelatedField()

    class Meta:
        model = OrderItem
        fields = '__all__'