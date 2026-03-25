from django.contrib import admin

from .models import Book, Borrow


admin.site.site_header = "Library Management Admin"
admin.site.site_title = "Library Admin"
admin.site.index_title = "Admin Dashboard"


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "quantity")
    search_fields = ("title", "author")
    list_filter = ("author",)
    ordering = ("title",)


@admin.register(Borrow)
class BorrowAdmin(admin.ModelAdmin):
    list_display = ("user_name", "book", "quantity", "borrow_date", "returned")
    list_filter = ("returned", "borrow_date")
    search_fields = ("user_name", "book__title")
    ordering = ("-borrow_date",)
