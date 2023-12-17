from django.urls import path
from . import views

urlpatterns = [
    path("get_active_projects/", views.get_active_projects, name="get_active_projects"),
    path("comunication_harverster_synthesis/", views.comunication_harverster_synthesis,
         name="comunication_harverster_synthesis"),
    path("purge_old_data/", views.purge_old_data, name="purge_old_data")
]