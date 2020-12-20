from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from cms.fields import OrderField
from pathlib import Path


class Book(models.Model):
    HARDCOVER = 1
    PAPERBACK = 2
    EBOOK = 3
    BOOK_TYPES = (
        (HARDCOVER, 'Hardcover'),
        (PAPERBACK, 'Paperback'),
        (EBOOK, 'E-book'),
    )
    title = models.CharField(max_length=50, verbose_name='Title')
    publication_date = models.DateField(null=True, verbose_name='Publicate on')
    price = models.DecimalField(
        max_digits=5, decimal_places=2, verbose_name='Price, €')
    pages = models.IntegerField(blank=True, null=True, verbose_name='Pages')
    book_type = models.PositiveSmallIntegerField(
        choices=BOOK_TYPES, default=EBOOK, verbose_name='Book type')
    # order = models.PositiveSmallIntegerField(default=0, verbose_name='Order')
    order = OrderField(blank=True, verbose_name='Order #')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('books:book-update', kwargs={'pk': self.pk})

    class Meta:
        # db_table = 'books'
        ordering = ['order']
        verbose_name = 'Book'
        verbose_name_plural = 'Books'


class Lead(models.Model):
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, verbose_name='Book')
    slug = models.SlugField(max_length=255, verbose_name='Slug', unique=True)
    title = models.CharField(max_length=100, verbose_name='Title')
    username = models.CharField(max_length=90, verbose_name='User name')
    email = models.EmailField(verbose_name='email')
    date_sent = models.DateTimeField(
        blank=True, null=True, verbose_name='Date sent')
    # order = models.PositiveSmallIntegerField(default=0, verbose_name='Order')
    order = OrderField(blank=True, for_fields=['book'], verbose_name='Order #')

    def __str__(self):
        return str(self.title)

    def save(self, *args, **kwargs):
        self.slug = slugify('{}-{}-{}'.format(self.title,
                                              self.book.title, self.book.pk))
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('books:lead-update', kwargs={'book': self.book.pk, 'slug': self.slug})

    class Meta:
        verbose_name = 'Lead'
        verbose_name_plural = 'Leads'
        ordering = ('order', '-date_sent')


class File(models.Model):
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, verbose_name='Book')
    file = models.FileField(upload_to='files/', null=True,
                            blank=True, max_length=255, verbose_name='Filename')
    uploaded_at = models.DateTimeField(
        auto_now_add=True, null=True, blank=True, verbose_name='File uploaded at')
    order = OrderField(blank=True, for_fields=['book'], verbose_name='Order #')

    @property
    def filename(self):
        return Path(self.file.name).name

    def __str__(self):
        return self.filename

    def save(self, *args, **kwargs):
        if self.pk:
            old_file = File.objects.get(pk=self.pk).file
            if not old_file == self.file:
                storage = old_file.storage
                if storage.exists(old_file.name):
                    storage.delete(old_file.name)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        storage = self.file.storage
        if storage.exists(self.file.name):
            storage.delete(self.file.name)
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name = 'File'
        verbose_name_plural = 'Files'
        ordering = ('order', )
