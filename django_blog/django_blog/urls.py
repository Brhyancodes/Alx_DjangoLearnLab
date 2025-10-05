from django.urls import path
from . import views

urlpatterns = [
    # ===== Authentication & Profile =====
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile_view, name="profile"),
    # ===== Posts =====
    path("", views.PostListView.as_view(), name="post-list"),
    path("post/<int:pk>/", views.PostDetailView.as_view(), name="post-detail"),
    path("post/new/", views.PostCreateView.as_view(), name="post-create"),
    path("post/<int:pk>/edit/", views.PostUpdateView.as_view(), name="post-update"),
    path("post/<int:pk>/delete/", views.PostDeleteView.as_view(), name="post-delete"),
    # ===== Comments =====
    path(
        "post/<int:post_id>/comment/new/",
        views.CommentCreateView.as_view(),
        name="add-comment",
    ),
    path(
        "comment/<int:pk>/edit/",
        views.CommentUpdateView.as_view(),
        name="edit-comment",
    ),
    path(
        "comment/<int:pk>/delete/",
        views.CommentDeleteView.as_view(),
        name="delete-comment",
    ),
    # ===== Search =====
    path("search/", views.SearchResultsView.as_view(), name="search-results"),
    path(
        "tags/<slug:tag_slug>/", views.PostByTagListView.as_view(), name="posts-by-tag"
    ),
]
