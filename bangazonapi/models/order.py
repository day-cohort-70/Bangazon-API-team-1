"""Customer order model"""
from django.db import models
from .customer import Customer
from .payment import Payment


# models/order.py
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    payment_type = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True)
    created_date = models.DateField(default="0000-00-00")

    def calculate_total_price(self):
        total_price = sum([op.product.price for op in self.lineitems.all()])
        return total_price