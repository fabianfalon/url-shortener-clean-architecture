from src.domain.url import Url
from src.domain.url_repository import UrlRepository
from src.domain.value_objects import OriginalUrl, ShortCode
from src.infrastructure.events.event_bus_impl import InMemoryEventBus
from src.infrastructure.shortener.shortener import URLShortener
from src.infrastructure.storage.cache import AbstractCacheRepository


class CreateShortUrlUseCase:
    def __init__(
        self,
        url_repository: UrlRepository,
        shorter: URLShortener,
        cache: AbstractCacheRepository,
        event_bus: InMemoryEventBus,
    ):
        self._url_repository = url_repository
        self._shorter = shorter
        self._cache = cache
        self._event_bus = event_bus

    async def execute(self, original_url: str) -> str:
        cached_url = self._cache.get(original_url)
        if cached_url:
            return cached_url

        original_url_vo = OriginalUrl(original_url)
        existing_url = await self._url_repository.find_by_original_url(original_url_vo)
        if existing_url:
            self._cache.set(original_url, str(existing_url.short_code))
            return str(existing_url.short_code)

        # Generate short code
        next_id = await self._url_repository.get_next_id()
        short_code = ShortCode(self._shorter.shorten_url(next_id))

        # Create URL aggregate
        url = Url.create(
            url_id=next_id, original_url=original_url_vo, short_code=short_code
        )

        # Save to repository
        saved_url = await self._url_repository.save(url)

        for event in saved_url.get_events():
            self._event_bus.publish(event)

        self._cache.set(original_url, str(saved_url.short_code))
        return str(saved_url.short_code)
