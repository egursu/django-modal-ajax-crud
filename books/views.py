from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import Book, Lead, File
from .forms import BookForm, LeadForm, FileForm
from cms.ajax import AjaxCreateView, AjaxUpdateView, AjaxDeleteView, AjaxFilesUpload
from django.views.generic import View
from django.http import JsonResponse
from django.template.loader import render_to_string
import time


@login_required
def home(request):
    return redirect('books:books-list')


@login_required
def books_list(request):
    books = Book.objects.all()
    context = {"title": "Books", "book_list": books}
    return render(request, 'books/books.html', context)


class BookCreate(LoginRequiredMixin, AjaxCreateView):
    model = Book
    form_class = BookForm
    ajax_modal = 'ajax/form_modal.html'
    ajax_list = 'books/books_list.html'


class BookUpdate(LoginRequiredMixin, AjaxUpdateView):
    model = Book
    form_class = BookForm
    ajax_modal = 'ajax/form_modal.html'
    ajax_list = 'books/books_list.html'


class BookDelete(LoginRequiredMixin, AjaxDeleteView):
    model = Book
    ajax_modal = 'ajax/delete_modal.html'
    ajax_list = 'books/books_list.html'


@login_required
def leads_list(request, book):
    book_obj = get_object_or_404(Book, pk=book)
    title = "Leads on {}".format(book_obj)
    leads = book_obj.lead_set.all()
    context = {"title": title, "book": book_obj, "lead_list": leads}
    return render(request, 'books/leads.html', context)


class LeadCreate(LoginRequiredMixin, AjaxCreateView):
    model = Lead
    form_class = LeadForm
    ajax_modal = 'ajax/form_modal.html'
    ajax_list = 'books/leads_list.html'


class LeadUpdate(LoginRequiredMixin, AjaxUpdateView):
    model = Lead
    form_class = LeadForm
    ajax_modal = 'ajax/form_modal.html'
    ajax_list = 'books/leads_list.html'


class LeadDelete(LoginRequiredMixin, AjaxDeleteView):
    model = Lead
    ajax_modal = 'ajax/delete_modal.html'
    ajax_list = 'books/leads_list.html'


@login_required
def file_list(request, book):
    book_obj = get_object_or_404(Book, pk=book)
    title = "Files on {}".format(book_obj)
    files = book_obj.file_set.all()
    context = {"title": title, "book": book_obj, "file_list": files}
    return render(request, 'books/files.html', context)


class FilesUpload(LoginRequiredMixin, AjaxFilesUpload):
    model = File
    form_class = FileForm
    ajax_list = 'books/files_list.html'


class FileDelete(LoginRequiredMixin, AjaxDeleteView):
    model = File
    ajax_modal = 'ajax/delete_modal.html'
    ajax_list = 'books/files_list.html'