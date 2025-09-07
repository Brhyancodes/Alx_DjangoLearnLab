from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseForbidden
from .models import Library, Book
from .models import Relationship  # Make sure this import exists
from django.views.generic import ListView, CreateView, UpdateView, DeleteView


# Function-based view that lists all books stored in the database.
def list_books(request):
    books = Book.objects.all()
    return render(request, "relationship_app/list_books.html", {"books": books})


# Home page view (needed for your URLs)
def index(request):
    return render(request, "relationship_app/index.html")


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


# Add function-based views for relationships (referenced in your URLs)
def relationship_list(request):
    relationships = Relationship.objects.all()
    return render(
        request,
        "relationship_app/relationship_list.html",
        {"relationships": relationships},
    )


def relationship_detail(request, pk):
    relationship = Relationship.objects.get(pk=pk)
    return render(
        request,
        "relationship_app/relationship_detail.html",
        {"relationship": relationship},
    )


def relationship_create(request):
    # Add your implementation for relationship creation
    pass


def relationship_update(request, pk):
    # Add your implementation for relationship update
    pass


def relationship_delete(request, pk):
    # Add your implementation for relationship deletion
    pass


# Add class-based views for relationships (referenced in your URLs)
class RelationshipListView(ListView):
    model = Relationship
    template_name = "relationship_app/relationship_list.html"
    context_object_name = "relationships"


class RelationshipDetailView(DetailView):
    model = Relationship
    template_name = "relationship_app/relationship_detail.html"
    context_object_name = "relationship"


class RelationshipCreateView(CreateView):
    model = Relationship
    template_name = "relationship_app/relationship_form.html"
    # Add your form fields here


class RelationshipUpdateView(UpdateView):
    model = Relationship
    template_name = "relationship_app/relationship_form.html"
    # Add your form fields here


class RelationshipDeleteView(DeleteView):
    model = Relationship
    template_name = "relationship_app/relationship_confirm_delete.html"
    success_url = "/"  # Update with your success URL


# Role-based access control function
def check_role(user, role_name):
    """Check if user has the specified role"""
    return (
        user.is_authenticated
        and hasattr(user, "userprofile")
        and user.userprofile.role == role_name
    )


# Role-based views with explicit user_passes_test usage
@login_required
@user_passes_test(lambda u: check_role(u, "Admin"))
def admin_view(request):
    return render(request, "relationship_app/admin_view.html")


@login_required
@user_passes_test(lambda u: check_role(u, "Librarian"))
def librarian_view(request):
    return render(request, "relationship_app/librarian_view.html")


@login_required
@user_passes_test(lambda u: check_role(u, "Member"))
def member_view(request):
    return render(request, "relationship_app/member_view.html")
