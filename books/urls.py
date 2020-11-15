from django.urls import path
from .views import *

app_name = 'books'

urlpatterns = [
    path('', home, name='home'),
    path('books/', books_list, name='books-list'),

    path('book/create/', BookCreate.as_view(), name='book-create'),
    path('book/<int:pk>/', BookUpdate.as_view(), name='book-update'),
    path('book/<int:pk>/delete/', BookDelete.as_view(), name='book-delete'),
]