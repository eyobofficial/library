from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from .models import Book, BookInstance, Genre, Author, Language
from .forms import RenewalForm

import datetime

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

class AuthorDetailView(generic.DetailView):
    model = Author 

    def get_context_data(self, *args, **kwargs):
        context = super(AuthorDetailView, self).get_context_data()
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

class AddAuthorView(PermissionRequiredMixin, CreateView):
    permission_required = ('catalog.return_bookinstance')
    template_name = 'catalog/add_author.html'
    success_url = '/catalog/authors/'
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']


class UpdateAuthorView(PermissionRequiredMixin, UpdateView):
    permission_required = 'catalog.return_bookinstance'
    template_name = 'catalog/edit_author.html'
    success_url = '/catalog/authors/'
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']

    def get_context_data(self):
        context = super(UpdateAuthorView, self).get_context_data()
        context['page_title'] = 'Authors'
        return context 

class RegisterationView(FormView):
    form_class = UserCreationForm
    template_name = 'catalog/register.html'
    success_url = '/catalog/'

        
    def get(self, *args, **kwargs):      
        if self.request.user.is_authenticated:
            return redirect('catalog:index')
        return super(RegisterationView, self).get(*args, **kwargs)

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')

        user = authenticate(username=username, password=password)

        if user is not None and user.is_active:
            login(self.request, user)
            return redirect('catalog:index')
        return super(RegisterationView, self).form_valid(form)

@permission_required('catalog.return_bookinstance')
def renew_book(request, pk):
    """
    Renew borrowed bookInstance due_back
    """
    form_class = RenewalForm
    template_name = 'catalog/book_renewal.html'
    book_copy = get_object_or_404(BookInstance, pk=pk)

    if request.method == 'POST':
        form = form_class(request.POST)

        if form.is_valid():
            renewal_date = form.cleaned_data['renewal_date']
            book_copy.due_back = renewal_date
            book_copy.save()

            return redirect('/catalog/borrowed/')
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = form_class(initial={'renewal_date': proposed_renewal_date})
    return render(request, template_name, {
           'form': form,
           'copy': book_copy,
           })

class AuthorCreate(PermissionRequiredMixin, CreateView):
    permission_required = (('catalog.return_bookinstance'),)
    model = Author 
    fields = '__all__'
    template_name_suffix = '_create' 

class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = (('catalog.return_bookinstance'),)
    model = Author
    fields = '__all__'
    template_name_suffix = '_update'

class AuthorDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'catalog.return_bookinstance'
    model = Author 
    success_url = reverse_lazy('catalog:author_list')
