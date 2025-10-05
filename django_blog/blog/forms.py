from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Comment, Tag  # <-- added Tag import


class CustomUserCreationForm(UserCreationForm):
    """Extended registration form with email field"""

    email = forms.EmailField(
        required=True, help_text="Required. Enter a valid email address."
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
        help_texts = {
            "username": "Required. 150 characters or fewer.",
        }


class PostForm(forms.ModelForm):
    """
    Form for creating and updating blog posts.
    Now includes a tags field for comma-separated tags.
    """

    tags = forms.CharField(
        required=False,
        help_text="Enter comma-separated tags (e.g. Django, Python, Web)",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter tags separated by commas",
            }
        ),
        label="Tags",
    )

    class Meta:
        model = Post
        fields = ("title", "content", "tags")
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter post title"}
            ),
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Write your post content here...",
                    "rows": 10,
                }
            ),
        }
        help_texts = {
            "title": "Max 200 characters",
            "content": "Write your blog post content",
        }
        labels = {
            "title": "Post Title",
            "content": "Post Content",
        }

    def save(self, commit=True, *args, **kwargs):
        instance = super().save(commit=False, *args, **kwargs)
        if commit:
            instance.save()

        # Tag handling logic
        tag_input = self.cleaned_data.get("tags", "")
        if tag_input:
            tag_names = [t.strip() for t in tag_input.split(",") if t.strip()]
            tag_objects = []
            for name in tag_names:
                tag_obj, _ = Tag.objects.get_or_create(name=name)
                tag_objects.append(tag_obj)
            instance.tags.set(tag_objects)
        else:
            instance.tags.clear()

        return instance


class CommentForm(forms.ModelForm):
    """
    Form for creating and updating comments.
    Only includes content field - post and author are set automatically.
    """

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
        labels = {
            "content": "Your Comment",
        }

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
