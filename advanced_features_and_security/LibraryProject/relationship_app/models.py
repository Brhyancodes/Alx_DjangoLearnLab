from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver


# --- Custom User Manager ---
class CustomUserManager(BaseUserManager):
    def create_user(
        self, username, email=None, password=None, date_of_birth=None, **extra_fields
    ):
        if not username:
            raise ValueError("The Username field must be set")

        email = self.normalize_email(email)
        user = self.model(
            username=username, email=email, date_of_birth=date_of_birth, **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, username, email=None, password=None, date_of_birth=None, **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(
            username, email, password, date_of_birth, **extra_fields
        )


# --- Custom User Model ---
class CustomUser(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(
        upload_to="profile_photos/", null=True, blank=True
    )

    objects = CustomUserManager()

    def __str__(self):
        return self.username


# --- Author model (with permissions) ---
class Author(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        permissions = [
            ("can_view_author", "Can view author"),
            ("can_create_author", "Can create author"),
            ("can_edit_author", "Can edit author"),
            ("can_delete_author", "Can delete author"),
        ]

    def __str__(self):
        return self.name


# --- Book model (already had these — kept them) ---
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    class Meta:
        permissions = [
            ("can_view_book", "Can view book"),
            ("can_create_book", "Can create book"),
            ("can_edit_book", "Can edit book"),
            ("can_delete_book", "Can delete book"),
        ]

    def __str__(self):
        return self.title


# --- Library model (with permissions) ---
class Library(models.Model):
    name = models.CharField(max_length=100)
    books = models.ManyToManyField(Book)

    class Meta:
        permissions = [
            ("can_view_library", "Can view library"),
            ("can_create_library", "Can create library"),
            ("can_edit_library", "Can edit library"),
            ("can_delete_library", "Can delete library"),
        ]

    def __str__(self):
        return self.name


# --- Librarian (simple) ---
class Librarian(models.Model):
    name = models.CharField(max_length=100)
    library = models.OneToOneField(Library, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# --- UserProfile linking to CustomUser ---
class UserProfile(models.Model):
    ROLE_CHOICES = [
        ("Admin", "Admin"),
        ("Librarian", "Librarian"),
        ("Member", "Member"),
    ]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="Member")

    def __str__(self):
        return f"{self.user.username} - {self.role}"


# --- Signals to create/save UserProfile ---
@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, "userprofile"):
        instance.userprofile.save()
    else:
        UserProfile.objects.create(user=instance)
