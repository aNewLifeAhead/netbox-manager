from django.urls import path
from . import views

app_name = "netbox_sync"

urlpatterns = [
    path("", views.home, name="home"),
]
