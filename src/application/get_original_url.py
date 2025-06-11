from typing import Optional

from src.domain.url_repository import UrlRepository
from src.domain.value_objects import ShortCode
from src.infrastructure.events.event_bus_impl import InMemoryEventBus
from src.infrastructure.storage.cache import AbstractCacheRepository


class GetOriginalUrlUseCase:
    def __init__(
        self,
        url_repository: UrlRepository,
        cache: AbstractCacheRepository,
        event_bus: InMemoryEventBus,
    ):
        self._url_repository = url_repository
        self._cache = cache
        self._event_bus = event_bus

    async def execute(self, short_code: str) -> Optional[str]:
        """Retrieve the original URL for a given short code."""
        cached_url = self._cache.get(short_code)
        if cached_url:
            return cached_url

        short_code_vo = ShortCode(short_code)

        url = await self._url_repository.find_by_short_code(short_code_vo)

        if not url:
            return None

        # Record access and update
        url.record_access()
        await self._url_repository.save(url)

        # Publish events related to the URL access
        for event in url.get_events():
            await self._event_bus.publish(event)

        # Cache the result
        self._cache.set(short_code, str(url.original_url))

        return str(url.original_url)
