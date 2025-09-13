from django.urls import path
from . import views

app_name = "bookshelf"

urlpatterns = [
    path("books/", views.book_list, name="book_list"),
    path("books/add/", views.book_add, name="book_add"),
    path("books/<int:pk>/edit/", views.book_edit, name="book_edit"),
    path("books/<int:pk>/delete/", views.book_delete, name="book_delete"),
    path("books/search/", views.book_search, name="book_search"),
]
