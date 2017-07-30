from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date

import uuid

class Genre(models.Model):
    """
    Model representing a book genre (e.g Science Fiction, Non Fiction, Fantasy etc)
    """
    name = models.CharField(max_length=120, help_text='Enter a book genre (e.g. Science Fiction, None Fiction)')

    def __str__(self):
        """
        String representing the Model object
        """
        return self.name

class Book(models.Model):
    """
    Model representing a book (but not a specific copy of a book)
    """
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    isbn = models.CharField('ISBN', max_length=13, help_text='13 character ISBN number')
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True, help_text='Book Language')
    summary = models.TextField(help_text='Brief description of the book', null=True, blank=True)

    def __str__(self):
        """
        String for the representing the Book Model object
        """
        return self.title

    def get_absolute_url(self):
        """
        Returns the url to access a particular book instance
        """
        return reverse('catalog:book-detail', kwargs={'pk': self.pk})

class BookInstance(models.Model):
    """
    Model representing a particular book copy which can be borrowed
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique id for this book copy')
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    LOAN_STATUS = (
            ('d', 'Maintenance'),
            ('o', 'On loan'),
            ('a', 'Available'),
            ('r', 'Reserved'),
        )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='d', help_text='Book Availablity Status')

    class Meta:
        ordering = ['due_back']
        verbose_name = 'Book Copy'
        verbose_name_plural = 'Book Copies'
        permissions = (
                ('return_bookinstance', 'Return borrowed bookinstance'),
            )

    @property 
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        else:
            return False

    def __str__(self):
        """
        Return string repsentation of BookInstance Model Object
        """
        return '{} ({})'.format(self.id, self.book.title)

class Author(models.Model):
    """
    Model representing an Author
    """
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    def full_name(self):
        """
        Return the full name of a particular author
        """
        return '{} {}'.format(self.first_name, self.last_name)

    def get_absolute_url(self):
        """
        Returns the url to access a particular author
        """
        return reverse('catalog:author_detail', kwargs={'pk': str(self.pk)})

    def __str__(self):
        """
        String representation of Author Model object
        """
        return '{}, {}'.format(self.last_name, self.first_name)

class Language(models.Model):
    """
    Model representing a language
    """
    name = models.CharField(max_length=60)

    def __str__(self):
        """
        String repersentation of Language Model object
        """
        return self.name













