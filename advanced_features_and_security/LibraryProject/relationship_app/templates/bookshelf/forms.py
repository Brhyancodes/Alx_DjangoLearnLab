from django import forms
from .models import Book, CustomUser
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class BookForm(forms.ModelForm):
    """
    Form for creating and updating Book objects.
    Using ModelForm ensures validation and protects against SQL injection.
    """
    class Meta:
        model = Book
        fields = ["title", "author", "publication_year"]


class CustomUserCreationForm(UserCreationForm):
    """
    Form for creating new CustomUser objects.
    Extends Django’s built-in UserCreationForm to work with CustomUser.
    """
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("username", "email", "date_of_birth", "profile_photo")


class CustomUserChangeForm(UserChangeForm):
    """
    Form for updating existing CustomUser objects.
    """
    class Meta:
        model = CustomUser
        fields = ("username", "email", "date_of_birth", "profile_photo")
