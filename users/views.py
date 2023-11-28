from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.forms import UserLoginForm, UserRegistrationForm


class UserRegistrationView(SuccessMessageMixin, CreateView):
    model = User
    template_name = 'users/register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy("users:login")
    success_message = "Вы успешно зарегестрировались"


class UserLoginView(LoginView):
    template_name = "users/login.html"
    form_class = UserLoginForm
    next_page = reverse_lazy("home")


class UserLogoutView(LogoutView):
    next_page = reverse_lazy("home")
