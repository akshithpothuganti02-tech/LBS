from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.book_list, name='book_list'),
    path('add/', views.add_book, name='add_book'),
    path('edit/<int:id>/', views.edit_book, name='edit_book'),
    path('delete/<int:id>/', views.delete_book, name='delete_book'),
    path('borrow/', views.borrow_book, name='borrow_book'),
    path('return/<int:id>/', views.return_book, name='return_book'),
]
