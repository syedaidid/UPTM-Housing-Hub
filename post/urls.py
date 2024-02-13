from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="post-home"),
    path("create/", views.create_post, name="post-create"),
]
