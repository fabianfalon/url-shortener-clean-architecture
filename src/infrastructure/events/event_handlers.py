import logging

from src.domain.events import UrlShortenedEvent, UrlAccessedEvent
from src.infrastructure.storage.analytics_repository import AnalyticsRepository


class UrlEventHandlers:
    def __init__(self, analytics_repository: AnalyticsRepository):
        self._analytics_repository = analytics_repository
        self._logger = logging.getLogger(__name__)

    def handle_url_shortened(self, event: UrlShortenedEvent) -> None:
        """Handle URL shortened event"""
        try:
            self._analytics_repository.record_url_creation(
                url_id=int(event.url_id),
                original_url=str(event.original_url),
                short_code=str(event.short_code),
                created_at=event.occurred_on,
            )
            self._logger.info(f"URL shortened event recorded: {event.short_code}")
        except Exception as e:
            self._logger.error(f"Error handling URL shortened event: {str(e)}")

    def handle_url_accessed(self, event: UrlAccessedEvent) -> None:
        """Handle URL accessed event"""
        try:
            self._analytics_repository.record_url_access(
                url_id=int(event.url_id),
                short_code=str(event.short_code),
                accessed_at=event.accessed_at,
            )
            self._logger.info(f"URL accessed event recorded: {event.short_code}")
        except Exception as e:
            self._logger.error(f"Error handling URL accessed event: {str(e)}")
