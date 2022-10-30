from feedze.settings.base import *  # noqa

SECRET_KEY = "django-insecure-omd9rdz$vea#!d_!54rhq0w=g9==)xhk8b#goq0innp9)+mmb#"
JWT_SECRET_KEY = "$vea#!d_!54rhq0w=g9"

DEBUG = True

ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "feedze",
        "USER": "meysam",
        "PASSWORD": "pg123",
        "HOST": "localhost",
        "PORT": "5432",
    },
}

INSTALLED_APPS += ["debug_toolbar", "django_extensions"]  # noqa
MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]  # noqa
