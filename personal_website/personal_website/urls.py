"""
URL configuration for personal_website project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from Main import views
from Main.custom_admin import custom_admin_site
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.urls import re_path

# Custom error handlers
handler404 = 'Main.views.custom_404'
handler500 = 'Main.views.custom_500'

urlpatterns = [
    # Use the custom admin site
    path('4dm1n/', custom_admin_site.urls),
    path('', include('Main.urls'), name='home'),
    path('contact/', views.contact, name='contact'),
    path('articles/', include('Articles.urls', namespace='articles')),
    path('projects/', include('Projects.urls')),
    path('research/', include('Research.urls')),
]

# Serve media files in production if not using Cloudinary
if not settings.DEBUG and not getattr(settings, 'USE_CLOUDINARY', True):
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]

# Only in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
