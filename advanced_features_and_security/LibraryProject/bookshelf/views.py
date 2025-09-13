# bookshelf/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required, login_required
from django.views.decorators.http import require_POST
from .models import Book
from .forms import BookForm, ExampleForm  # ✅ added ExampleForm

# ============================
# BOOK CRUD VIEWS (with permissions)
# ============================


# list view (requires can_view)
@permission_required("bookshelf.can_view", raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, "bookshelf/book_list.html", {"books": books})


# create view
@permission_required("bookshelf.can_create", raise_exception=True)
def book_add(request):
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES or None)
        if form.is_valid():
            form.save()
            return redirect("bookshelf:book_list")
    else:
        form = BookForm()
    return render(
        request, "bookshelf/form_example.html", {"form": form, "title": "Add book"}
    )


# edit view
@permission_required("bookshelf.can_edit", raise_exception=True)
def book_edit(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES or None, instance=book)
        if form.is_valid():
            form.save()
            return redirect("bookshelf:book_list")
    else:
        form = BookForm(instance=book)
    return render(
        request, "bookshelf/form_example.html", {"form": form, "title": "Edit book"}
    )


# delete view — POST only
@permission_required("bookshelf.can_delete", raise_exception=True)
@require_POST
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book.delete()
    return redirect("bookshelf:book_list")


# ============================
# SAFE SEARCH VIEW
# ============================
def book_search(request):
    q = request.GET.get("q", "").strip()
    results = Book.objects.none()
    if q:
        results = Book.objects.filter(title__icontains=q)
    return render(request, "bookshelf/book_list.html", {"books": results})


# ============================
# EXAMPLE FORM DEMO VIEW
# ============================
def example_form_view(request):
    """
    Demo page for ExampleForm (CSRF, validation, and safe input handling).
    """
    if request.method == "POST":
        form = ExampleForm(request.POST)
        if form.is_valid():
            # normally you’d process data here
            cleaned = form.cleaned_data
            return render(
                request,
                "bookshelf/form_example.html",
                {"form": form, "title": "Form Submitted!", "cleaned": cleaned},
            )
    else:
        form = ExampleForm()

    return render(
        request,
        "bookshelf/form_example.html",
        {"form": form, "title": "Example Form"},
    )
