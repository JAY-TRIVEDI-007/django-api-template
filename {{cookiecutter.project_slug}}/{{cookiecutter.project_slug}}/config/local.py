# ruff: noqa: E501
import os

from .base import *  # noqa: F403

DEBUG = True

# NOTE: All addresses included to expose the development server to private network
ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]

DATABASES["default"]["HOST"] = "127.0.0.1"

{% if cookiecutter.is_documentation_dev_only == 'y' %}
INSTALLED_APPS += ['drf_spectacular', 'api_docs']

REST_FRAMEWORK['DEFAULT_SCHEMA_CLASS'] = 'drf_spectacular.openapi.AutoSchema'

# Documentation
SPECTACULAR_SETTINGS = {
    'AUTHENTICATION_CLASSES': (
        {% if cookiecutter.authentication_method == 'token' %}
        'rest_framework.authentication.TokenAuthentication',
        {% endif %}
        {% if cookiecutter.authentication_method == 'jwt' %}
        'rest_framework.authentication.JWTAuthentication',
        {% endif %}
    ),
    'SWAGGER_UI_SETTINGS': {
        'persistAuthorization': True
    }
}
{% endif %}
CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOWED_ORIGINS = ['http://localhost:4200']
