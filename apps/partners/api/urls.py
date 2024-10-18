from django.urls import path
from . import views


urlpatterns = [
    path("", views.partners, name="partners"),
    path("<slug:slug>/info/", views.partnerInfo, name="partner_portal"),
    path("student/", views.student_view, name="student_view"),
    path("<slug:slug>/portal/", views.student_portal, name="student_portal"),
]