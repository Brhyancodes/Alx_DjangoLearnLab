from django.urls import path
from .views import (
    RegisterView,
    MyLoginView,
    MyLogoutView,
    profile,
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
)

urlpatterns = [
    # Authentication URLs
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", MyLoginView.as_view(), name="login"),
    path("logout/", MyLogoutView.as_view(), name="logout"),
    path("profile/", profile, name="profile"),
    # Blog Post URLs
    path("", PostListView.as_view(), name="post-list"),  # Home page - list all posts
    path("posts/", PostListView.as_view(), name="post-list-alt"),  # Alternative URL
    path("posts/new/", PostCreateView.as_view(), name="post-create"),  # Create new post
    path("posts/<int:pk>/", PostDetailView.as_view(), name="post-detail"),  # View post
    path(
        "posts/<int:pk>/edit/", PostUpdateView.as_view(), name="post-update"
    ),  # Edit post
    path(
        "posts/<int:pk>/delete/", PostDeleteView.as_view(), name="post-delete"
    ),  # Delete post
]
