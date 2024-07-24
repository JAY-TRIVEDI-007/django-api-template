# ruff: noqa: E501
from .base import *  # noqa: F403
from .base import env

DEBUG = True

SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="Da71JRBrtu9IoVkgitcuw8DFOyTbX8SWv2BE8zYyDdvCe5SG6l30gHQHKwB2R55P",
)

ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]
