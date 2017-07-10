from django.conf.urls import url
from . import views

app_name = 'catalog'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^books/$', views.BookListView.as_view(), name='book_list'),
    url(r'^book/(?P<pk>[0-9]+)$', views.BookDetailView.as_view(), name='book_detail'),
    url(r'^authors/$', views.AuthorListView.as_view(), name='author_list'),
    url(r'^mybooks/$', views.BorrowedBookList.as_view(), name='my_borrowed_book_list'),
    url(r'^borrowed/$', views.AllBorrowedBookList.as_view(), name='all_borrowed_book_list'),
    url(r'^about/$', views.AboutView.as_view(), name='about'),
    # url(r'^contact/$', views.ContactView.as_view(), name='contact'),
    # url(r'^authors/$', views.author_listing, name='author_list'),
    # url(r'^author/(?P<pk>\d+)$', views.AuthorDetailView.as_view(), name='author_detail'),
]