from django.db import models
from django.urls import reverse


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

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('books:book-update', kwargs={'pk': self.pk})

    class Meta:
        # db_table = 'books'
        verbose_name = 'Book'
        verbose_name_plural = 'Books'