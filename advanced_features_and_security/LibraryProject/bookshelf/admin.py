from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Book, CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # Add custom fields to list display
    list_display = ("username", "email", "date_of_birth", "is_staff", "is_superuser")
    # Add filters
    list_filter = ("is_staff", "is_superuser", "date_of_birth")
    # Add fields to search
    search_fields = ("username", "email")
    # Ordering by username
    ordering = ("username",)
    # Fieldsets for editing user info
    fieldsets = UserAdmin.fieldsets + (
        (None, {"fields": ("date_of_birth", "profile_photo")}),
    )
    # Fieldsets for creating new users
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {"fields": ("date_of_birth", "profile_photo")}),
    )


# Register models
admin.site.register(CustomUser, CustomUserAdmin)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "publication_year")
    list_filter = ("author", "publication_year")
    search_fields = ("title", "author")
    ordering = ("title",)
