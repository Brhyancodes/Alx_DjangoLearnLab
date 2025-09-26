from django.urls import path
from .views import (
    BookListView,
    BookDetailView,
    BookCreateView,
    BookUpdateView,
    BookDeleteView,
)

urlpatterns = [
    path("books/", BookListView.as_view(), name="book-list"),  # GET all
    path("books/<int:pk>/", BookDetailView.as_view(), name="book-detail"),  # GET one
    path(
        "books/create/", BookCreateView.as_view(), name="book-create"
    ),  # POST (create)
    path(
        "books/<int:pk>/update/", BookUpdateView.as_view(), name="book-update"
    ),  # PUT/PATCH
    path(
        "books/<int:pk>/delete/", BookDeleteView.as_view(), name="book-delete"
    ),  # DELETE
]
