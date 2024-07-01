from django.db import models
from .customer import Customer


class Store (models.Model):

    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    seller = models.ForeignKey(Customer, on_delete=models.DO_NOTHING, related_name='seller')
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING, related_name='customer')