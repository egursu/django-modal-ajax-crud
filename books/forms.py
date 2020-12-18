from django import forms
from .models import Book, Lead, File
from bootstrap_datepicker_plus import DatePickerInput


class BookForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Book
        fields = ('title', 'publication_date', 'price', 'pages', 'book_type', )
        widgets = {
            'publication_date': DatePickerInput(format='%Y-%m-%d'),
        }


class LeadForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['book'].empty_label = None
        if kwargs.get('instance') is None:
            self.fields['email'].help_text = 'email format: address@host.ext'

    class Meta:
        model = Lead
        fields = ('book', 'title', 'username', 'email', 'date_sent', )
        widgets = {
            'date_sent': DatePickerInput(format='%Y-%m-%d'),
        }


class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ('file', )

