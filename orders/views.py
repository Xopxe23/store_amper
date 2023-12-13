import io
from datetime import timezone

from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.utils.encoding import force_str
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from openpyxl.workbook import Workbook

from orders.forms import ChangeOrderStatusForm, OrderForm
from orders.models import Cart, CartItem, Order
from products.models import Product


@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart.calculate_totals()  # Предварительно загружаем агрегированные значения
    cart_items = cart.cartitem_set.select_related('product').all()  # Получаем все товары в корзине
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'total_price': cart.total_price,
        'total_quantity': cart.total_quantity
    }

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
    success_url = reverse_lazy('orders:order-list')

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
        if self.request.user.is_staff:
            return Order.objects.all().order_by('status', '-created_at')
        return Order.objects.filter(initiator=self.request.user).order_by('status', '-created_at')


class OrderDetailView(DetailView):
    template_name = 'orders/order-detail.html'
    model = Order
    context_object_name = "order"


class OrderUpdateView(UpdateView):
    template_name = 'orders/order-update.html'
    model = Order
    form_class = ChangeOrderStatusForm
    context_object_name = "order"

    def get_success_url(self):
        return reverse_lazy("orders:order-detail", args=[self.object.pk])


@user_passes_test(lambda user: user.is_staff)
def export_orders_to_excel(request):
    # Получите данные о заказах, которые вам нужны для статистики
    orders = Order.objects.all()

    # Создайте новый файл Excel и добавьте в него данные
    workbook = Workbook()

    # Лист для заказов
    worksheet_orders = workbook.active
    worksheet_orders.title = 'Orders'

    # Заголовки для листа заказов
    worksheet_orders.append(['Order ID', 'User', 'Total Price', 'Date Created'])

    # Добавление данных для заказов
    for order in orders:
        date_created_utc = order.created_at.astimezone(timezone.utc).replace(tzinfo=None)
        worksheet_orders.append([order.id, order.initiator.email, order.cart_history["total_price"], date_created_utc])

    worksheet_products = workbook.create_sheet(title='Products')  # Лист для продуктов

    # Заголовки для листа продуктов
    worksheet_products.append(['Product Name', 'Total Quantity Sold', 'Total Sales Amount'])
    products_info = {}  # Словарь для хранения информации о продуктах

    # Обработка заказов для получения информации о продуктах
    for order in orders:
        for item in order.cart_history["items"]:
            product_name = item["product"]
            quantity_sold = item["quantity"]
            total_price = item["total_price"]

            if product_name in products_info:
                # Если продукт уже встречался, обновляем информацию
                products_info[product_name]['quantity_sold'] += quantity_sold
                products_info[product_name]['total_sales'] += total_price
            else:
                # Если продукт встречается впервые, добавляем информацию
                products_info[product_name] = {
                    'quantity_sold': quantity_sold,
                    'total_sales': total_price
                }

    # Добавление информации о продуктах на лист
    for product_name, info in products_info.items():
        worksheet_products.append([product_name, info['quantity_sold'], info['total_sales']])

    # Добавление строки с общими данными внизу таблицы с продуктами
    total_quantity_all_products = sum(info['quantity_sold'] for info in products_info.values())
    total_sales_all_products = sum(info['total_sales'] for info in products_info.values())
    worksheet_products.append(['Total', total_quantity_all_products, total_sales_all_products])

    excel_data = io.BytesIO()  # Создание байтового объекта для временного хранения файла в памяти
    workbook.save(excel_data)  # Сохранение книги в байтовый объект
    excel_data.seek(0)  # Перемотка байтового объекта в начало

    # Создание HTTP-ответа с содержимым файла Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = force_str('attachment; filename=orders_statistics.xlsx')
    response.write(excel_data.read())

    return response
