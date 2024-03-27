"""Orders Models"""
from django.db import models
from django.contrib.auth.models import User
from users.models import Company

# Create your models here.
  
class Order(models.Model):
  supplier = models.ForeignKey(Company, related_name='supplied_orders', on_delete=models.PROTECT) # [pending merge with company models]
  customer = models.ForeignKey(Company, related_name='purchased_orders', on_delete=models.PROTECT) # [pending merge with company models
  created_at = models.DateTimeField(auto_now_add=True)
  created_by = models.ForeignKey(User, related_name='created_orders', on_delete=models.PROTECT)
  
  def __str__(self):
    return str(self.id)
  

class OrderItem(models.Model):
  order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
#   product = models.ForeignKey(Product, related_name='order_items', on_delete=models.PROTECT) # [pending merge with product models]
  unit_price = models.DecimalField(decimal_places=5, max_digits=20)
  qty = models.PositiveIntegerField()
  created_at = models.DateTimeField(auto_now_add=True)
  created_by = models.ForeignKey(User, related_name='created_order_items', on_delete=models.PROTECT)
  
  def __str__(self):
    return str(self.id)