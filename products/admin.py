from django.contrib import admin

from products.models import ProductCategory, Product


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("id", "name")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category", "price")
    list_display_links = ("id", "name")
    list_filter = ("category", )
