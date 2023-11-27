from django.urls import path

from products.views import ProductListView

app_name = 'products'

urlpatterns = [
    path("", ProductListView.as_view(), name='product-list'),
    path("page/<int:page>/", ProductListView.as_view(), name='paginator'),
    path('category/<int:category_id>/', ProductListView.as_view(), name='category')
]
