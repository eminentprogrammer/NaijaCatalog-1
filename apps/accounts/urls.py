from django.urls import path
from . import views


urlpatterns = [
    path('', views.dashboard_redirect, name="dashboard"),
    path('login/', views.signIn, name='signin'),
    path('logout/', views.signOut, name='signout'),

    path('search/', views.dashboard_search, name="dashboard_search"),
    
    path("profile/update/", views.update_profile, name="update_profile"),
    path("password/update/", views.update_password, name="update_password"),
    path("password/reset/", views.reset_password, name="reset_password"),

    

    path('student/signup/', views.signUp, name='signup'),
    path('student/dashboard/', views.studentDashboard, name="student_dashboard"),
    path('institution/dashboard/', views.insitutionDashboard, name="institution_dashboard"),
    path('institution/signup/', views.institutionRegistration, name="institution_registration"),
]
