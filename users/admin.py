from django.contrib import admin

from users.models import EmailUser


@admin.register(EmailUser)
class EmailUserAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "first_name", "last_name")
    list_display_links = ("id", "email")
