"""BookWeb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from django.conf.urls import url, handler404, handler400, handler403, handler500
from django.conf import settings
from django.views.static import serve

path_to_error = 'books.views.error_4xx'

handler404 = path_to_error
handler400 = path_to_error
handler403 = path_to_error
handler500 = 'books.views.error_500'

urlpatterns = [
    path('', include('books.urls')),
    path('panel-administratora/', admin.site.urls, name='admin_panel'),
    # path('panel-administratora/doc/', include('django.contrib.admindocs.urls')),
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {
           'document_root': settings.MEDIA_ROOT,
        }),
    ]