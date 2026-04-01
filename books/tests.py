from django.test import TestCase
from django.urls import reverse

from .models import Book, Borrow


class BookViewsTests(TestCase):
    def test_book_list_page_loads(self):
        response = self.client.get(reverse("book_list"))

        self.assertEqual(response.status_code, 200)

    def test_add_book_creates_record(self):
        response = self.client.post(
            reverse("add_book"),
            {"title": "Django Basics", "author": "NCI", "quantity": 3},
        )

        self.assertRedirects(response, reverse("book_list"))
        self.assertTrue(Book.objects.filter(title="Django Basics").exists())

    def test_edit_book_updates_record(self):
        book = Book.objects.create(
            title="Old Title",
            author="Author",
            quantity=1,
        )

        response = self.client.post(
            reverse("edit_book", args=[book.id]),
            {"title": "New Title", "author": "Author", "quantity": 4},
        )

        self.assertRedirects(response, reverse("book_list"))
        book.refresh_from_db()
        self.assertEqual(book.title, "New Title")
        self.assertEqual(book.quantity, 4)

    def test_delete_book_removes_record(self):
        book = Book.objects.create(
            title="Delete Me",
            author="Author",
            quantity=1,
        )

        response = self.client.post(reverse("delete_book", args=[book.id]))

        self.assertRedirects(response, reverse("book_list"))
        self.assertFalse(Book.objects.filter(id=book.id).exists())


class BorrowFlowTests(TestCase):
    def test_borrow_book_reduces_stock_and_creates_record(self):
        book = Book.objects.create(title="Cloud", author="DevOps", quantity=5)

        response = self.client.post(
            reverse("borrow_book"),
            {"user_name": "Alice", "book": book.id, "quantity": 2},
        )

        self.assertRedirects(response, reverse("book_list"))
        book.refresh_from_db()
        self.assertEqual(book.quantity, 3)
        self.assertTrue(
            Borrow.objects.filter(user_name="Alice", book=book, quantity=2).exists()
        )

    def test_borrow_book_rejects_quantity_above_stock(self):
        book = Book.objects.create(title="Secure App", author="NCI", quantity=1)

        response = self.client.post(
            reverse("borrow_book"),
            {"user_name": "Bob", "book": book.id, "quantity": 3},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "Only 1 books available.",
        )
        book.refresh_from_db()
        self.assertEqual(book.quantity, 1)
        self.assertEqual(Borrow.objects.count(), 0)

    def test_return_book_requires_post(self):
        book = Book.objects.create(title="Python", author="Team", quantity=2)
        borrow = Borrow.objects.create(
            user_name="Cara",
            book=book,
            quantity=1,
        )

        response = self.client.get(reverse("return_book", args=[borrow.id]))

        self.assertEqual(response.status_code, 405)

    def test_return_book_marks_returned_and_restores_quantity(self):
        book = Book.objects.create(title="Python", author="Team", quantity=2)
        borrow = Borrow.objects.create(
            user_name="Cara",
            book=book,
            quantity=1,
        )
        book.quantity = 1
        book.save()

        response = self.client.post(reverse("return_book", args=[borrow.id]))

        self.assertRedirects(response, reverse("book_list"))
        borrow.refresh_from_db()
        book.refresh_from_db()
        self.assertTrue(borrow.returned)
        self.assertEqual(book.quantity, 2)
