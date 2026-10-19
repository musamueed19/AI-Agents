from django.shortcuts import render
from .models import Order, Product, RefundRequest

# Create your views here.
def orders_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'orders': orders
    }

    return render(request, 'orders/orders_list.html', context)