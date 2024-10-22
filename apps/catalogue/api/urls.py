from django.urls import path
from .views import *


app_name = "catalog"


urlpatterns = [
    path("", viewCatalog.as_view(), name="catalog_view"),

    path("view/", list_books, name="listBook"),

    path("create-book", UploadBook.as_view(), name="create_book"),
    path("book/<int:pk>/edit", EditBook.as_view(), name="edit_book_info"),

    path("book/<slug:slug>/info", single_book_info, name="single_book_info"),
    
    path("book/<int:pk>/delete", delete_book, name="delete_book"),

    path("search/", list_books, name="search_book_title"),
    path('advanced-search/', advanced_search, name="advanced_search"),
]