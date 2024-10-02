from src.domain.url import Url
from src.domain.url_repository import UrlRepository
from src.infrastructure.shortener.shortener import URLShortener
from src.infrastructure.storage.cache import AbstractCacheRepository


class CreateShortUrlUseCase:
    def __init__(
        self,
        url_repository: UrlRepository,
        shorter: URLShortener,
        cache: AbstractCacheRepository,
    ):
        self.repository = url_repository
        self.shorter = shorter
        self.cache = cache

    async def execute(self, original_url: str) -> str:
        cached_url = self.cache.get(original_url)
        if cached_url:
            return cached_url

        existing_url = await self.repository.get_by_original_url(original_url)
        if existing_url:
            self.cache.set(original_url, existing_url.short_url)
            return existing_url.short_url

        next_id = await self._get_next_url_id()
        short_url = self.shorter.shorten_url(next_id)
        url = Url(_id=next_id, url=original_url, short_url=short_url)
        await self.repository.save(url)
        self.cache.set(original_url, url.short_url)
        return url.short_url

    async def _get_next_url_id(self) -> int:
        count = await self.repository.find_all()
        return len(count) + 1
