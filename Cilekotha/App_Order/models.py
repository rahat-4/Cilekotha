from django.db import models
from django.conf import settings

from App_Shop.models import Product

# Create your models here.
class Cart(models.Model):
    item = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_cart')
    quantity = models.IntegerField(default=1)
    purchased = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.quantity} X {self.item.name}'
    
    def get_total(self):
        total = self.quantity * self.item.price
        float_total = format(total, '.2f')
        return float_total

class Order(models.Model):
    order_items = models.ManyToManyField(Cart)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_order")
    ordered = models.BooleanField(default=False)
    payment_id = models.CharField(max_length=264, blank=True, null=True)
    order_id = models.CharField(max_length=264, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return self.user.email
    
    def total_order(self):
        total = 0
        for order_item in self.order_items.all():
            total += float(order_item.get_total())
        return total