from django.db import models
from django.core.validators import MinValueValidator


class Order(models.Model):
    """Модель заказов."""
    STATUS_CHOICES = [
        ('pending', 'В ожидании'),
        ('ready', 'Готово'),
        ('paid', 'Оплачено'),
    ]

    table_number = models.PositiveIntegerField(
        verbose_name="Номер стола",
        validators=[MinValueValidator(1)]
    )

    items = models.JSONField(
        verbose_name="Блюда",
        help_text="Список блюд с ценами в формате "
        "[{'name': 'Суп', 'price': 200}]"
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Общая стоимость",
        default=0.0
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Статус заказа"
    )

    def save(self, *args, **kwargs):
        self.total_price = sum(item['price'] for item in self.items)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Заказ {self.id} для стола {self.table_number}"
