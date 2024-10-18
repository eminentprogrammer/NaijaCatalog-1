from django.urls import path
from . import views


app_name = "catalog"


urlpatterns = [
    path("", views.catalog_view, name="catalog_view"),
    path("view/", views.list_books, name="listBook"),

    path("create-book", views.upload_book, name="create_book"),
    path("book/<slug:slug>/info", views.single_book_info, name="single_book_info"),
    path("book/<slug:slug>/edit", views.edit_book_info, name="edit_book_info"),
    path("book/<slug:slug>/delete", views.delete_book, name="delete_book"),

    path("search/", views.list_books, name="search_book_title"),
    path('advanced-search/', views.advanced_search, name="advanced_search"),
]