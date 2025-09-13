from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from relationship_app.models import Author, Book, Library


class Command(BaseCommand):
    help = "Create default groups and assign permissions"

    def handle(self, *args, **kwargs):
        # Define groups and their permissions
        groups_permissions = {
            "Admins": [
                "can_view_author",
                "can_create_author",
                "can_edit_author",
                "can_delete_author",
                "can_view_book",
                "can_create_book",
                "can_edit_book",
                "can_delete_book",
                "can_view_library",
                "can_create_library",
                "can_edit_library",
                "can_delete_library",
            ],
            "Editors": [
                "can_create_author",
                "can_edit_author",
                "can_create_book",
                "can_edit_book",
                "can_create_library",
                "can_edit_library",
            ],
            "Viewers": [
                "can_view_author",
                "can_view_book",
                "can_view_library",
            ],
        }

        # Loop through groups and assign permissions
        for group_name, perms in groups_permissions.items():
            group, created = Group.objects.get_or_create(name=group_name)
            for perm_codename in perms:
                try:
                    perm = Permission.objects.get(codename=perm_codename)
                    group.permissions.add(perm)
                except Permission.DoesNotExist:
                    self.stdout.write(
                        self.style.WARNING(f"Permission {perm_codename} not found!")
                    )
            group.save()
            self.stdout.write(self.style.SUCCESS(f"Group '{group_name}' updated."))
