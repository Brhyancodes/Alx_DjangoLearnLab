from django.db import models

# Create your models here.


# Author model - represents authors who can write multiple books
class Author(models.Model):
    """
    Author model to store information about book authors.

    Fields:
    - name: The author's full name

    Relationships:
    - One-to-many with Book model (one author can have many books)
    """

    name = models.CharField(max_length=100, help_text="Author's full name")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


# Book model with foreign key relationship to Author
class Book(models.Model):
    """
    Book model to store information about individual books.

    Fields:
    - title: The book's title
    - publication_year: The year the book was published
    - author: Foreign key linking to the Author model

    Relationships:
    - Many-to-one with Author model (many books can belong to one author)
    The related_name='books' allows reverse lookup from Author to Books
    """

    title = models.CharField(max_length=200, help_text="Book's title")
    publication_year = models.IntegerField(help_text="Year the book was published")
    author = models.ForeignKey(
        Author,
        related_name="books",
        on_delete=models.CASCADE,
        help_text="Author who wrote this book",
    )

    def __str__(self):
        return f"{self.title} ({self.publication_year})"

    class Meta:
        ordering = ["-publication_year", "title"]
        # Ensure no duplicate books by same author with same title and year
        unique_together = ["title", "author", "publication_year"]
