from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart


# Create your views here.


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            form.instance.client = request.user
            order = form.save()
            for obj in cart:
                OrderItem.objects.create(order=order,
                                         item=obj['item'],
                                         price=obj['price'],
                                         quantity=obj['quantity'])
            cart.clear()
            return render(request, 'order_app/order_detail.html', {'order': order})
    else:
        form = OrderCreateForm
    return render(request, 'order_app/order_create.html', {'cart': cart, 'form': form})
