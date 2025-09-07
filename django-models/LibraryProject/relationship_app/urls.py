from django.urls import path
from . import views
from .views import list_books, LibraryDetailView
from .views import (
    RelationshipListView,
    RelationshipDetailView,
    RelationshipCreateView,
    RelationshipUpdateView,
    RelationshipDeleteView,
)

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
]
