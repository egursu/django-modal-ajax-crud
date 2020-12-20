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



class BookAdmin(admin.ModelAdmin):
    inlines = (FileInline, )
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
