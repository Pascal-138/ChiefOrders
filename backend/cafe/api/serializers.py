from rest_framework import serializers
from typing import Any, Dict, List, Union
from order.models import Order
import json


class OrderSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Order."""
    table_number = serializers.IntegerField(min_value=1)

    class Meta:
        model = Order
        fields = '__all__'

    @staticmethod
    def validate_items(value: str) -> List[Dict[str, Union[str, float]]]:
        """Метод для валидации списка заказа."""
        try:
            parsed_items: Any = json.loads(value)
            if not isinstance(parsed_items, list) or any(
                not isinstance(item, dict) or 'name' not in
                item or 'price' not in item
                for item in parsed_items
            ):
                raise ValueError("Некорректный формат блюд.")
        except (json.JSONDecodeError, ValueError):
            raise serializers.ValidationError("Некорректный формат "
                                              "блюд. Проверьте JSON.")
        return parsed_items

    def create(self, validated_data: Dict[str, Any]) -> Order:
        """Метод для создания заказа."""
        return Order.objects.create(**validated_data)

    def update(self, instance: Order, validated_data: Dict[str, Any]) -> Order:
        """Метод для изменения статуса заказа."""
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance

    def delete(self, instance: Order) -> None:
        """Метод для удаления заказа."""
        if instance.status == 'paid':
            raise serializers.ValidationError(
                "Нельзя удалить оплаченный заказ.")
        instance.delete()
