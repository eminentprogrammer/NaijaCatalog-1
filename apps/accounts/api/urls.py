from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.signIn, name='signin'),
    path('logout/', views.signOut, name='signout'),
    path('student/signup/', views.signUp, name='signup'),
    
    path("profile/update/", views.update_profile, name="update_profile"),
    path("password/update/", views.update_password, name="update_password"),
    path("password/reset/", views.reset_password, name="reset_password"),

    path('dashboard/', views.dashboard, name="dashboard_view"),
    path('dashboard/', views.dashboard_redirect, name="dashboard"),

    path('institution/signup/', views.institutionRegistration, name="institution_registration"),
]
