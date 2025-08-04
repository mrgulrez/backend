from django.urls import path
from .views import (
    message_list, message_detail,
    build_list, build_detail, set_delivery,
    delivery_list, delivery_detail,
    create_order, verify_payment, order_detail, order_list, update_tracking, bulk_update_orders
)
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


urlpatterns = [
    # Messages
    path('messages/', message_list, name='message-list'),
    path('messages/<int:pk>/', message_detail, name='message-detail'),

    # Builds
    path('builds/', build_list, name='build-list'),
    path('builds/<str:build_id>/', build_detail, name='build-detail'),
    path('builds/<str:build_id>/set_delivery/', set_delivery, name='set-delivery'),

    # Deliveries
    path('deliveries/', delivery_list, name='delivery-list'),
    path('deliveries/<str:delivery_id>/', delivery_detail, name='delivery-detail'),

    path('orders/bulk-update/', bulk_update_orders, name='bulk-update-orders'),
    path('orders/create/', create_order, name='create-order'),
    path('orders/verify-payment/', verify_payment, name='verify-payment'),
    path('orders/<str:order_id>/', order_detail, name='order-detail'),
    path('orders/', order_list, name='order-list'),
    path('orders/<str:order_id>/tracking/', update_tracking, name='update-tracking'),


    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]