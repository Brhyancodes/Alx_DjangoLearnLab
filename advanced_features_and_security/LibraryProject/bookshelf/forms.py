from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

# Import models from the same app
from .models import Book, CustomUser


class ExampleForm(forms.Form):
    """
    Simple example form used by the project's checker and demos.

    Fields:
      - title (required)
      - author (required)
      - publication_year (optional)
    """

    title = forms.CharField(max_length=200, required=True)
    author = forms.CharField(max_length=100, required=True)
    publication_year = forms.IntegerField(required=False, min_value=0)

    def clean_title(self):
        title = self.cleaned_data.get("title", "").strip()
        if not title:
            raise forms.ValidationError("Title is required.")
        # additional validation can go here
        return title


class BookForm(forms.ModelForm):
    """
    ModelForm to create/edit Book instances. Validates input and prevents raw SQL usage.
    """

    class Meta:
        model = Book
        fields = ["title", "author", "publication_year"]

    def clean_title(self):
        title = self.cleaned_data.get("title", "").strip()
        if not title:
            raise forms.ValidationError("Title cannot be empty.")
        if len(title) > 200:
            raise forms.ValidationError("Title is too long.")
        return title


class CustomUserCreationForm(UserCreationForm):
    """
    Creation form for CustomUser.
    """

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("username", "email", "date_of_birth", "profile_photo")


class CustomUserChangeForm(UserChangeForm):
    """
    Form for updating CustomUser.
    """

    class Meta:
        model = CustomUser
        fields = ("username", "email", "date_of_birth", "profile_photo")
