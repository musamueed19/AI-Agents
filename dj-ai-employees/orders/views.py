from django.shortcuts import render
from .models import Order, Product, RefundRequest
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def orders_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'orders': orders
    }

    return render(request, 'orders/orders_list.html', context)

@login_required
def order_detail(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user)

    # get refund requests history for the order
    refund_requests = RefundRequest.objects.filter(order=order).order_by('-created_at')
    context = {
        'order': order,
        'refund_requests': refund_requests
    }

    return render(request, 'orders/order_detail.html', context)