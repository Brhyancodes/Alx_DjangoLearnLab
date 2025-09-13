# from django.shortcuts import render
# from django.contrib.auth.decorators import permission_required
# from .models import Book


# # View to list all books (only if user has 'can_view' permission)
# @permission_required("bookshelf.can_view", raise_exception=True)
# def book_list(request):
#     books = Book.objects.all()
#     return render(request, "bookshelf/book_list.html", {"books": books})

# bookshelf/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required, login_required
from django.views.decorators.http import require_POST
from .models import Book
from .forms import BookForm


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


# a safe search example (validate input via a small form or via GET param sanitize)
def book_search(request):
    q = request.GET.get("q", "").strip()
    # Avoid raw SQL — use ORM and parameterization
    results = Book.objects.none()
    if q:
        results = Book.objects.filter(title__icontains=q)
    return render(request, "bookshelf/book_list.html", {"books": results})
