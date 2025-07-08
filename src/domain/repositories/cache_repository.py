from abc import ABC, abstractmethod
from typing import Optional


class AbstractCacheRepository(ABC):
    @abstractmethod
    def set(self, key: str, value: str) -> None: ...

    @abstractmethod
    def get(self, key: str) -> Optional[str]: ...
