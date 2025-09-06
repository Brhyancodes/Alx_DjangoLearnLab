from django.contrib import admin
from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # Display these fields in the list view
    list_display = ("title", "author", "publication_year")

    # Add filters for author and publication year
    list_filter = ("author", "publication_year")

    # Enable search functionality for title and author
    search_fields = ("title", "author")

    # Optional: Add ordering by title by default
    ordering = ("title",)
