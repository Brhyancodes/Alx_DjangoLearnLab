from django.urls import path
from django.contrib.auth import views as auth_views
from .views import RegisterView, profile_view
from templates.blog import profile_edit
from . import views
from .views import add_comment, edit_comment, delete_comment, search_posts
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
)

urlpatterns = [
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="blog/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("profile/", profile_view, name="profile"),
    path("profile/edit/", profile_edit, name="profile_edit"),
    # List of posts (Read)
    path("", PostListView.as_view(), name="post-list"),
    # View a specific post (Read)
    path("post/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    # Create a new post (Create)
    path("post/new/", PostCreateView.as_view(), name="post-create"),
    # Update a specific post (Update)
    path("post/<int:pk>/update/", PostUpdateView.as_view(), name="post-edit"),
    # Delete a specific post (Delete)
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name="post-delete"),
    path("post/<int:post_id>/comment/", add_comment, name="add-comment"),
    path("comment/<int:comment_id>/edit/", edit_comment, name="edit-comment"),
    path("comment/<int:comment_id>/delete/", delete_comment, name="delete-comment"),
    path("search/", search_posts, name="search-posts"),
    path("tags/<str:tag_name>/", PostListView.as_view(), name="posts-by-tag"),
    path(
        "tags/<slug:tag_slug>/", views.PostByTagListView.as_view(), name="posts_by_tag"
    ),
    path(
        "post/<int:pk>/comments/new/",
        views.CommentCreateView.as_view(),
        name="comment_create",
    ),
    path(
        "comment/<int:pk>/update/",
        views.CommentUpdateView.as_view(),
        name="comment_update",
    ),
    path(
        "comment/<int:pk>/delete/",
        views.CommentDeleteView.as_view(),
        name="comment_delete",
    ),
]
