from django import forms
from .models import Book, Borrow


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'quantity']


class BorrowForm(forms.ModelForm):
    class Meta:
        model = Borrow
        fields = ['user_name', 'book', 'quantity']

    def clean(self):
        cleaned_data = super().clean()
        book = cleaned_data.get("book")
        quantity = cleaned_data.get("quantity")

        if book and quantity:
            if quantity > book.quantity:
                raise forms.ValidationError(
                    f"Only {book.quantity} books available."
                )

        return cleaned_data
