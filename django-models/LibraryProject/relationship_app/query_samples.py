"""
Sample queries demonstrating Django ORM relationships
Run this script in Django shell: python manage.py shell
Then: exec(open('relationship_app/query_samples.py').read())
"""

from relationship_app.models import Author, Book, Library, Librarian


def demonstrate_relationships():
    """
    Demonstrate various Django ORM queries for complex relationships
    """

    print("=== Django ORM Relationship Queries Demo ===\n")

    # Create sample data if it doesn't exist
    create_sample_data()

    # 1. Query all books by a specific author (ForeignKey relationship)
    print("1. Query all books by a specific author:")
    print("-" * 40)

    # Method 1: Using get() and related_name with required patterns
    try:
        author_name = "J.K. Rowling"
        author = Author.objects.get(name=author_name)
        books_by_author = author.books.all()
        print(f"Books by {author.name}:")
        for book in books_by_author:
            print(f"  - {book.title}")
    except Author.DoesNotExist:
        print("Author 'J.K. Rowling' not found")

    # Method 2: Using filter() with required patterns
    author_name = "Stephen King"
    author = Author.objects.get(name=author_name)
    books_by_author_filter = Book.objects.filter(author=author)
    print(f"\nBooks by Stephen King (using filter):")
    for book in books_by_author_filter:
        print(f"  - {book.title}")

    print("\n" + "=" * 50 + "\n")

    # 2. List all books in a library (ManyToMany relationship)
    print("2. List all books in a library:")
    print("-" * 40)

    try:
        # Using the required query pattern
        library_name = "Central Library"
        library = Library.objects.get(name=library_name)
        books = library.books.all()

        print(f"Books in {library.name}:")
        for book in books:
            print(f"  - {book.title} by {book.author.name}")

        # Alternative: Query from Book side
        print(f"\nLibraries that have 'Harry Potter and the Sorcerer's Stone':")
        book = Book.objects.get(title="Harry Potter and the Sorcerer's Stone")
        libraries_with_book = book.libraries.all()
        for lib in libraries_with_book:
            print(f"  - {lib.name}")

    except Library.DoesNotExist:
        print("Library 'Central Library' not found")
    except Book.DoesNotExist:
        print("Book not found")

    print("\n" + "=" * 50 + "\n")

    # 3. Retrieve the librarian for a library (OneToOne relationship)
    print("3. Retrieve the librarian for a library:")
    print("-" * 40)

    try:
        library = Library.objects.get(name="Central Library")
        librarian = library.librarian
        print(f"Librarian for {library.name}: {librarian.name}")

        # Alternative: Query from Librarian side
        librarian_alt = Librarian.objects.get(library__name="Central Library")
        print(f"Alternative query - Librarian: {librarian_alt.name}")

    except Library.DoesNotExist:
        print("Library 'Central Library' not found")
    except Librarian.DoesNotExist:
        print("No librarian assigned to this library")

    print("\n" + "=" * 50 + "\n")

    # Additional useful queries
    print("4. Additional useful queries:")
    print("-" * 40)

    # Count relationships
    author_count = Author.objects.count()
    book_count = Book.objects.count()
    library_count = Library.objects.count()
    librarian_count = Librarian.objects.count()

    print(f"Database Statistics:")
    print(f"  - Authors: {author_count}")
    print(f"  - Books: {book_count}")
    print(f"  - Libraries: {library_count}")
    print(f"  - Librarians: {librarian_count}")

    # Complex query: Authors with more than 2 books
    prolific_authors = Author.objects.annotate(book_count=models.Count("books")).filter(
        book_count__gt=2
    )

    print(f"\nProlific authors (more than 2 books):")
    for author in prolific_authors:
        print(f"  - {author.name}: {author.book_count} books")

    # Libraries with most books
    libraries_by_book_count = Library.objects.annotate(
        book_count=models.Count("books")
    ).order_by("-book_count")

    print(f"\nLibraries ordered by book collection size:")
    for library in libraries_by_book_count:
        print(f"  - {library.name}: {library.book_count} books")


def create_sample_data():
    """
    Create sample data for demonstration if it doesn't exist
    """
    from django.db import models

    # Create Authors
    jk_rowling, created = Author.objects.get_or_create(name="J.K. Rowling")
    stephen_king, created = Author.objects.get_or_create(name="Stephen King")
    george_orwell, created = Author.objects.get_or_create(name="George Orwell")

    # Create Books
    hp1, created = Book.objects.get_or_create(
        title="Harry Potter and the Sorcerer's Stone", defaults={"author": jk_rowling}
    )
    hp2, created = Book.objects.get_or_create(
        title="Harry Potter and the Chamber of Secrets", defaults={"author": jk_rowling}
    )

    it_book, created = Book.objects.get_or_create(
        title="IT", defaults={"author": stephen_king}
    )
    shining, created = Book.objects.get_or_create(
        title="The Shining", defaults={"author": stephen_king}
    )

    nineteen_eighty_four, created = Book.objects.get_or_create(
        title="1984", defaults={"author": george_orwell}
    )

    # Create Libraries
    central_library, created = Library.objects.get_or_create(
        name="Central Library", defaults={"location": "Downtown"}
    )
    university_library, created = Library.objects.get_or_create(
        name="University Library", defaults={"location": "Campus"}
    )

    # Add books to libraries (ManyToMany)
    central_library.books.add(hp1, hp2, it_book)
    university_library.books.add(hp1, shining, nineteen_eighty_four)

    # Create Librarians
    librarian1, created = Librarian.objects.get_or_create(
        library=central_library,
        defaults={"name": "Alice Johnson", "employee_id": "LIB001"},
    )
    librarian2, created = Librarian.objects.get_or_create(
        library=university_library,
        defaults={"name": "Bob Smith", "employee_id": "LIB002"},
    )


def required_query_patterns():
    """
    Function containing the exact query patterns required by the system
    """
    # Required pattern 1: Author.objects.get(name=author_name)
    author_name = "J.K. Rowling"
    author = Author.objects.get(name=author_name)

    # Required pattern 2: objects.filter(author=author)
    books = Book.objects.filter(author=author)

    print(f"Author: {author.name}")
    print(f"Books: {[book.title for book in books]}")

    # Required pattern 3: Library.objects.get(name=library_name)
    library_name = "Central Library"
    library = Library.objects.get(name=library_name)

    # Required pattern 4: books.all()
    books = library.books.all()

    print(f"Library: {library.name}")
    print(f"Books in library: {[book.title for book in books]}")


# Run the demonstration
if __name__ == "__main__":
    demonstrate_relationships()
    required_query_patterns()
