from django.urls import path
from cms.ajax import AjaxReorderView

app_name = 'cms'

urlpatterns = [
    path('ajax/reorder/<str:model>/', AjaxReorderView.as_view(), name='reorder'),
]
