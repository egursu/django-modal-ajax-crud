from django.db import models
from django.urls import reverse
from django.utils.text import slugify 
from cms.fields import OrderField


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
    price = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Price, €')
    pages = models.IntegerField(blank=True, null=True, verbose_name='Pages')
    book_type = models.PositiveSmallIntegerField(choices=BOOK_TYPES, verbose_name='Book type')
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
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='Book')
    slug = models.SlugField(max_length=255, verbose_name='Slug', unique=True)
    title = models.CharField(max_length=100, verbose_name='Title')
    username = models.CharField(max_length=90, verbose_name='User name')
    email = models.EmailField(verbose_name='email')
    date_sent = models.DateTimeField(blank=True, null=True, verbose_name='Date sent')
    # order = models.PositiveSmallIntegerField(default=0, verbose_name='Order')
    order = OrderField(blank=True, for_fields=['book'], verbose_name='Order #')

    def __str__(self):
        return str(self.title)

    def save(self, *args, **kwargs):
        self.slug = slugify('{}-{}-{}'.format(self.title, self.book.title, self.book.pk))
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('books:lead-update', kwargs={'book': self.book.pk, 'slug': self.slug})

    class Meta:
        verbose_name = 'Lead'
        verbose_name_plural = 'Leads'
        ordering = ('order', '-date_sent')
