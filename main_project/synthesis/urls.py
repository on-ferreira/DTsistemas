from django.urls import path
from .views import synthesis_view

urlpatterns = [
    path('', synthesis_view, name='synthesis'),
]