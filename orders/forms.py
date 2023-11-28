from django.forms import ModelForm

from orders.models import Order


class OrderForm(ModelForm):

    class Meta:
        model = Order
        fields = ("full_name", "email", "address", "phone", "comment")
