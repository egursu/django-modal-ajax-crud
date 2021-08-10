from django.urls import path
from .views import *

app_name = 'app'

urlpatterns = [
    path('', home, name='home'),

    path('books/', BookList.as_view(), name='book-list'),

    path('book/create/', BookCreate.as_view(), name='book-create'),
    path('book/update/<int:pk>/', BookUpdate.as_view(), name='book-update'),
    path('book/delete/<int:pk>/', BookDelete.as_view(), name='book-delete'),
    path('book/<int:pk>/', BookDetail.as_view(), name='book-detail'),

    path('book/<int:book>/files', FileList.as_view(), name='file-list'),
    path('book/<int:book>/files/upload', FileUpload.as_view(), name='file-upload'),
    path('book/<int:book>/file/<int:pk>/delete/', FileDelete.as_view(), name='file-delete'),

    path('book/<int:book>/leads', LeadList.as_view(), name='lead-list'),
    path('book/<int:book>/lead/create/', LeadCreate.as_view(), name='lead-create'),
    path('book/<int:book>/lead/update/<int:pk>/', LeadUpdate.as_view(), name='lead-update'),
    path('book/<int:book>/lead/delete/<int:pk>/', LeadDelete.as_view(), name='lead-delete'),
    path('book/<int:book>/lead/<int:pk>/', LeadDetail.as_view(), name='lead-detail'),
]