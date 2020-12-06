from django.urls import path
from .views import *

app_name = 'books'

urlpatterns = [
    path('', home, name='home'),

    path('books/', books_list, name='books-list'),
    path('book/create/', BookCreate.as_view(), name='book-create'),
    path('book/<int:pk>/', BookUpdate.as_view(), name='book-update'),
    path('book/<int:pk>/delete/', BookDelete.as_view(), name='book-delete'),

    path('book/<int:book>/leads/', leads_list, name='leads-list'),
    path('book/<int:book>/lead/create/',
         LeadCreate.as_view(), name='lead-create'),
    path('book/<int:book>/lead/<slug:slug>/',
         LeadUpdate.as_view(), name='lead-update'),
    path('book/<int:book>/lead/<slug:slug>/delete/',
         LeadDelete.as_view(), name='lead-delete'),
]
