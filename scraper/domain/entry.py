from dataclasses import dataclass
from datetime import datetime
from time import mktime


@dataclass
class Entry:
    title: str = None
    link: str = None
    author: str = None
    published: str = None
    summary: str = None
    content: str = None
    published_parsed: object = None

    @property
    def published_datetime(self):
        if self.published_parsed:
            return datetime.utcfromtimestamp(mktime(self.published_parsed))
