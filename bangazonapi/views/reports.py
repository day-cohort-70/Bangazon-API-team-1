from django.shortcuts import render
from ..models import Product


def expensive_products_report(request):
    # print("Expensive products report view called")
    # Query the database for products priced at $1000 or more
    expensive_products = Product.objects.filter(price__gte=1000)
    print(f"Found {expensive_products.count()} expensive products")

    # Render the template with the queried data
    return render(
        request, "expensive_products_report.html", {"products": expensive_products}
    )
  


def inexpensive_products_report(request):
    inexpensive_products = Product.objects.filter(price__lte=999)
    print(f"Found {inexpensive_products.count()} inexpensive products less than $1000")

    return render(
        request, "inexpensive_products_report.html", {"products": inexpensive_products}
    )

from bangazonapi.models import *


def CompletedOrders(request):

    orders = Order.objects.filter(payment_type__isnull=False)
    

    return render(request, 'completedorders.html', {'orders': orders})

