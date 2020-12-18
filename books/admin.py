from django.contrib import admin
from .models import Book, Lead, File


class BookAdmin(admin.ModelAdmin):
    save_as = True
    save_on_top = True
    list_display = ('title', 'book_type', 'publication_date', )
    list_display_links = ('title', )
    search_fields = ('title', )
    # exclude = ('pk', )
    fields = (('title', ), ('book_type', 'publication_date'),
              ('pages', 'price'), )
    # readonly_fields = ('pk', )


admin.site.register(Book, BookAdmin)


class LeadAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    save_as = True
    save_on_top = True
    list_display = ('title', 'book', 'username', 'email', 'date_sent')
    list_display_links = ('title', 'book')
    search_fields = ('title', 'book')
    list_filter = ('book', )
    # list_editable = ('', )
    # readonly_fields = ('username',)
    ordering = ('book', 'order',)
    fields = (('title', 'slug'), ('username', 'email'),
              ('book', 'date_sent'), )


admin.site.register(Lead, LeadAdmin)


class FileAdmin(admin.ModelAdmin):
    save_as = True
    save_on_top = True
    list_display = ('book', 'file', 'uploaded_at', )
    list_display_links = ('file', )
    search_fields = ('file', )
    list_filter = ('book', )
    # list_editable = ('', )
    # readonly_fields = ('username',)
    ordering = ('book', 'order',)
    fields = ('book', 'file', 'uploaded_at', )


admin.site.register(File, FileAdmin)
