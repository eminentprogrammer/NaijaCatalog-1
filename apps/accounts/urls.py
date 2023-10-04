from django.urls import path
from . import views


urlpatterns = [
    path('', views.dashboard_view, name="dashboard"),
    path('sign-up/', views.signUp, name='signup'),
    path('sign-in/', views.signIn, name='signin'),
    path('sign-out/', views.signOut, name='signout'),
    path('search/', views.dashboard_search, name="dashboard_search"),
]
