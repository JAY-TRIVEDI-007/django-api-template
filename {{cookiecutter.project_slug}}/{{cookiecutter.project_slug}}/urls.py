"""
URL configuration for {{cookiecutter.project_slug}} project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/auth/", include("djoser.urls.base")),
{% if cookiecutter.authentication_method == 'token' %}
    path("api/auth/", include("djoser.urls.authtoken")),
{% endif %}
{% if cookiecutter.authentication_method == 'jwt' %}
    path("api/auth/", include("djoser.urls.jwt"))
{% endif %}
{% if cookiecutter.is_documentation_dev_only == 'n' %}
    path("", include("api_docs.urls"))
{% endif %}
]
{% if cookiecutter.is_documentation_dev_only == 'y' %}
if settings.DEBUG:
    urlpatterns += [path("", include("api_docs.urls"))]
{% endif %}