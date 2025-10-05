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
    CommentCreateView,
    CommentUpdateView,
    CommentDeleteView,
)

urlpatterns = [
    # Authentication URLs
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", MyLoginView.as_view(), name="login"),
    path("logout/", MyLogoutView.as_view(), name="logout"),
    path("profile/", profile, name="profile"),
    # Blog Post URLs
    path("", PostListView.as_view(), name="post-list"),
    path("post/new/", PostCreateView.as_view(), name="post-create"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("post/<int:pk>/update/", PostUpdateView.as_view(), name="post-update"),
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name="post-delete"),
    # Comment URLs (added for CRUD)
    path(
        "post/<int:pk>/comments/new/",
        CommentCreateView.as_view(),
        name="comment-create",
    ),
    path(
        "comment/<int:pk>/update/",
        CommentUpdateView.as_view(),
        name="comment-update",
    ),
    path(
        "comment/<int:pk>/delete/",
        CommentDeleteView.as_view(),
        name="comment-delete",
    ),
]
