from abc import ABC, abstractmethod
from typing import List, Optional

from src.domain.url import Url
from src.domain.value_objects import OriginalUrl, ShortCode, UrlId


class UrlRepository(ABC):
    @abstractmethod
    async def save(self, url: Url) -> Url:
        """Save a new URL or update an existing one"""
        ...

    @abstractmethod
    async def find_by_id(self, url_id: UrlId) -> Optional[Url]:
        """Find a URL by its ID"""
        ...

    @abstractmethod
    async def find_by_short_code(self, short_code: ShortCode) -> Optional[Url]:
        """Find a URL by its short code"""
        ...

    @abstractmethod
    async def find_by_original_url(self, original_url: OriginalUrl) -> Optional[Url]:
        """Find a URL by its original URL"""
        ...

    @abstractmethod
    async def find_all(self) -> List[Url]:
        """Get all URLs"""
        ...

    @abstractmethod
    async def delete(self, url_id: UrlId) -> None:
        """Delete a URL by its ID"""
        ...

    @abstractmethod
    async def get_next_id(self) -> int:
        """Get the next available ID for a new URL"""
        ...
