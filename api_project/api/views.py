from django.shortcuts import render

# Create your views here.
#  create a view named BookList that extends rest_framework.generics.ListAPIView.
from rest_framework import generics
from .models import Book
from .serializers import BookSerializer


class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # a new class BookViewSet that handles all CRUD operations.


from rest_framework import viewsets


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
