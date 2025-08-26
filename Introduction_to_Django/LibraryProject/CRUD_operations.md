cat > CRUD_operations.md << 'EOF'
# CRUD Operations Documentation

## CREATE Operation

**Command Executed:**
```python
from bookshelf.models import Book
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
print(f"Created book: {book}")

# Retrieve

retrieved_book = Book.objects.get(title="1984")
print(f"Title: {retrieved_book.title}, Author: {retrieved_book.author}, Year: {retrieved_book.publication_year}")

# Update

book_to_update = Book.objects.get(title="1984")
book_to_update.title = "Nineteen Eighty-Four"
book_to_update.save()
updated_book = Book.objects.get(id=book_to_update.id)
print(f"Updated title: {updated_book.title}")

# Delete
book_to_delete = Book.objects.get(title="Nineteen Eighty-Four")
book_to_delete.delete()
print("Book deleted successfully")

# Verification
remaining_books = Book.objects.all()
print(f"Books remaining in database: {remaining_books.count()}")