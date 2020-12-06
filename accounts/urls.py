from django.urls import path
from .views import *
from django.contrib.auth.views import LoginView, LogoutView
from .forms import LoginForm


app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='accounts/signin.html',
                                     authentication_form=LoginForm), name='login'),
    path('logout/', LogoutView.as_view(next_page='accounts:login'), name='logout'),
]
