from django.urls import path
from . import views
urlpatterns = [
    path('', views.messages_view, name='landing_page'),
]