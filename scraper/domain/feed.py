from dataclasses import dataclass
from datetime import datetime
from time import mktime

from scraper.exceptions import FeedException


@dataclass
class Feed:
    title: str = None
    link: str = None
    published: str = None
    published_parsed: object = None
    updated: str = None
    updated_parsed: object = None
    image_url: str = None
    description: str = None

    def validate(self):
        if not self.title or len(self.title) == 0:
            raise FeedException("Feed title not provided")

    @property
    def published_datetime(self):
        if self.published_parsed:
            return datetime.utcfromtimestamp(mktime(self.published_parsed))

    @property
    def updated_datetime(self):
        if self.updated_parsed:
            return datetime.utcfromtimestamp(mktime(self.updated_parsed))
