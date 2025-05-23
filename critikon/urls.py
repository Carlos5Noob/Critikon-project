"""
URL configuration for critikon project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.views.generic import TemplateView

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', TemplateView.as_view(template_name='inicio.html'), name='inicio'), # template de inicio '/'
    path('admin/', admin.site.urls), # urls del admin page
    path('critikon/', include('app.urls')), # urls de la aplicación
    path('api/', include('api.urls')), # urls de la api
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')), # necesario para el login de la api
    path('accounts/', include('django.contrib.auth.urls')), # rutas para el login, logout y registration
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)