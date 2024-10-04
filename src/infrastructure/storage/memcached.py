import memcache
from typing import Optional
from src.infrastructure.storage.cache import AbstractCacheRepository


class MemcachedRepository(AbstractCacheRepository):
    def __init__(self) -> None:
        self.client = memcache.Client(["url-shortener-memcached:11211"], debug=0)
        super().__init__()

    def set(self, key: str, value: str) -> None:
        self.client.set(key, value, time=3600)  # Cache for 1 hour

    def get(self, key: str) -> Optional[str]:
        value = self.client.get(key)
        return value