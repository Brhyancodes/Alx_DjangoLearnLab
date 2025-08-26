# Django Admin Interface Configuration

## Steps Completed:

1. **Created Superuser Account**
   - Command: `python manage.py createsuperuser`
   - Created admin account with username/password

2. **Configured bookshelf/admin.py**
   - Registered Book model with admin interface
   - Customized list display: title, author, publication_year
   - Added list filters: author, publication_year
   - Enabled search: title, author fields
   - Set default ordering: by title

3. **Admin Interface Features:**
   - List view shows all book attributes
   - Filter books by author or publication year
   - Search functionality for titles and authors
   - Add/edit/delete books through web interface

## admin.py Code:
```python
from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')
    list_filter = ('author', 'publication_year')
    search_fields = ('title', 'author')
    ordering = ('title',)