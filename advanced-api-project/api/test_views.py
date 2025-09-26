# Test file

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from api.models import Book, Author
from django.contrib.auth.models import User


class BookAPITests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.author = Author.objects.create(name="Test Author")
        self.book = Book.objects.create(
            title="Test Book", author=self.author, isbn="1234567890"
        )
        self.book_data = {
            "title": "New Book",
            "author": self.author.id,
            "isbn": "0987654321",
        }

    def test_get_book_list(self):
        url = reverse("book-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_book_detail(self):
        url = reverse("book-detail", kwargs={"pk": self.book.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Test Book")

    def test_create_book(self):
        url = reverse("book-list")
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, self.book_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)

    def test_update_book(self):
        url = reverse("book-detail", kwargs={"pk": self.book.id})
        self.client.force_authenticate(user=self.user)
        updated_data = {
            "title": "Updated Book",
            "author": self.author.id,
            "isbn": "1111111111",
        }
        response = self.client.put(url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Updated Book")

    def test_delete_book(self):
        url = reverse("book-detail", kwargs={"pk": self.book.id})
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

    def test_search_books(self):
        another_author = Author.objects.create(name="Another Author")
        Book.objects.create(
            title="Another Book", author=another_author, isbn="9876543210"
        )
        url = reverse("book-list") + "?search=Another"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Another Book")

    def test_filter_books(self):
        python_author = Author.objects.create(name="Python Author")
        Book.objects.create(
            title="Python Book", author=python_author, isbn="1111111111"
        )
        url = reverse("book-list") + f"?author={python_author.id}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Python Book")

    def test_order_books(self):
        another_author = Author.objects.create(name="A Author")
        Book.objects.create(title="A Book", author=another_author, isbn="2222222222")
        url = reverse("book-list") + "?ordering=title"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["title"], "A Book")
        self.assertEqual(response.data[1]["title"], "Test Book")

    def test_unauthenticated_create(self):
        url = reverse("book-list")
        response = self.client.post(url, self.book_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthenticated_update(self):
        url = reverse("book-detail", kwargs={"pk": self.book.id})
        response = self.client.put(url, self.book_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthenticated_delete(self):
        url = reverse("book-detail", kwargs={"pk": self.book.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.login
