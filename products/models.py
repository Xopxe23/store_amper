from django.db import models


class ProductCategory(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


def upload_to(instance, filename):
    # instance.category - это поле ForeignKey, связывающее продукт с категорией
    category_name = instance.category.name if instance.category else 'uncategorized'
    return f"{category_name}/{filename}"


class Product(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveSmallIntegerField(default=0)
    image = models.ImageField(upload_to=upload_to)
    category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return f'Продукт: {self.name} | Категория: {self.category.name}'
