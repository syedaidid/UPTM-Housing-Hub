from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="static-home"),
    path("about/", views.about, name="static-about"),
]