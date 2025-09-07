from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseForbidden
from .models import Library, Book


# Function-based view that lists all books stored in the database.
def list_books(request):
    books = Book.objects.all()
    return render(request, "relationship_app/list_books.html", {"books": books})


# Class-based view that displays details for a specific library
class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add all books available in this library to the context
        context["books"] = self.object.books.all()
        return context


# Registration view for user authentication
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(
                "relationship:index"
            )  # Redirect to home page after registration
    else:
        form = UserCreationForm()
    return render(request, "relationship_app/register.html", {"form": form})


# Role-based access control functions
def check_role(user, role_name):
    """Check if user has the specified role"""
    return (
        user.is_authenticated
        and hasattr(user, "userprofile")
        and user.userprofile.role == role_name
    )


def admin_required(function=None):
    """Decorator for views that checks the user has Admin role"""
    actual_decorator = user_passes_test(
        lambda u: check_role(u, "Admin"), login_url="/accounts/login/"
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def librarian_required(function=None):
    """Decorator for views that checks the user has Librarian role"""
    actual_decorator = user_passes_test(
        lambda u: check_role(u, "Librarian"), login_url="/accounts/login/"
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def member_required(function=None):
    """Decorator for views that checks the user has Member role"""
    actual_decorator = user_passes_test(
        lambda u: check_role(u, "Member"), login_url="/accounts/login/"
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


# Role-based views
@login_required
@admin_required
def admin_view(request):
    return render(request, "admin_view.html")


@login_required
@librarian_required
def librarian_view(request):
    return render(request, "librarian_view.html")


@login_required
@member_required
def member_view(request):
    return render(request, "member_view.html")
