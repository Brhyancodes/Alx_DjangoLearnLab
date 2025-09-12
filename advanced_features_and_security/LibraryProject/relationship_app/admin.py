from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Author, Book, Library, Librarian, UserProfile


# Custom User Admin
class CustomUserAdmin(UserAdmin):
    # Define the fields to be used in displaying the User model in admin
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "date_of_birth",
        "is_staff",
        "is_active",
    )
    list_filter = ("is_staff", "is_superuser", "is_active", "date_joined")
    search_fields = ("username", "email", "first_name", "last_name")
    ordering = ("username",)

    # Define fieldsets for the user change form
    fieldsets = UserAdmin.fieldsets + (
        ("Additional Information", {"fields": ("date_of_birth", "profile_photo")}),
    )

    # Define fieldsets for the user creation form
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional Information", {"fields": ("date_of_birth", "profile_photo")}),
    )

    # Make profile photo display nicely in admin
    readonly_fields = ("date_joined", "last_login")


# Register the CustomUser model with the custom admin
admin.site.register(CustomUser, CustomUserAdmin)


# Admin configurations for other models
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author")
    list_filter = ("author",)
    search_fields = ("title", "author__name")


@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    filter_horizontal = ("books",)  # Makes ManyToMany field easier to manage
    search_fields = ("name",)


@admin.register(Librarian)
class LibrarianAdmin(admin.ModelAdmin):
    list_display = ("name", "library")
    list_filter = ("library",)
    search_fields = ("name", "library__name")


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role")
    list_filter = ("role",)
    search_fields = ("user__username", "user__email")

    # Display user info in a more readable format
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related("user")  # Optimize database queries
