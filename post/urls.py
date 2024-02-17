from django.urls import path
from . import views
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView
urlpatterns = [
    path("", PostListView.as_view(), name="post-home"),
    path("new/", PostCreateView.as_view(), name="post-create"),
    path("news/", views.create_post, name="post-creates"),
    path("<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("<int:pk>/update/", PostUpdateView.as_view(), name="post-update"),
    path("<int:pk>/delete/", PostDeleteView.as_view(), name="post-delete"),
    # path("create/", views.create_post, name="post-create"),
]
