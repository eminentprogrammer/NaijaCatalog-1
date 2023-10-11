
Bad request
handler400 – django.conf.urls.handler400.

Permission Denied
handler403 – django.conf.urls.handler403.

Page Not Found
handler404 – django.conf.urls.handler404.

Internal Server Error
handler500 – django.conf.urls.handler500.

<>COPY AND PASTE INTO BASE PROJECT URLS<>

from django.conf.urls import handler400, handler403, handler404, handler500
from https import views

handler400 = views.handler400
handler403 = views.handler403
handler404 = views.handler404
handler500 = views.handler500
