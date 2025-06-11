from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Type, Callable

from .value_objects import OriginalUrl, ShortCode, UrlId


@dataclass
class DomainEvent: ...


@dataclass
class UrlShortenedEvent(DomainEvent):
    url_id: UrlId
    original_url: OriginalUrl
    short_code: ShortCode
    occurred_on: datetime = field(default_factory=datetime.now)


@dataclass
class UrlAccessedEvent(DomainEvent):
    url_id: UrlId
    short_code: ShortCode
    accessed_at: datetime = datetime.now()
    occurred_on: datetime = field(default_factory=datetime.now)


class EventBus:
    _handlers: List[callable] = []

    @classmethod
    def subscribe(cls, event_type: Type[DomainEvent], handler: Callable) -> None:
        pass

    @classmethod
    def publish(cls, event: DomainEvent):
        for handler in cls._handlers:
            handler(event)
