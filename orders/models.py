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


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in {self.cart.user.email}'s cart"

    def total_price(self):
        total_sum = self.product.price * self.quantity
        return total_sum
