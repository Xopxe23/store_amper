from django.urls import path

from users.views import UserLoginView, UserLogoutView, UserRegistrationView

app_name = 'users'

urlpatterns = [
    path("login/", UserLoginView.as_view(), name='login'),
    path("logout/", UserLogoutView.as_view(), name='logout'),
    path('register/', UserRegistrationView.as_view(), name='register'),
]
