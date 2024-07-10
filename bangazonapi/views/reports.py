from django.shortcuts import render
from bangazonapi.models import *


def CompletedOrders(request):

    orders = Order.objects.filter(payment_type__isnull=False)
    

    return render(request, 'completedorders.html', {'orders': orders})