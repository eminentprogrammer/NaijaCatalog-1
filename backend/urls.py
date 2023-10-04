from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls import i18n

urlpatterns = [
    path('', include('frontend.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path("catalog/", include("apps.catalogue.urls")),
    path("i18n/", include(i18n)),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

