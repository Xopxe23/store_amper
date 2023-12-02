from django.urls import path

from orders.views import (OrderCreateView, OrderDetailView, OrderListView,
                          OrderUpdateView, add_quantity, add_to_cart,
                          export_orders_to_excel, remove_from_cart,
                          subtract_quantity, view_cart)

app_name = 'orders'

urlpatterns = [
    path('view/', view_cart, name='view-cart'),
    path('add/<int:product_id>/', add_to_cart, name='add-to-cart'),
    path('add_quantity/<int:cart_item_id>/', add_quantity, name='add-quantity'),
    path('subtract_quantity/<int:cart_item_id>/', subtract_quantity, name='subtract-quantity'),
    path('remove/<int:cart_item_id>/', remove_from_cart, name='remove-from-cart'),
    path('create_order/', OrderCreateView.as_view(), name='create-order'),
    path('order_list/', OrderListView.as_view(), name='order-list'),
    path('order_detail/<int:pk>', OrderDetailView.as_view(), name='order-detail'),
    path('order_update/<int:pk>', OrderUpdateView.as_view(), name='order-update'),
    path('export-orders-to-excel/', export_orders_to_excel, name='export-orders-to-excel'),
]
