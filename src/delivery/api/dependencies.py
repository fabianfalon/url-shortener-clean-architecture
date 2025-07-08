from fastapi import Depends

from src.application.create_short_url import CreateShortUrlUseCase
from src.application.get_all_short_urls import GetAllShortUrlsUseCase
from src.application.get_original_url import GetOriginalUrlUseCase
from src.application.get_url_stats import GetUrlStatsUseCase
from src.domain.events import UrlAccessedEvent, UrlShortenedEvent
from src.domain.repositories.url_repository import UrlRepository
from src.infrastructure.events.event_bus_impl import InMemoryEventBus
from src.infrastructure.events.event_handlers import UrlEventHandlers
from src.infrastructure.shortener.shortener import URLShortener, URLShortenerSHA2
from src.infrastructure.storage.analytics_repository import MongoAnalyticsRepository
from src.infrastructure.storage.cache import (
    AbstractCacheRepository,
    InMemoryCacheRepository,
)
from src.infrastructure.storage.in_memory import InMemoryRepository
from src.infrastructure.storage.memcached import MemcachedRepository
from src.infrastructure.storage.mongo import MongoRepository


# Event Bus and Handlers
async def get_analytics_repository() -> MongoAnalyticsRepository:
    return MongoAnalyticsRepository()


async def get_event_bus() -> InMemoryEventBus:
    event_bus = InMemoryEventBus()
    analytics_repository = await get_analytics_repository()
    url_event_handlers = UrlEventHandlers(analytics_repository)

    # Subscribe event handlers
    event_bus.subscribe(UrlShortenedEvent, url_event_handlers.handle_url_shortened)
    event_bus.subscribe(UrlAccessedEvent, url_event_handlers.handle_url_accessed)

    return event_bus


async def get_shortener() -> URLShortener:
    return URLShortenerSHA2()


async def get_url_cache_repository() -> AbstractCacheRepository:
    return InMemoryCacheRepository()


async def get_url_cache_memcached_repository() -> AbstractCacheRepository:
    return MemcachedRepository()


async def in_memory_repository() -> UrlRepository:
    return InMemoryRepository()


async def mongo_repository() -> UrlRepository:
    return MongoRepository()


async def create_short_url_use_case(
    url_repository: UrlRepository = Depends(mongo_repository),
    shorter: URLShortener = Depends(get_shortener),
    cache: AbstractCacheRepository = Depends(get_url_cache_repository),
    event_bus: InMemoryEventBus = Depends(get_event_bus),
) -> CreateShortUrlUseCase:
    return CreateShortUrlUseCase(
        url_repository=url_repository, shorter=shorter, cache=cache, event_bus=event_bus
    )


async def get_original_url_use_case(
    url_repository: UrlRepository = Depends(mongo_repository),
    cache: AbstractCacheRepository = Depends(get_url_cache_memcached_repository),
    event_bus: InMemoryEventBus = Depends(get_event_bus),
) -> GetOriginalUrlUseCase:
    return GetOriginalUrlUseCase(
        url_repository=url_repository, cache=cache, event_bus=event_bus
    )


async def get_all_short_urls_use_case(
    url_repository: UrlRepository = Depends(mongo_repository),
) -> GetAllShortUrlsUseCase:
    return GetAllShortUrlsUseCase(url_repository=url_repository)


async def get_url_stats_use_case(
    analytics_repository: MongoAnalyticsRepository = Depends(get_analytics_repository),
) -> GetUrlStatsUseCase:
    return GetUrlStatsUseCase(analytics_repository)
