from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from users.models import EmailUser


class UserLoginForm(AuthenticationForm):

    class Meta:
        model = EmailUser
        fields = ("email", "password")


class UserRegistrationForm(UserCreationForm):

    class Meta:
        model = EmailUser
        fields = ("first_name", "last_name", "email", "password1", "password2")
