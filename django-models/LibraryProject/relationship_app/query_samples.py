from django.db import models


class Author(models.Model):
    """
    Author model representing a book author.
    """

    name = models.CharField(max_length=100, help_text="Full name of the author")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Book(models.Model):
    """
    Book model representing a book with a foreign key relationship to Author.
    """

    title = models.CharField(max_length=200, help_text="Title of the book")
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name="books",
        help_text="Author of the book",
    )
    publication_date = models.DateField(null=True, blank=True)
    isbn = models.CharField(max_length=13, unique=True, null=True, blank=True)

    def __str__(self):
        return f"{self.title} by {self.author.name}"

    class Meta:
        ordering = ["title"]


class Library(models.Model):
    """
    Library model representing a library with many-to-many relationship to Books.
    """

    name = models.CharField(max_length=200, help_text="Name of the library")
    books = models.ManyToManyField(
        Book,
        related_name="libraries",
        blank=True,
        help_text="Books available in this library",
    )
    location = models.CharField(max_length=200, null=True, blank=True)
    established_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Libraries"


class Librarian(models.Model):
    """
    Librarian model representing a librarian with one-to-one relationship to Library.
    """

    name = models.CharField(max_length=100)
    library = models.OneToOneField(Library, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
