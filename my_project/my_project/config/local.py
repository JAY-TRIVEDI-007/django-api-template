# ruff: noqa: E501
from .base import *  # noqa: F403
from .base import env

DEBUG = True

SECRET_KEY = env.get("DJANGO_SECRET_KEY", default="changethis")

# NOTE: All addresses included to expose the development server to private network
ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]
