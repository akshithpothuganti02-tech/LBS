from django import forms
from .models import Book, Borrow

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'quantity']
        from .models import Borrow

class BorrowForm(forms.ModelForm):
    class Meta:
        model = Borrow
        fields = ['user_name', 'book']
        from django.core.exceptions import ValidationError

class BorrowForm(forms.ModelForm):
    class Meta:
        model = Borrow
        fields = ['user_name', 'book']

    def clean_book(self):
        book = self.cleaned_data['book']
        if book.quantity <= 0:
            raise forms.ValidationError("Book not available")
        return book