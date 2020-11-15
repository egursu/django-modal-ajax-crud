from django.contrib import admin
from .models import Book

class BookAdmin(admin.ModelAdmin):
    save_as = True
    save_on_top = True    
    list_display = ('title', 'book_type', 'publication_date', )
    list_display_links = ('title', )
    search_fields = ('title', )
    # exclude = ('pk', )
    fields = (('title', ), ('book_type', 'publication_date'), ('pages', 'price'), )
    # readonly_fields = ('pk', )

admin.site.register(Book, BookAdmin)
