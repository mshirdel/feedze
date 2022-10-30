import os
from feedze.settings.base import *  # noqa


SECRET_KEY = os.environ.get("SECRET_KEY", "")

DEBUG = False

ALLOWED_HOSTS = [
    host for host in os.environ.get("ALLOWED_HOSTS", "").split(",") if host
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ["POSTGRES_NAME"],
        "USER": os.environ["POSTGRES_USER"],
        "PASSWORD": os.environ["POSTGRES_PASSWORD"],
        "HOST": "db",
        "PORT": 5432,
    },
}
