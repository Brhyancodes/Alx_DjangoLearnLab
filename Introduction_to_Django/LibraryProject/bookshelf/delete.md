
## 5. bookshelf/delete.md

```markdown
# Delete Operation

**Command:**
```python
from bookshelf.models import Book
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()

# Verify deletion
books = Book.objects.all()
print(f"Books remaining: {books.count()}")