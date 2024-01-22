from django.urls import path
from . import views


urlpatterns = [
    path("", views.partner_portal, name="partner_portal"),
    path("partner-portal/<slug:slug>/", views.partner_portal, name="partner_portal"),
]