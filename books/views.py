from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Book
from .forms import BookForm

# View all books (READ)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'books/book_list.html', {'books': books})


# Add book (CREATE)
def add_book(request):
    form = BookForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('book_list')
    return render(request, 'books/add_book.html', {'form': form})


# Edit book (UPDATE)
def edit_book(request, id):
    book = get_object_or_404(Book, id=id)
    form = BookForm(request.POST or None, instance=book)
    if form.is_valid():
        form.save()
        return redirect('book_list')
    return render(request, 'books/add_book.html', {'form': form})


# Delete book (DELETE)
def delete_book(request, id):
    book = get_object_or_404(Book, id=id)
    book.delete()
    return redirect('book_list')
from .forms import BorrowForm
from .models import Borrow

# Borrow book
def borrow_book(request):
    form = BorrowForm(request.POST or None)
    if form.is_valid():
        borrow = form.save(commit=False)

        # Check if book is available
        if borrow.book.quantity > 0:
            borrow.book.quantity -= 1
            borrow.book.save()
            borrow.save()
            return redirect('book_list')

    return render(request, 'books/borrow_book.html', {'form': form})


# Return book
def return_book(request, id):
    borrow = get_object_or_404(Borrow, id=id)
    borrow.returned = True
    borrow.book.quantity += 1
    borrow.book.save()
    borrow.save()
    return redirect('book_list')