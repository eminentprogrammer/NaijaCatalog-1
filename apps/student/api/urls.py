from django.urls import path
from . import views
from apps.catalogue.api.views import list_books


app_name = "student"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path('list-books/', list_books, name="list_books"),
]
