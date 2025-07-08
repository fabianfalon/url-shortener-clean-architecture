from src.domain.repositories.cache_repository import AbstractCacheRepository


class InMemoryCacheRepository(AbstractCacheRepository):
    mapping = {}

    def set(self, key, value):
        self.mapping[key] = value

    def get(self, key):
        return self.mapping.get(key, None)
