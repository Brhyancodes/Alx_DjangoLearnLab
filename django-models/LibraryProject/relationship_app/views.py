from django.shortcuts import render
from django.views.generic import DetailView
from .models import Library, Book


# Function-based view that lists all books stored in the database.
def list_books(request):
    books = Book.objects.all()
    return render(request, "relationship_app/list_books.html", {"books": books})


# Class-based view that displays details for a specific library
class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add all books available in this library to the context
        context["books"] = self.object.books.all()
        return context
