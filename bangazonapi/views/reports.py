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
  
from bangazonapi.models import *


def CompletedOrders(request):

    orders = Order.objects.filter(payment_type__isnull=False)
    

    return render(request, 'completedorders.html', {'orders': orders})

