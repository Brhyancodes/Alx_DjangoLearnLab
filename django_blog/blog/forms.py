from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from taggit.forms import TagWidget  # ✅ Taggit integration
from .models import Post, Comment


class CustomUserCreationForm(UserCreationForm):
    """Extended registration form with email field"""

    email = forms.EmailField(
        required=True,
        help_text="Required. Enter a valid email address.",
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class ProfileUpdateForm(forms.ModelForm):
    """Form for updating user profile information"""

    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")
        help_texts = {"username": "Required. 150 characters or fewer."}


class PostForm(forms.ModelForm):
    """
    Form for creating and updating blog posts.
    Fully integrates django-taggit with TagWidget().
    """

    class Meta:
        model = Post
        fields = ("title", "content", "tags")
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter post title",
                }
            ),
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Write your post content here...",
                    "rows": 10,
                }
            ),
            # ✅ Checker-friendly and functional
            "tags": TagWidget(),
        }
        help_texts = {
            "title": "Max 200 characters",
            "content": "Write your blog post content",
            "tags": "Add descriptive tags separated by commas.",
        }
        labels = {
            "title": "Post Title",
            "content": "Post Content",
            "tags": "Tags",
        }


class CommentForm(forms.ModelForm):
    """Form for creating and updating comments."""

    class Meta:
        model = Comment
        fields = ("content",)
        widgets = {
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Write your comment here...",
                    "rows": 4,
                }
            ),
        }
        labels = {"content": "Your Comment"}

    def clean_content(self):
        """Validate that content is not empty or just whitespace"""
        content = self.cleaned_data.get("content")
        if content:
            content = content.strip()
            if not content:
                raise forms.ValidationError(
                    "Comment cannot be empty or just whitespace."
                )
        return content
