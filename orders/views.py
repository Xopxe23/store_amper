from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render

from products.models import Product

from .models import Cart, CartItem


@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.cartitem_set.all()
    context = {'cart': cart, 'cart_items': cart_items}
    return render(request, 'orders/view-cart.html', context)


@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(pk=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    cart_item.quantity += 1
    cart_item.save()
    return HttpResponseRedirect(request.META["HTTP_REFERER"])


def add_quantity(request, cart_item_id: int):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    cart_item.quantity += 1
    cart_item.save()
    return HttpResponseRedirect(request.META["HTTP_REFERER"])


def subtract_quantity(request, cart_item_id: int):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
    cart_item.save()
    return HttpResponseRedirect(request.META["HTTP_REFERER"])


@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = CartItem.objects.get(id=cart_item_id)
    cart_item.delete()
    return HttpResponseRedirect(request.META["HTTP_REFERER"])
