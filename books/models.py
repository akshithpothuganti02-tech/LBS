from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.title


class Borrow(models.Model):
    user_name = models.CharField(max_length=100)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    borrow_date = models.DateTimeField(auto_now_add=True)
    returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user_name} - {self.book.title}"
