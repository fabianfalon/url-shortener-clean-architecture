from abc import ABC, abstractmethod
from typing import List, Optional

from src.domain.url import Url


class UrlRepository[T](ABC):
    """UrlRepository"""

    @abstractmethod
    async def save(self, url: Url) -> Url: ...

    @abstractmethod
    async def delete(self, url_id: str) -> None: ...

    @abstractmethod
    async def find_one(self, url_id: str) -> Optional[Url]: ...

    @abstractmethod
    async def find_all(self) -> List[Url]: ...

    @abstractmethod
    async def get_by_original_url(self, original_url) -> Url: ...

    @abstractmethod
    async def get_by_short_url(self, short_url) -> Url: ...
