from django.shortcuts import render
from django.views import generic
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import Group
from .models import Book, BookInstance, Genre, Author, Language
from .forms import ContactUsForm

def index(request):
    """
    Handles the index (home page) of the catalog app
    """

    # Track user's website (home page) visit
    visit_count = request.session.get('visit_count', 0)
    request.session['visit_count'] = visit_count + 1

    return render(request, 'catalog/index.html', {
            'page_title': 'Home',
            'book_count': Book.objects.count(),
            'copies_count': BookInstance.objects.count(),
            'available_count': BookInstance.objects.filter(status='a').count(),
            'author_count': Author.objects.count(),
            'visit_count': visit_count,
        })

class BookListView(generic.ListView):
    """
    Returns list of all books
    """
    model = Book

    def get_context_data(self, *args, **kwargs):
        """
        Return the page title along with list of all books
        """
        context = super(BookListView, self).get_context_data()
        context['page_title'] = 'Books'
        return context

class BookDetailView(generic.DetailView):
    """
    Returns a particular book
    """
    model = Book

    def get_context_data(self, *args, **kwargs):
        """
        Return the page title along with list of all books
        """
        context = super(BookDetailView, self).get_context_data()
        context['page_title'] = 'Book'
        return context

class AuthorListView(generic.ListView):
    """
    Returns list of all authors
    """
    model = Author 
    paginate_by = 4

    def get_context_data(self):
        """
        Returns the page title to the template along side the context data
        """
        context = super(AuthorListView, self).get_context_data()
        context['page_title'] = 'Authors'
        return context

class BorrowedBookList(LoginRequiredMixin, generic.ListView):
    """
    Returns list of borrowed book by a logged user
    """
    model = BookInstance
    template_name = 'catalog/user_borrowed_books.html'
    paginate_by = 2

    def get_queryset(self):
        return BookInstance.objects.filter(borrower = self.request.user).filter(status__exact = 'o').order_by('due_back')

    def get_context_data(self):
        context = super(BorrowedBookList, self).get_context_data()
        context['page_title'] = 'My Books'
        return context

class AllBorrowedBookList(UserPassesTestMixin, generic.ListView):
    """
    Return all borrowed book instances
    """
    model = BookInstance
    template_name = 'catalog/all_borrowed_book_list.html'
    paginate_by = 10

    def test_func(self):
        """
        Check if logged user is a librarian. Return False if not
        """
        librarian_group = Group.objects.filter(name='Librarian')[0]
        return librarian_group in self.request.user.groups.all()

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')

    def get_context_data(self):
        context = super(AllBorrowedBookList, self).get_context_data()
        context['page_title'] = 'All Borrowed Books'
        return context


def author_listing(request):
    # Get author queryset
    author_list = Author.objects.all()

    # Create paginator object instance
    paginator = Paginator(author_list, 4)

    # Get page number from GET request
    page_num = request.GET.get('page')

    # Inistantiate page object
    try:
        authors = paginator.page(page_num)
    except PageNotAnInteger:
        authors = paginator.page(1)
    except EmptyPage:
        authors = paginator.page(paginator.num_pages)

    return render(request, 'catalog/author_list.html', {
            'author_list': authors,
        })

class AboutView(generic.TemplateView):
    template_name = 'catalog/about.html'

    def get_context_data(self):
        context = super(AboutView, self).get_context_data()
        context['page_title'] = 'About'
        return context