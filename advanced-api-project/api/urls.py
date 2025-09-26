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
    path("books/", BookCreateView.as_view(), name="book-create"),  # POST (create)
    path(
        "books/<int:pk>/", BookUpdateView.as_view(), name="book-update"
    ),  # PUT/PATCH (update)
    path("books/<int:pk>/", BookDeleteView.as_view(), name="book-delete"),  # DELETE
]
