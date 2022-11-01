import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

env = os.environ.get("DJANGO_ENV")
settings_module = f"feedze.settings.{env}"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)

app = Celery("feedze")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.beat_schedule = {
    "update_feeds_task_periodically": {
        "task": "feed.tasks.update_feeds_task_periodically",
        "schedule": crontab(minute="*/5"),
        "args": (),
    },
}


class BaseTaskWithRetry(app.Task):
    autoretry_for = (Exception,)
    retry_kwargs = {"max_retries": 5}
    retry_backoff = True
