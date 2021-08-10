from django.urls import path
from .views import *
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import views
from django.contrib.auth.forms import AuthenticationForm

app_name = 'account'

urlpatterns = [
    path('login/', views.LoginView.as_view(template_name='account/signin.html',
                                           authentication_form=AuthenticationForm,
                                           extra_context={
                                               'title': 'Login',
                                               'extra_title': 'Please sign in',
                                           }), name='login'),
    path('logout/', views.LogoutView.as_view(next_page='account:login'), name='logout'),
]