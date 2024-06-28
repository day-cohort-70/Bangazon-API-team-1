from django.views.generic import TemplateView
from ..models import Order
from rest_framework import serializers

class OrdersReportView(TemplateView):
    template_name = 'ordersreport.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Fetch incomplete orders
        orders = Order.objects.filter(payment_type__isnull=True)
        
        # Serialize orders with total price calculation
        serializer = IncompleteOrderSerializer(orders, many=True, context={'request': self.request})
        
        # Assign serialized data to the context
        context['my_orders'] = serializer.data
        
        return context

class IncompleteOrderSerializer(serializers.ModelSerializer):
    """JSON serializer for customer orders"""
    customer_name = serializers.CharField(source='customer.user.last_name', read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'customer_name', 'total_price')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Calculate the total price by summing the prices of all related OrderProducts
        total_price = instance.calculate_total_price()
        if total_price is not None:
            representation['total_price'] = total_price
        else:
            representation['total_price'] = 0
        return representation