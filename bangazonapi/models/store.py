from django.db import models
from .customer import Customer


class Store (models.Model):

    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    seller = models.OneToOneField(Customer, on_delete=models.DO_NOTHING)