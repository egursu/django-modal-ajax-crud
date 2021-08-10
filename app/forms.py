from django import forms
from .models import Book, Lead, File
from bootstrap_datepicker_plus import DatePickerInput
from cms.forms import BootstrapHelperForm


class BookForm(BootstrapHelperForm, forms.ModelForm):
    class Meta:
        model = Book
        fields = ('title', 'publication_date', 'price', 'pages', 'book_type', )
        widgets = {
            'publication_date': DatePickerInput(format='%Y-%m-%d'),
        }


class LeadForm(BootstrapHelperForm, forms.ModelForm):
    class Meta:
        model = Lead
        fields = ('book', 'title', 'username', 'email', 'date_sent', )
        widgets = {
            'book': forms.HiddenInput(),
            'date_sent': DatePickerInput(format='%Y-%m-%d'),
        }


class FileForm(BootstrapHelperForm, forms.ModelForm):
    class Meta:
        model = File
        fields = ('file', )