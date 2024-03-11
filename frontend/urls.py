from django.contrib.sitemaps.views import sitemap
from django.urls import path
from . import views
from .sitemaps import Sitemap  # Import your sitemap class


sitemaps = {
    'sitemap': Sitemap,  # Add your sitemap class
}

urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('news/', views.news, name="news"),
    path('search/', views.search, name="search"),
    path('advanced/', views.advanced_search, name="advanced_search"),
    path('about-us/', views.about, name="about_us"),
    path('support/', views.support, name="support"),

    # Add other URL patterns as needed
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}),
    path('robots.txt', views.robots_view, name='robots_txt'),
    
    path('google-scholar-search/', views.google_scholar_search, name='google_scholar_search')
]