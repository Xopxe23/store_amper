from django.urls import path

from orders.views import (OrderCreateView, OrderDetailView, OrderListView,
                          add_quantity, add_to_cart, remove_from_cart,
                          subtract_quantity, view_cart)

app_name = 'orders'

urlpatterns = [
    path('view/', view_cart, name='view_cart'),
    path('add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('add_quantity/<int:cart_item_id>/', add_quantity, name='add_quantity'),
    path('subtract_quantity/<int:cart_item_id>/', subtract_quantity, name='subtract_quantity'),
    path('remove/<int:cart_item_id>/', remove_from_cart, name='remove_from_cart'),
    path('create_order/', OrderCreateView.as_view(), name='create_order'),
    path('order_list/', OrderListView.as_view(), name='order_list'),
    path('order_detail/<int:pk>', OrderDetailView.as_view(), name='order_detail'),
]
