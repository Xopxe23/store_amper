from django.db import models

from products.models import Product
from users.models import EmailUser


class Cart(models.Model):
    user = models.OneToOneField(EmailUser, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='CartItem')

    def __str__(self):
        return f"Cart for {self.user.email}"

    def total_price(self):
        cart_items = self.cartitem_set.all()
        total_sum = sum([item.total_price() for item in cart_items])
        return total_sum

    def total_quantity(self):
        cart_items = self.cartitem_set.all()
        total_sum = sum([item.quantity for item in cart_items])
        return total_sum

    def to_json(self):
        cart = {
            "items": [],
            "total_price": float(self.total_price()),
        }
        for item in self.cartitem_set.all():
            cart_item = {
                "product": item.product.name,
                "quantity": item.quantity,
                "total_price": float(item.total_price())
            }
            cart["items"].append(cart_item)
        return cart


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in {self.cart.user.email}'s cart"

    def total_price(self):
        total_sum = self.product.price * self.quantity
        return total_sum


class Order(models.Model):
    CREATED = 0
    PAID = 1
    ON_WAY = 2
    DELIVERED = 3
    STATUSES = (
        (CREATED, 'Создан'),
        (PAID, 'Оплачен'),
        (ON_WAY, 'В пути'),
        (DELIVERED, 'Доставлен'),
    )
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    address = models.CharField(max_length=256)
    phone = models.CharField(max_length=30)
    cart_history = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.SmallIntegerField(default=CREATED, choices=STATUSES)
    initiator = models.ForeignKey(EmailUser, on_delete=models.CASCADE)
    comment = models.TextField()

    def __str__(self):
        return f'Order #{self.pk} for {self.full_name}'
