from django.urls import path
from . import views


urlpatterns = [
    path('', views.dashboard_view, name="dashboard"),
    path('register/', views.signUp, name='signup'),
    path('login/', views.signIn, name='signin'),
    path('logout/', views.signOut, name='signout'),
    path('search/', views.dashboard_search, name="dashboard_search"),
]
