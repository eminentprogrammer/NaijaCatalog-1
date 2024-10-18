from django.contrib.sitemaps.views import sitemap
from django.urls import path
from . import views
from .sitemaps import Sitemap  # Import your sitemap class
from apps.catalogue.api.views import search, advanced_search, google_scholar_search


sitemaps = {
    'sitemap': Sitemap,  # Add your sitemap class
}

urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('search/', search, name="search"),
    path('advanced/', advanced_search, name="advanced_search"),
    path('about-us/', views.about, name="about_us"),
    path('support/', views.support, name="support"),

    # Add other URL patterns as needed
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}),
    path('robots.txt', views.robots_view, name='robots_txt'),
    
    path('google-scholar-search/', google_scholar_search, name='google_scholar_search')
]