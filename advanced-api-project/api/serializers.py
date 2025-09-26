from rest_framework import serializers
from datetime import datetime
from .models import Author, Book


class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.

    Handles serialization/deserialization of Book instances and includes
    custom validation to ensure publication_year is not in the future.

    Fields:
    - id: Auto-generated primary key
    - title: Book's title
    - publication_year: Year book was published (with custom validation)
    - author: Foreign key to Author (will show author ID by default)
    """

    class Meta:
        model = Book
        fields = ["id", "title", "publication_year", "author"]

    def validate_publication_year(self, value):
        """
        Custom validation to ensure publication_year is not in the future.

        Args:
            value: The publication_year value to validate

        Returns:
            int: The validated publication_year

        Raises:
            serializers.ValidationError: If publication_year is in the future
        """
        current_year = datetime.now().year

        if value > current_year:
            raise serializers.ValidationError(
                f"Publication year cannot be in the future. Current year is {current_year}."
            )

        # For fun Added minimum year validation
        if value < 1000:
            raise serializers.ValidationError(
                "Publication year must be a valid 4-digit year."
            )

        return value


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Author model with nested Book serialization.

    This serializer includes a nested BookSerializer to dynamically serialize
    all books related to an author, demonstrating one-to-many relationship handling.

    Fields:
    - id: Auto-generated primary key
    - name: Author's name
    - books: Nested serialization of all related Book instances
    """

    # Nested serializer for related books
    # 'many=True' because one author can have many books
    # 'read_only=True' because we don't want to create/update books through author endpoint
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ["id", "name", "books"]

    def to_representation(self, instance):
        """
        Override to provide additional context in the serialized output.
        This method is called when serializing data for output.
        """
        representation = super().to_representation(instance)

        # Add book count for convenience
        representation["book_count"] = instance.books.count()

        return representation


# Alternative: Simple AuthorSerializer without nested books (for basic operations)
class AuthorSimpleSerializer(serializers.ModelSerializer):
    """
    Simple Author serializer without nested books.
    Useful for cases where you don't need the full book details.
    """

    book_count = serializers.SerializerMethodField()

    class Meta:
        model = Author
        fields = ["id", "name", "book_count"]

    def get_book_count(self, obj):
        """Return the number of books by this author."""
        return obj.books.count()


# Alternative: Detailed BookSerializer with author name (instead of just ID)
class BookDetailSerializer(serializers.ModelSerializer):
    """
    Detailed Book serializer that includes author name instead of just ID.
    Useful for displaying book information with author details.
    """

    author_name = serializers.CharField(source="author.name", read_only=True)

    class Meta:
        model = Book
        fields = ["id", "title", "publication_year", "author", "author_name"]

    def validate_publication_year(self, value):
        """Same validation as BookSerializer."""
        current_year = datetime.now().year

        if value > current_year:
            raise serializers.ValidationError(
                f"Publication year cannot be in the future. Current year is {current_year}."
            )

        if value < 1000:
            raise serializers.ValidationError(
                "Publication year must be a valid 4-digit year."
            )

        return value
