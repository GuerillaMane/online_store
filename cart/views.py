from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Item
from .cart import Cart
from .forms import CartAddForm
from promocodes.forms import PromoCodeApplyForm


# Create your views here.


@require_POST
def cart_add(request, item_id):
    cart = Cart(request)
    item = get_object_or_404(Item, id=item_id)
    form = CartAddForm(request.POST)
    if form.is_valid() and form.cleaned_data['quantity'] > item.stock:
        return redirect('cart:cart_error')
    if form.is_valid() and form.cleaned_data['quantity'] <= item.stock:
        cd = form.cleaned_data
        cart.add(item=item, quantity=cd['quantity'], update_quantity=cd['update'])
    return redirect('cart:cart_detail')


def cart_remove(request, item_id):
    cart = Cart(request)
    item = get_object_or_404(Item, id=item_id)
    cart.remove(item)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    promocode_form = PromoCodeApplyForm()
    return render(request, 'cart/cart_detail.html', {'cart': cart, 'promocode_form': promocode_form})


def cart_error(request):
    return render(request, 'cart/cart_error.html')
