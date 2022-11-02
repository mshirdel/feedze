from celery import shared_task
from feedze.celery import app as celery_app, BaseTaskWithRetry
from feed.feed_manager import FeedFetcher, FeedUpdater
from feed.models import Feed


@shared_task
def import_feed_task(url: str):
    FeedFetcher(url).fetch()


@celery_app.task
def update_feeds_task_periodically():
    for feed in Feed.objects.all().iterator(chunk_size=50):
        update_feed.delay(feed_id=feed.id)


@celery_app.task(bind=True, base=BaseTaskWithRetry)
def update_feed(bind, *, feed_id, **kwargs):
    feed = Feed.objects.get(id=feed_id)
    FeedUpdater(feed).update()
