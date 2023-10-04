from django.urls import path
from . import views



app_name = "catalog"


urlpatterns = [
    path("", views.catalogView, name="list"),
    path("create-book", views.CreateBook, name="create_book"),
]