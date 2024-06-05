"""Orders Models"""
from django.db import models
from django.contrib.auth.models import User
from users.models import Company
from products.models import Product
from django.db import transaction

# Create your models here.
  
class Order(models.Model):
  supplier = models.ForeignKey(Company, related_name='supplied_orders', on_delete=models.PROTECT) 
  customer = models.ForeignKey(Company, related_name='purchased_orders', on_delete=models.PROTECT) 
  created_at = models.DateTimeField(auto_now_add=True)
  created_by = models.ForeignKey(User, related_name='created_orders', on_delete=models.PROTECT)
  
  def __str__(self):
    return str(self.id)
  

class OrderItem(models.Model):
  order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
  product = models.ForeignKey(Product, related_name='order_items', on_delete=models.PROTECT) 
  unit_price = models.DecimalField(decimal_places=5, max_digits=20)
  qty = models.PositiveIntegerField()
  created_at = models.DateTimeField(auto_now_add=True)
  created_by = models.ForeignKey(User, related_name='created_order_items', on_delete=models.PROTECT)
  
  def __str__(self):
    return str(self.id)
  
  @staticmethod
  @transaction.atomic
  def bulk_create_order_items(order_items_data,order_id, created_by_id):
    results = 200
    new_order_items = []
    failed = []
    for order_item_data in order_items_data:
          product = Product.objects.filter(id=order_item_data.get('product'))
          if not product:
                failed.append({'product':order_item_data.get('product'), 'error':'Product not found.'})
                continue
          
          product = product.first()
          if int(order_item_data.get('qty')) > product.stock:
                failed.append({'product':product.name, 'error':'Not enough stock.'})
                continue
          
          product.stock = product.stock - int(order_item_data.get('qty')) 
          product.save()

          new_order_item = OrderItem(
             order_id=order_id,
             created_by_id=created_by_id,
             unit_price=order_item_data.get('unit_price'),
             qty=order_item_data.get('qty'),
             product_id=order_item_data.get('product')
          )
          new_order_items.append(new_order_item)
    OrderItem.objects.bulk_create(new_order_items)
  
    return results, failed