from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from orders.forms import OrderForm
from orders.models import Cart, CartItem, Order
from products.models import Product


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


class OrderCreateView(CreateView):
    template_name = 'orders/order-create.html'
    form_class = OrderForm
    success_url = reverse_lazy('orders:order_list')

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        cart = Cart.objects.get(user=self.request.user)
        form.instance.cart_history = cart.to_json()
        cart.delete()
        return super(OrderCreateView, self).form_valid(form)


class OrderListView(ListView):
    template_name = "orders/order-list.html"
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(initiator=self.request.user)


class OrderDetailView(DetailView):
    template_name = 'orders/order-detail.html'
    model = Order
    context_object_name = "order"
