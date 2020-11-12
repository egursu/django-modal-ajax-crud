from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    context = {"title": 'Books'}
    return render(request, 'book_list.html', context)