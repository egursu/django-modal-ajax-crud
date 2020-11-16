from django import forms
from .models import Book, Lead
from bootstrap_datepicker_plus import DatePickerInput


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('title', 'publication_date', 'price', 'pages', 'book_type', )
        widgets = {
            'publication_date': DatePickerInput(format='%Y-%m-%d'),
        }

class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ('book', 'title', 'username', 'email', 'date_sent', )
        widgets = {
            # 'book': forms.Select(attrs={'disabled':'True'}),
            'date_sent': DatePickerInput(format='%Y-%m-%d'),
        }
