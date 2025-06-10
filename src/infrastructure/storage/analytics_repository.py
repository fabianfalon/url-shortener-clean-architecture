from abc import ABC, abstractmethod
from datetime import datetime


class AnalyticsRepository(ABC):
    @abstractmethod
    def record_url_creation(
        self, url_id: int, original_url: str, short_code: str, created_at: datetime
    ) -> None:
        """Record when a URL is shortened"""
        pass

    @abstractmethod
    def record_url_access(
        self, url_id: int, short_code: str, accessed_at: datetime
    ) -> None:
        """Record when a URL is accessed"""
        pass


class InMemoryAnalyticsRepository(AnalyticsRepository):
    def __init__(self):
        self._url_creations = []
        self._url_accesses = []

    def record_url_creation(
        self, url_id: int, original_url: str, short_code: str, created_at: datetime
    ) -> None:
        self._url_creations.append(
            {
                "url_id": url_id,
                "original_url": original_url,
                "short_code": short_code,
                "created_at": created_at,
            }
        )

    def record_url_access(
        self, url_id: int, short_code: str, accessed_at: datetime
    ) -> None:
        self._url_accesses.append(
            {"url_id": url_id, "short_code": short_code, "accessed_at": accessed_at}
        )

    def get_url_creations(self):
        return self._url_creations

    def get_url_accesses(self):
        return self._url_accesses
