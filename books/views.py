from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, Borrow
from .forms import BookForm, BorrowForm


def book_list(request):
    books = Book.objects.all()
    borrows = Borrow.objects.all().order_by('-borrow_date')
    return render(request, 'books/book_list.html', {
        'books': books,
        'borrows': borrows
    })


def add_book(request):
    form = BookForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('book_list')
    return render(request, 'books/add_book.html', {
        'form': form,
        'page_title': 'Add Book'
    })


def edit_book(request, id):
    book = get_object_or_404(Book, id=id)
    form = BookForm(request.POST or None, instance=book)
    if form.is_valid():
        form.save()
        return redirect('book_list')
    return render(request, 'books/add_book.html', {
        'form': form,
        'page_title': 'Edit Book'
    })


def delete_book(request, id):
    book = get_object_or_404(Book, id=id)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'books/delete_book.html', {'book': book})


def borrow_book(request):
    form = BorrowForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        borrow = form.save(commit=False)

        book = borrow.book
        qty = borrow.quantity

        book.quantity -= qty
        book.save()

        borrow.save()

        return redirect('book_list')

    return render(request, 'books/borrow_book.html', {'form': form})



def return_book(request, id):
    borrow = get_object_or_404(Borrow, id=id)

    if not borrow.returned:
        borrow.returned = True

        borrow.book.quantity += borrow.quantity
        borrow.book.save()

        borrow.save()

    return redirect('book_list')
