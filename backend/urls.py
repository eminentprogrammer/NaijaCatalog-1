from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls import i18n
from django.conf.urls import handler400, handler403, handler404, handler500
from https import views

admin.site.site_header = "Naija Catalog Admin"
admin.site.site_title = "Naija Catalog Portal"
admin.site.index_title = "Welcome to Naija Catalog Portal"
# admin.site.site_url = "/"

handler400 = views.handler400
handler403 = views.handler403
handler404 = views.handler404
handler500 = views.handler500



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('frontend.urls')),
    path('user/', include('apps.accounts.api.urls')),
    path('student/', include("apps.student.api.urls")),
    path('partners/', include("apps.partners.api.urls")),
    path('catalog/', include("apps.catalogue.api.urls")),

    path('blog/', include("blog.urls")),
    
    path('i18n/', include(i18n)),
    path('health/', include('health_check.urls')),
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# settings.DEBUG = False