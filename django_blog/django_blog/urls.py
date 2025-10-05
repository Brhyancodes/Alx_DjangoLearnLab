from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import (
    RegisterView,
    profile_view,
    add_comment,
    edit_comment,
    delete_comment,
    search_posts,
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
)

urlpatterns = [
    path("login/", auth_views.LoginView.as_view(template_name="blog/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("profile/", profile_view, name="profile"),
    path("profile/edit/", views.profile_edit, name="profile_edit"),

    # Post CRUD
    path("", PostListView.as_view(), name="post-list"),
    path("post/new/", PostCreateView.as_view(), name="post-create"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("post/<int:pk>/update/", PostUpdateView.as_view(), name="post-edit"),
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name="post-delete"),

    # Comments
    path("post/<int:post_id>/comment/", add_comment, name="add-comment"),
    path("comment/<int:comment_id>/edit/", edit_comment, name="edit-comment"),
    path("comment/<int:comment_id>/delete/", delete_comment, name="delete-comment"),
    path("post/<int:pk>/comments/new/", views.CommentCreateView.as_view(), name="comment_create"),
    path("comment/<int:pk>/update/", views.CommentUpdateView.as_view(), name="comment_update"),
    path("comment/<int:pk>/delete/", views.CommentDeleteView.as_view(), name="comment_delete"),

    # Search
    path("search/", search_posts, name="search-posts"),

    # Disturbing code
    path("tags/<slug:tag_slug>/", views.PostByTagListView.as_view(), name="posts-by-tag"),
]
