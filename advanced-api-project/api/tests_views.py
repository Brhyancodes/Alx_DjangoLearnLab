# api/test_views.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status

from .models import Book

User = get_user_model()


class BookAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create two users
        self.user = User.objects.create_user(username="user1", password="pass123")
        self.other_user = User.objects.create_user(username="user2", password="pass456")

        # Create some Book instances for testing
        Book.objects.create(
            title="Django Unchained", author="Quentin", publication_year=2012
        )
        Book.objects.create(
            title="Learning Django", author="Ryan", publication_year=2020
        )
        Book.objects.create(title="Python Tricks", author="Dan", publication_year=2018)

        # URL names (adjust if your names differ)
        self.list_url = reverse("book-list")  # /api/books/
        self.create_url = reverse("book-create")  # /api/books/create/

        # We'll reference a single book later
        self.book = Book.objects.first()
        self.detail_url = reverse("book-detail", kwargs={"pk": self.book.pk})
        self.update_url = reverse("book-update", kwargs={"pk": self.book.pk})
        self.delete_url = reverse("book-delete", kwargs={"pk": self.book.pk})

    def test_list_books_public(self):
        """Anyone (even unauthenticated) can list books."""
        resp = self.client.get(self.list_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()
        # Ensure at least the 3 initial books exist
        self.assertGreaterEqual(len(data), 3)

    def test_retrieve_book_public(self):
        """Anyone can retrieve a single book detail."""
        resp = self.client.get(self.detail_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        payload = resp.json()
        self.assertEqual(payload["id"], self.book.pk)
        self.assertIn("title", payload)
        self.assertIn("author", payload)

    def test_create_book_unauthenticated_forbidden(self):
        """Creating a book requires authentication."""
        payload = {"title": "New Book", "author": "Anon", "publication_year": 2025}
        resp = self.client.post(self.create_url, payload, format="json")
        self.assertIn(
            resp.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN)
        )

    def test_create_book_authenticated(self):
        """Authenticated users can create books."""
        self.client.force_authenticate(self.user)
        payload = {"title": "New Book", "author": "Anon", "publication_year": 2025}
        resp = self.client.post(self.create_url, payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        body = resp.json()
        self.assertEqual(body["title"], payload["title"])
        self.assertEqual(body["author"], payload["author"])
        # cleanup auth for next tests
        self.client.force_authenticate(None)

    def test_update_book_unauthenticated_forbidden(self):
        """Updating a book requires authentication."""
        payload = {"title": "Changed Title"}
        resp = self.client.patch(self.update_url, payload, format="json")
        self.assertIn(
            resp.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN)
        )

    def test_update_book_authenticated(self):
        """Authenticated user can update a book."""
        self.client.force_authenticate(self.user)
        payload = {"title": "Changed Title"}
        resp = self.client.patch(self.update_url, payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Changed Title")
        self.client.force_authenticate(None)

    def test_delete_book_unauthenticated_forbidden(self):
        """Deleting requires authentication."""
        resp = self.client.delete(self.delete_url)
        self.assertIn(
            resp.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN)
        )

    def test_delete_book_authenticated(self):
        """Authenticated user can delete a book."""
        # Create a fresh book to delete
        b = Book.objects.create(
            title="To be deleted", author="X", publication_year=1999
        )
        delete_url = reverse("book-delete", kwargs={"pk": b.pk})

        self.client.force_authenticate(self.user)
        resp = self.client.delete(delete_url)
        # Accept either 204 No Content or 200 OK depending on your view
        self.assertIn(
            resp.status_code, (status.HTTP_204_NO_CONTENT, status.HTTP_200_OK)
        )
        self.assertFalse(Book.objects.filter(pk=b.pk).exists())
        self.client.force_authenticate(None)

    def test_filtering_by_author_and_publication_year(self):
        """Filtering on filterset_fields works."""
        resp = self.client.get(self.list_url, {"author": "Ryan"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()
        for item in data:
            self.assertIn("Ryan", item["author"] or "")

        resp = self.client.get(self.list_url, {"publication_year": 2018})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()
        # all returned items should have publication_year == 2018
        for item in data:
            self.assertEqual(item.get("publication_year"), 2018)

    def test_searching_title_and_author(self):
        """SearchFilter should return matching results for querystring `search`."""
        resp = self.client.get(self.list_url, {"search": "Django"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()
        # each returned item should contain "Django" in title or author
        self.assertGreaterEqual(len(data), 1)
        matches = 0
        for item in data:
            text = f'{item.get("title","")} {item.get("author","")}'.lower()
            if "django" in text:
                matches += 1
        self.assertGreaterEqual(matches, 1)

    def test_ordering_by_publication_year_and_title(self):
        """OrderingFilter should sort results correctly."""
        # order ascending by publication_year
        resp = self.client.get(self.list_url, {"ordering": "publication_year"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()
        years = [
            item.get("publication_year")
            for item in data
            if item.get("publication_year") is not None
        ]
        self.assertEqual(sorted(years), years)

        # order descending by title
        resp = self.client.get(self.list_url, {"ordering": "-title"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()
        titles = [item.get("title") for item in data if item.get("title") is not None]
        self.assertEqual(sorted(titles, reverse=True), titles)

    def test_permissions_enforced_on_endpoints(self):
        """Quick sanity for permission behavior on endpoints."""
        # list and detail should be public
        res_list = self.client.get(self.list_url)
        res_detail = self.client.get(self.detail_url)
        self.assertEqual(res_list.status_code, status.HTTP_200_OK)
        self.assertEqual(res_detail.status_code, status.HTTP_200_OK)

        # create/update/delete should require auth
        res_create = self.client.post(self.create_url, {"title": "x", "author": "y"})
        self.assertIn(
            res_create.status_code,
            (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN),
        )

        res_update = self.client.patch(self.update_url, {"title": "y"})
        self.assertIn(
            res_update.status_code,
            (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN),
        )

        res_delete = self.client.delete(self.delete_url)
        self.assertIn(
            res_delete.status_code,
            (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN),
        )


"""
How to run:
    python manage.py test api

Notes:
- The tests assume your Book serializer returns at least: id, title, author, publication_year.
- If your API requires extra fields or owner logic, adjust the payloads/assertions accordingly.
- If URL names differ, change the reverse() calls to match your configuration.
"""
