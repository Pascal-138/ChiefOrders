from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from order.models import Order
import json


class OrderViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.order_data = [
            {
                "table_number": 5,
                "items": [
                    {"name": "Pizza", "price": 200}
                ],
                "status": "pending"
            },
            {
                "table_number": 6,
                "items": [
                    {"name": "Soda", "price": 30}
                ],
                "status": "pending"
            }
        ]

        self.orders = []
        for data in self.order_data:
            self.orders.append(Order.objects.create(**data))

        self.order = self.orders[0]

    def test_create_order(self):
        url = reverse('order-list')
        items_data = [{"name": "Pizza", "price": 200}]
        items_json = json.dumps(items_data)

        data = {
            "table_number": 5,
            "items": items_json,
            "status": "pending"
        }

        response = self.client.post(url, data=data, format='json')
        print(response.json())

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 3)

    def test_update_order_status(self):
        url = reverse('order-detail', kwargs={'pk': self.order.pk})
        data = {"status": "paid"}
        response = self.client.patch(url, data, format='json')
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, "paid")

    def test_get_order_list(self):
        url = reverse('order-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.json()), 1)

    def test_get_order_detail(self):
        url = reverse('order-detail', kwargs={'pk': self.order.pk})
        response = self.client.get(url, format='json',
                                   HTTP_ACCEPT='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data['table_number'],
                         self.order_data[0]['table_number'])

    def test_delete_order(self):
        order = self.orders[0]
        url = reverse('order-detail', kwargs={'pk': order.pk})

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Order.objects.filter(pk=order.pk).exists())
