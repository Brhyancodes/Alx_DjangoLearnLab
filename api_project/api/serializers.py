# Import serializers from Django REST framework
from rest_framework import serializers

# BookSerializer class that extends rest_framework.serializers.ModelSerializer and includes all fields of the Book model.
from .models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"
