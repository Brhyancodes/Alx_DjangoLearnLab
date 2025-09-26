from rest_framework import generics
from django_filters import rest_framework
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Book
from .serializers import BookSerializer


class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # Enable filtering, searching, ordering
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    # Filter by exact matches
    filterset_fields = ["title", "author", "publication_year"]

    # Search in these fields (case-insensitive)
    search_fields = ["title", "author"]

    # Allow ordering
    ordering_fields = ["title", "publication_year"]
    ordering = ["title"]  # default ordering
