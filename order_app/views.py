from django.shortcuts import render, redirect
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from django.db.models import F
from shop.models import Item


# Create your views here.


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            form.instance.client = request.user
            order = form.save(commit=False)
            if cart.promocode:
                order.promocode = cart.promocode
                order.discount = cart.promocode.discount
            order.save()
            for obj in cart:
                ch_item = Item.objects.get(name=obj['item'])

                # тут проверяем чтобы пользователь не заказал больше чем есть

                # прикол в том что нельзя выбрать больше чем есть при заказе одного айтема за раз
                # но можно заказать больше если мы добавляем в корзину по несколько раз один и тот же айтем

                # дальше под уведомление пользователя об ошибке нужно будет добавить темплейт для редиректа
                # пока что редиректим обратно на список товаров и очищаем корзину
                # либо добавить логику вычитания при добавлении айтема в корзину

                if obj['quantity'] > ch_item.stock:
                    cart.clear()
                    return redirect('order_app:order_error')
                else:
                    OrderItem.objects.create(order=order,
                                             item=obj['item'],
                                             price=obj['price'],
                                             quantity=obj['quantity'])

                    # if item.stock equals to 0, we change it's available status to false
                    if ch_item.stock - obj['quantity'] == 0:
                        ch_item.available = False
                    # here we subtract stock values of an ordered items after order
                    ch_item.stock = F('stock') - obj['quantity']
                    ch_item.save()
                cart.clear()
                return render(request, 'order_app/order_detail.html', {'order': order})
    else:
        form = OrderCreateForm
    return render(request, 'order_app/order_create.html', {'cart': cart, 'form': form})


def order_error(request):
    return render(request, 'order_app/order_error.html')
