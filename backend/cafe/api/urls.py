from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path('api/', include(router.urls)),
    path('orders/', OrderViewSet.as_view({'get': 'order_list'}),
         name='order_list'),
    path('orders/add/', OrderViewSet.as_view(
        {'get': 'order_add', 'post': 'order_add'}), name='order_add'),
    path('orders/<int:pk>/', OrderViewSet.as_view(
        {'get': 'order_detail'}), name='order_detail'),
    path('orders/<int:pk>/edit/', OrderViewSet.as_view(
        {'get': 'order_edit', 'post': 'order_edit'}), name='order_edit'),
    path('orders/<int:pk>/delete/', OrderViewSet.as_view(
        {'get': 'delete_order', 'delete': 'delete_order'}),
        name='delete_order'),
    path('orders/search/', OrderViewSet.as_view(
        {'get': 'order_search'}), name='order_search'),
    path('revenue/', OrderViewSet.as_view(
        {'get': 'revenue_for_shift'}), name='revenue_for_shift'),
]
