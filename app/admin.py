from django.contrib import admin
from .models import Book, Lead, File


class FileInline(admin.StackedInline):
    model = File
    can_delete = True
    verbose_name = 'Files'
    verbose_name_plural = verbose_name
    fk_name = 'book'
    extra = 0
    readonly_fields = ('uploaded_at',)
    fields = (('file', 'uploaded_at'),)


class LeadInline(admin.StackedInline):
    model = Lead
    prepopulated_fields = {"slug": ("title",)}
    can_delete = True
    verbose_name = 'Leads'
    verbose_name_plural = verbose_name
    fk_name = 'book'
    extra = 0
    fields = (('title', 'slug'), ('username', 'email'), ('book', 'date_sent'), )


class BookAdmin(admin.ModelAdmin):
    inlines = (LeadInline, FileInline, )
    save_as = True
    save_on_top = True
    list_display = ('title', 'book_type', 'publication_date', 'get_files_count')
    list_display_links = ('title', )
    search_fields = ('title', )
    fields = (('title', ), ('book_type', 'publication_date'),
              ('pages', 'price'), )

    def get_files_count(self, instance):
        return instance.file_set.count()
    get_files_count.short_description = 'Files'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super().get_inline_instances(request, obj)


admin.site.register(Book, BookAdmin)