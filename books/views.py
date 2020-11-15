from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import Book
from .forms import BookForm
from .ajax import AjaxCreateView, AjaxUpdateView, AjaxDeleteView


@login_required
def home(request):
    return redirect('books:books-list')

@login_required
def books_list(request):
    books = Book.objects.all()
    context = {"title": "Books", "object_list": books}
    return render(request, 'books.html', context)


class BookCreate(LoginRequiredMixin, AjaxCreateView):
    model = Book
    form_class = BookForm
    ajax_modal = 'ajax/form_modal.html'
    ajax_list = 'books_list.html'

class BookUpdate(LoginRequiredMixin, AjaxUpdateView):
    model = Book
    form_class = BookForm
    ajax_modal = 'ajax/form_modal.html'
    ajax_list = 'books_list.html'

class BookDelete(LoginRequiredMixin, AjaxDeleteView):
    model = Book
    ajax_modal = 'ajax/delete_modal.html'
    ajax_list = 'books_list.html'
