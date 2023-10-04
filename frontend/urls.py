from django.urls import path
from . import views


urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('search/', views.search, name="search"),
    path('google-scholar-search/', views.google_scholar_search, name='google_scholar_search'),
    # Add other URL patterns as needed
]