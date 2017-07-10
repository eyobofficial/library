from django.contrib import admin
from .models import Genre, Book, BookInstance, Author, Language

# Register Book Model Object
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')

# Register Author Model Object
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    list_filter = ('date_of_birth', 'date_of_death')

# Register BookInstance Model Object
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'borrower', 'due_back', 'id')
    list_filter = ('status', 'due_back')

# Register Genre Model Object
admin.site.register(Genre)

# Register Languge Model Object
admin.site.register(Language)