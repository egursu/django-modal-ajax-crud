from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from .models import Book, Lead, File
from .forms import BookForm, LeadForm, FileForm
from cms.ajax import (AjaxCreateView, AjaxDetailView, AjaxUpdateView, AjaxDeleteView, AjaxFilesUpload)
from cms.views import CoreListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    # return render(request, 'blank.html', context={'title': 'Blank page'})
    return redirect('app:book-list')


class BookList(LoginRequiredMixin, CoreListView):
    model = Book


class BookCreate(LoginRequiredMixin, AjaxCreateView):
    model = Book
    form_class = BookForm

    # def get_redirect_url(self):
    #     return reverse_lazy('app:home')


class BookUpdate(LoginRequiredMixin, AjaxUpdateView):
    model = Book
    form_class = BookForm

class BookDelete(LoginRequiredMixin, AjaxDeleteView):
    model = Book

class BookDetail(LoginRequiredMixin, AjaxDetailView):
    model = Book
    # form_class = BookForm


class LeadList(LoginRequiredMixin, CoreListView):
    model = Lead

class LeadCreate(LoginRequiredMixin, AjaxCreateView):
    model = Lead
    form_class = LeadForm

class LeadUpdate(LoginRequiredMixin, AjaxUpdateView):
    model = Lead
    form_class = LeadForm

class LeadDelete(LoginRequiredMixin, AjaxDeleteView):
    model = Lead

class LeadDetail(LoginRequiredMixin, AjaxDetailView):
    model = Lead


class FileList(LoginRequiredMixin, CoreListView):
    model = File

class FileUpload(LoginRequiredMixin, AjaxFilesUpload):
    model = File
    form_class = FileForm

class FileDelete(LoginRequiredMixin, AjaxDeleteView):
    model = File