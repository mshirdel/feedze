from celery import shared_task
from feed.feed_manager import FeedFetcher


@shared_task
def import_feed_task(url: str):
    FeedFetcher(url)
