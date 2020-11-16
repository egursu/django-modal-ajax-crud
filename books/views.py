from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import Book, Lead
from .forms import BookForm, LeadForm
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
    # template_name = 'ajax/form_modal_fields.html'
    ajax_modal = 'ajax/form_modal.html'
    ajax_list = 'books_list.html'

class BookDelete(LoginRequiredMixin, AjaxDeleteView):
    model = Book
    ajax_modal = 'ajax/delete_modal.html'
    ajax_list = 'books_list.html'



@login_required
def leads_list(request, book):
    book_obj = get_object_or_404(Book, pk=book)
    title = "Leads on {}".format(book_obj)
    leads = book_obj.lead_set.all()
    context = {"title": title, "book": book_obj, "object_list": leads}
    return render(request, 'leads.html', context)

class LeadCreate(LoginRequiredMixin, AjaxCreateView):
    model = Lead
    form_class = LeadForm
    ajax_modal = 'ajax/form_modal.html'
    ajax_list = 'leads_list.html'

class LeadUpdate(LoginRequiredMixin, AjaxUpdateView):
    model = Lead
    form_class = LeadForm
    # template_name = 'ajax/form_modal_fields.html'
    ajax_modal = 'ajax/form_modal.html'
    ajax_list = 'leads_list.html'

class LeadDelete(LoginRequiredMixin, AjaxDeleteView):
    model = Lead
    ajax_modal = 'ajax/delete_modal.html'
    ajax_list = 'leads_list.html'