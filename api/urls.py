from django.urls import path
from . import views
from .views import BuildListCreateView, BuildDetailView
urlpatterns = [
    path('', views.messages_view, name='landing_page'),
    path('builds/', BuildListCreateView.as_view(), name='build-list-create'),
    path('builds/<str:build_id>/', BuildDetailView.as_view(), name='build-detail'),
]