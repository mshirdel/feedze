import os

from celery import Celery
from django.conf import settings

env = os.environ.get("DJANGO_ENV")
settings_module = f"feedze.settings.{env}"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)

app = Celery("feedze")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
