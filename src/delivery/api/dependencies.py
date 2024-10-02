from fastapi import Depends

from src.application.get_original_url import GetOriginalUrlUseCase
from src.domain.url_repository import UrlRepository
from src.infrastructure.shortener.shortener import URLShortener, URLShortenerSHA2
from src.infrastructure.storage.cache import (
    AbstractCacheRepository,
    InMemoryCacheRepository,
)
from src.infrastructure.storage.in_memory import InMemoryRepository
from src.application.create_short_url import CreateShortUrlUseCase


async def get_shortener() -> URLShortener:
    return URLShortenerSHA2()


async def get_url_cache_repository() -> AbstractCacheRepository:
    return InMemoryCacheRepository()


async def in_memory_repository() -> UrlRepository:
    return InMemoryRepository()


async def get_url_shortener_use_case(
    url_repository: UrlRepository = Depends(in_memory_repository),
    shorter: URLShortener = Depends(get_shortener),
    cache: AbstractCacheRepository = Depends(get_url_cache_repository),
) -> CreateShortUrlUseCase:
    return CreateShortUrlUseCase(
        url_repository=url_repository, shorter=shorter, cache=cache
    )

async def get_original_url_use_case(
    url_repository: UrlRepository = Depends(in_memory_repository),
    cache: AbstractCacheRepository = Depends(get_url_cache_repository),
) -> GetOriginalUrlUseCase:
    return GetOriginalUrlUseCase(url_repository=url_repository, cache=cache)