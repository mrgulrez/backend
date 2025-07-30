from django.urls import path
from .views import (
    message_list, message_detail,
    build_list, build_detail, set_delivery,
    delivery_list, delivery_detail
)

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
]