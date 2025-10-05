from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy
from .models import Post, Comment
from .forms import CustomUserCreationForm, ProfileUpdateForm, PostForm, CommentForm


# ==================== AUTHENTICATION VIEWS ====================


def register_view(request):
    """Handle user registration"""
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request, f"Account created successfully! Welcome, {user.username}!"
            )
            return redirect("profile")
    else:
        form = CustomUserCreationForm()
    return render(request, "blog/register.html", {"form": form})


def login_view(request):
    """Handle user login"""
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect("profile")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, "blog/login.html", {"form": form})


def logout_view(request):
    """Handle user logout"""
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect("login")


@login_required
def profile_view(request):
    """Display and update user profile"""
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect("profile")
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, "blog/profile.html", {"form": form})


# ==================== BLOG POST CRUD VIEWS ====================


class PostListView(ListView):
    """
    Display all blog posts - accessible to everyone.
    Uses pagination to show 10 posts per page.
    """

    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        """Return all posts ordered by published date (newest first)"""
        return Post.objects.all().order_by("-published_date")


class PostDetailView(DetailView):
    """
    Display individual blog post - accessible to everyone.
    Shows full post content and author information.
    """

    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"


class PostCreateView(LoginRequiredMixin, CreateView):
    """
    Allow authenticated users to create new posts.
    Automatically sets the author to the current logged-in user.
    """

    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"
    success_url = reverse_lazy("post-list")

    def form_valid(self, form):
        """Set the author to the current logged-in user"""
        form.instance.author = self.request.user
        messages.success(self.request, "Your post has been created successfully!")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """Add context for template"""
        context = super().get_context_data(**kwargs)
        context["title"] = "Create New Post"
        context["button_text"] = "Create Post"
        return context


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Allow post authors to edit their posts.
    Only the author of the post can access this view.
    """

    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def form_valid(self, form):
        """Keep the original author when updating"""
        form.instance.author = self.request.user
        messages.success(self.request, "Your post has been updated successfully!")
        return super().form_valid(form)

    def test_func(self):
        """Check if the current user is the author of the post"""
        post = self.get_object()
        return self.request.user == post.author

    def get_context_data(self, **kwargs):
        """Add context for template"""
        context = super().get_context_data(**kwargs)
        context["title"] = "Edit Post"
        context["button_text"] = "Update Post"
        return context

    def get_success_url(self):
        """Redirect to the post detail page after update"""
        return reverse_lazy("post-detail", kwargs={"pk": self.object.pk})


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Allow post authors to delete their posts.
    Only the author of the post can access this view.
    Shows a confirmation page before deletion.
    """

    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("post-list")
    context_object_name = "post"

    def test_func(self):
        """Check if the current user is the author of the post"""
        post = self.get_object()
        return self.request.user == post.author

    def delete(self, request, *args, **kwargs):
        """Add success message when post is deleted"""
        messages.success(self.request, "Your post has been deleted successfully!")
        return super().delete(request, *args, **kwargs)


# ==================== COMMENT VIEWS ====================


@login_required
def add_comment(request, post_id):
    """Allow authenticated users to add comments to a post"""
    post = get_object_or_404(Post, pk=post_id)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, "Your comment has been added successfully!")
            return redirect("post-detail", pk=post_id)
    else:
        form = CommentForm()

    return render(request, "blog/add_comment.html", {"form": form, "post": post})


@login_required
def edit_comment(request, comment_id):
    """Allow comment authors to edit their comments"""
    comment = get_object_or_404(Comment, pk=comment_id)

    # Check if user is the comment author
    if request.user != comment.author:
        messages.error(request, "You can only edit your own comments!")
        return redirect("post-detail", pk=comment.post.pk)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, "Your comment has been updated successfully!")
            return redirect("post-detail", pk=comment.post.pk)
    else:
        form = CommentForm(instance=comment)

    return render(request, "blog/edit_comment.html", {"form": form, "comment": comment})


@login_required
def delete_comment(request, comment_id):
    """Allow comment authors to delete their comments"""
    comment = get_object_or_404(Comment, pk=comment_id)
    post_id = comment.post.pk

    # Check if user is the comment author
    if request.user != comment.author:
        messages.error(request, "You can only delete your own comments!")
        return redirect("post-detail", pk=post_id)

    if request.method == "POST":
        comment.delete()
        messages.success(request, "Your comment has been deleted successfully!")
        return redirect("post-detail", pk=post_id)

    return render(request, "blog/delete_comment.html", {"comment": comment})
