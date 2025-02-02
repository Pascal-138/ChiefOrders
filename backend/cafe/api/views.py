from typing import Optional, Union
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from order.models import Order
from .serializers import OrderSerializer
from django.db.models import QuerySet


class OrderViewSet(viewsets.ModelViewSet):
    """Сериализатор для модели Order."""
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @action(detail=False, methods=['get'])
    def order_list(self, request: Request) -> HttpResponse:
        """Метод для показа списка всех заказов с фильтрацией по статусу."""
        status_filter: str = request.GET.get('status', '')
        orders: QuerySet = self.queryset
        if status_filter:
            orders = orders.filter(status=status_filter)
        return render(request, 'orders/order_list.html', {'orders': orders})

    @action(detail=True, methods=['get'], url_path='detail')
    def order_detail(self, request: Request,
                     pk: Optional[int] = None) -> HttpResponse:
        """Метод для показа страницы заказа."""
        order: Order = get_object_or_404(Order, pk=pk)
        return render(request, 'orders/order_detail.html', {'order': order})

    @action(detail=False, methods=['get', 'post'])
    def order_add(self, request: Request) -> Union[HttpResponse, Response]:
        """Метод добавления заказа с валидацией."""
        if request.method == "POST":
            table_number: str = request.POST.get("table_number", "").strip()
            items: str = request.POST.get("items", "").strip()

            serializer = OrderSerializer(data={
                'table_number': table_number,
                'items': items,
                'status': 'pending'
            })

            if serializer.is_valid():
                serializer.save()
                return redirect('order_list')
            else:
                return render(request, 'orders/order_add.html', {
                    'error': serializer.errors,
                    'table_number': table_number,
                    'items': items
                })

        return render(request, 'orders/order_add.html')

    @action(detail=True, methods=['get', 'post'])
    def order_edit(self, request: Request,
                   pk: Optional[int] = None) -> Union[HttpResponse, Response]:
        """Метод для редактирования статуса заказа."""
        order: Order = get_object_or_404(Order, pk=pk)

        if request.method == 'POST':
            status_value: str = request.POST.get('status', '').strip()

            serializer = OrderSerializer(order,
                                         data={'status': status_value},
                                         partial=True)

            if serializer.is_valid():
                serializer.save()
                return redirect('order_detail', pk=order.id)
            else:
                return render(request, 'orders/order_edit.html', {
                    'order': order,
                    'error': serializer.errors
                })

        return render(request, 'orders/order_edit.html', {
            'order': order
        })

    @action(detail=True, methods=['get', 'delete'])
    def delete_order(self, request: Request,
                     pk: Optional[int] = None) -> HttpResponse:
        """Метод для удаления заказа."""
        order: Order = get_object_or_404(Order, pk=pk)
        order.delete()
        return redirect('order_list')

    @action(detail=False, methods=['get'])
    def order_search(self, request: Request) -> HttpResponse:
        """Метод для поиска страницы заказа."""
        table_number: str = request.GET.get('table_number', '').strip()
        status_filter: str = request.GET.get('status', '').strip()
        orders: QuerySet = self.queryset

        if table_number:
            if not table_number.isdigit() or int(table_number) < 1:
                return render(request, 'orders/order_search.html', {
                    'error': "Номер стола должен быть целым числом "
                    "больше или равным 1.",
                    'table_number': table_number,
                })
            orders = orders.filter(table_number=table_number)
        if status_filter:
            orders = orders.filter(status=status_filter)

        return render(request, 'orders/order_search.html', {'orders': orders})

    @action(detail=False, methods=['get'])
    def revenue_for_shift(self, request: Request) -> HttpResponse:
        """Метод для расчета стоимости оплаченных заказов."""
        paid_orders: QuerySet = self.queryset.filter(status='paid')
        total_revenue: float = sum(order.total_price for order in paid_orders)
        return render(request, 'orders/revenue_for_shift.html',
                      {'total_revenue': total_revenue})
