from django.contrib import admin
from .models import Author, Book


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """
    Admin configuration for Author model.
    Displays author name and book count in the admin list view.
    """

    list_display = ["name", "book_count"]
    search_fields = ["name"]
    ordering = ["name"]

    def book_count(self, obj):
        """Display the number of books by this author."""
        return obj.books.count()

    book_count.short_description = "Number of Books"


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    Admin configuration for Book model.
    Provides filtering, searching, and organized display of book information.
    """

    list_display = ["title", "author", "publication_year"]
    list_filter = ["author", "publication_year"]
    search_fields = ["title", "author__name"]
    ordering = ["-publication_year", "title"]

    # Group fields in the edit form
    fieldsets = (
        ("Book Information", {"fields": ("title", "publication_year")}),
        ("Author", {"fields": ("author",)}),
    )
