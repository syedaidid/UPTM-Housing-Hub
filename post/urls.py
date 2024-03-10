from django.urls import path
from . import views
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, UserDetailView, PostListMapView
urlpatterns = [
    path("", PostListView.as_view(), name="post-home"),
    path("new/", views.create_post, name="post-create"),
    path("map/", PostListMapView.as_view(), name="post-map"),
    path("<int:pk>/update/", views.update_post, name="post-update"),
    path("<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("user/<int:pk>/", UserDetailView.as_view(), name="user-detail"),
    path("<int:pk>/delete/", PostDeleteView.as_view(), name="post-delete"),
    path("updates/delete-images", views.delete_images, name="post-delete-images"),
    # path("create/", views.create_post, name="post-create"),
]
