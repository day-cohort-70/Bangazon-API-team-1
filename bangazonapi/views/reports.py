from django.shortcuts import render
from ..models import Product
from bangazonapi.models import *


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





def CompletedOrders(request):

    query_param = request.GET.get('status', None)
    orders = Order.objects.all()

    if query_param == 'complete':
        orders = Order.objects.filter(payment_type__isnull=False)

    if query_param == 'incomplete':
        orders = Order.objects.filter(payment_type__isnull=True)

    return render(request, 'completedorders.html', {'orders': orders})


def FavoriteSellers(request):

    query_param = request.GET.get('customer', None)
    favorite_sellers = None
    customer = None
    
    if query_param is not None:
        customer_id = int(query_param)
        customer = Customer.objects.get(pk=customer_id)
        favorite_sellers = Favorite.objects.filter(customer_id=customer_id)

    return render(request, 'favoritesellers.html', {'sellers': favorite_sellers, 'customer': customer})