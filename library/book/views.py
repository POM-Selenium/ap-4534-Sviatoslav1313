from django.shortcuts import render, get_object_or_404
from .models import Book
from order.models import Order
from authentication.models import CustomUser


def book_list_view(request):
    books = Book.objects.all()

    # Filtering
    title_query = request.GET.get('title', '')
    author_query = request.GET.get('author', '')

    if title_query:
        books = books.filter(name__icontains=title_query)
    if author_query:
        books = books.filter(
            authors__name__icontains=author_query
        ) | books.filter(
            authors__surname__icontains=author_query
        )
        books = books.distinct()

    context = {
        'books': books,
        'title_query': title_query,
        'author_query': author_query,
    }
    return render(request, 'book/book_list.html', context)


def book_detail_view(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    authors = book.authors.all()
    return render(request, 'book/book_detail.html', {'book': book, 'authors': authors})


def user_books_view(request, user_id):
    user_obj = get_object_or_404(CustomUser, id=user_id)
    orders = Order.objects.filter(user=user_obj, end_at__isnull=True)
    books = [order.book for order in orders]
    return render(request, 'book/user_books.html', {
        'books': books,
        'user_obj': user_obj,
    })
