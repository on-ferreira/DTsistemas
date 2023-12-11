from django.urls import path
from .views import collector_view

urlpatterns = [
    path('', collector_view, name='collector'),
]