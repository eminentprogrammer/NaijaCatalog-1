from . import views
from django.conf import settings
from django.urls import path, re_path
from django.views.decorators.csrf import csrf_exempt



app_name="paystack"

urlpatterns = [

    re_path('verify-payment/(?P<order>[\w.@+-]+)/$', views.verify_payment, name='verify_payment'),

    re_path('failed-verification/(?P<order_id>[\w.@+-]+)/$', views.failure_redirect_view, name='failed_verification'),

    re_path('^successful-verification/(?P<order_id>[\w.@+-]+)/$', views.success_redirect_view, name='successful_verification'),

    path('failed-page/', views.TemplateView.as_view(template_name='paystack/failed-page.html'), name='failed_page'),
    
    path('success-page/', views.TemplateView.as_view(template_name='paystack/success-page.html'), name='success_page'),

    path('webhook/', csrf_exempt(views.webhook_view), name='webhook'),

]
