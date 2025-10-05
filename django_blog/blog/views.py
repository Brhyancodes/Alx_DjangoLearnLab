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


# ==================== COMMENT CRUD VIEWS (class-based) ====================


class CommentCreateView(LoginRequiredMixin, CreateView):
    """
    Allow authenticated users to add comments to a post.
    Expects `post_id` in the URL kwargs.
    """

    model = Comment
    form_class = CommentForm
    template_name = "blog/add_comment.html"

    def form_valid(self, form):
        # Attach the author and related post before saving
        form.instance.author = self.request.user
        post = get_object_or_404(Post, pk=self.kwargs.get("post_id"))
        form.instance.post = post
        messages.success(self.request, "Your comment has been added successfully!")
        return super().form_valid(form)

    def get_success_url(self):
        # After saving, redirect to the post detail page
        return reverse_lazy("post-detail", kwargs={"pk": self.object.post.pk})


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Allow comment authors to edit their comments.
    Only the comment author may update.
    """

    model = Comment
    form_class = CommentForm
    template_name = "blog/edit_comment.html"

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def form_valid(self, form):
        messages.success(self.request, "Your comment has been updated successfully!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("post-detail", kwargs={"pk": self.object.post.pk})


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Allow comment authors to delete their comments.
    Only the comment author may delete.
    Shows a confirmation page before deletion.
    """

    model = Comment
    template_name = "blog/delete_comment.html"
    context_object_name = "comment"

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def delete(self, request, *args, **kwargs):
        # Save post pk before deletion so we can redirect after removing the comment
        self.object = self.get_object()
        post_pk = self.object.post.pk
        self.object.delete()
        messages.success(self.request, "Your comment has been deleted successfully!")
        return redirect("post-detail", pk=post_pk)
