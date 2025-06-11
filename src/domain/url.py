from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional, List

from .value_objects import OriginalUrl, ShortCode, UrlId
from .events import UrlShortenedEvent, UrlAccessedEvent, DomainEvent


class AggregateRoot(ABC):
    @abstractmethod
    def to_primitive(self) -> dict: ...

    @staticmethod
    @abstractmethod
    def from_primitive(raw_data: dict): ...


class Url(AggregateRoot):
    def __init__(
        self,
        url_id: UrlId,
        original_url: OriginalUrl,
        short_code: ShortCode,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ) -> None:
        self._id = url_id
        self._original_url = original_url
        self._short_code = short_code
        self._created_at = created_at if created_at else datetime.now()
        self._updated_at = updated_at if updated_at else datetime.now()
        self._access_count = 0
        self._events: List[DomainEvent] = []

    @property
    def id(self) -> UrlId:
        return self._id

    @property
    def original_url(self) -> OriginalUrl:
        return self._original_url

    @property
    def short_code(self) -> ShortCode:
        return self._short_code

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        return self._updated_at

    @property
    def access_count(self) -> int:
        return self._access_count

    def record_access(self) -> None:
        self._access_count += 1
        self._updated_at = datetime.now()
        self._events.append(
            UrlAccessedEvent(url_id=self._id, short_code=self._short_code)
        )

    def to_primitive(self) -> dict:
        return {
            "id": int(self._id),
            "url": str(self._original_url),
            "short_url": str(self._short_code),
            "created_at": self._created_at,
            "updated_at": self._updated_at,
            "access_count": self._access_count,
        }

    @staticmethod
    def from_primitive(raw_data: dict) -> "Url":
        return Url(
            url_id=UrlId(raw_data["id"]),
            original_url=OriginalUrl(raw_data["url"]),
            short_code=ShortCode(raw_data["short_url"]),
            created_at=raw_data["created_at"],
            updated_at=raw_data["updated_at"],
        )

    @classmethod
    def create(
        cls, url_id: int, original_url: OriginalUrl, short_code: ShortCode
    ) -> "Url":
        url = cls(
            url_id=UrlId(url_id), original_url=original_url, short_code=short_code
        )
        url._events.append(
            UrlShortenedEvent(
                url_id=url._id,
                original_url=url._original_url,
                short_code=url._short_code,
            )
        )
        return url

    def get_events(self) -> List[DomainEvent]:
        events = self._events.copy()
        self._events.clear()
        return events
