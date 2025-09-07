from django.urls import path
from . import views
from .views import list_books, LibraryDetailView
from .views import (
    RelationshipListView,
    RelationshipDetailView,
    RelationshipCreateView,
    RelationshipUpdateView,
    RelationshipDeleteView,
    BookCreateView,
    BookUpdateView,
    BookDeleteView,
)
from django.contrib.auth import views as auth_views

app_name = "relationship"

urlpatterns = [
    # Function-based views
    path("", views.index, name="index"),  # Home page
    path("books/", list_books, name="list_books"),  # Books list view
    path(
        "list-fbv/", views.relationship_list, name="relationship_list_fbv"
    ),  # List view (function-based)
    path(
        "create-fbv/", views.relationship_create, name="relationship_create_fbv"
    ),  # Create view (function-based)
    path(
        "detail-fbv/<int:pk>/",
        views.relationship_detail,
        name="relationship_detail_fbv",
    ),  # Detail view (function-based)
    path(
        "update-fbv/<int:pk>/",
        views.relationship_update,
        name="relationship_update_fbv",
    ),  # Update view (function-based)
    path(
        "delete-fbv/<int:pk>/",
        views.relationship_delete,
        name="relationship_delete_fbv",
    ),  # Delete view (function-based)
    # SECURED BOOK MANAGEMENT URLs - Function-based views
    path(
        "books/add/", views.add_book, name="add_book"
    ),  # Add book (requires can_add_book permission)
    path(
        "books/edit/<int:pk>/", views.edit_book, name="edit_book"
    ),  # Edit book (requires can_change_book permission)
    path(
        "books/delete/<int:pk>/", views.delete_book, name="delete_book"
    ),  # Delete book (requires can_delete_book permission)
    # SECURED BOOK MANAGEMENT URLs - Class-based views (alternative)
    path(
        "books/create/", BookCreateView.as_view(), name="book_create"
    ),  # Create book (CBV with permission)
    path(
        "books/update/<int:pk>/", BookUpdateView.as_view(), name="book_update"
    ),  # Update book (CBV with permission)
    path(
        "books/remove/<int:pk>/", BookDeleteView.as_view(), name="book_delete_cbv"
    ),  # Delete book (CBV with permission)
    # Authentication URLs
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="relationship_app/login.html"),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="relationship_app/logout.html"),
        name="logout",
    ),
    path(
        "register/",
        views.register,
        name="register",
    ),
    # Class-based views
    path(
        "library/<int:pk>/", LibraryDetailView.as_view(), name="library_detail"
    ),  # Library detail view
    path(
        "list/", RelationshipListView.as_view(), name="relationship_list"
    ),  # List view (class-based)
    path(
        "create/", RelationshipCreateView.as_view(), name="relationship_create"
    ),  # Create view (class-based)
    path(
        "detail/<int:pk>/", RelationshipDetailView.as_view(), name="relationship_detail"
    ),  # Detail view (class-based)
    path(
        "update/<int:pk>/", RelationshipUpdateView.as_view(), name="relationship_update"
    ),  # Update view (class-based)
    path(
        "delete/<int:pk>/", RelationshipDeleteView.as_view(), name="relationship_delete"
    ),  # Delete view (class-based)
    # role-based URLs
    path("admin/dashboard/", views.admin_view, name="admin_dashboard"),
    path("librarian/dashboard/", views.librarian_view, name="librarian_dashboard"),
    path("member/dashboard/", views.member_view, name="member_dashboard"),
]
