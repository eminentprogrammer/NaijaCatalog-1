from django.urls import path
from . import views


app_name = "catalog"


urlpatterns = [
    path("", views.catalogView, name="list"),
    path("bookinfo/<slug:slug>/", views.single_book_info, name="single_book_info"),
    path("create-book", views.CreateBook, name="create_book"),
]