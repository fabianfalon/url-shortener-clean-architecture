from typing import List, Optional

from src.domain.repositories.url_repository import UrlRepository
from src.domain.url import Url


class InMemoryRepository(UrlRepository):
    def delete(self, course_id: str) -> None:
        print("mock delete")

    _urls: List[Url] = []

    async def save(self, url: Url) -> None:
        self._urls.append(url)

    async def find_by_id(self, url_id: str) -> Optional[Url]:
        return next(filter(lambda x: (x.id == url_id), self._urls), None)

    async def find_all(self) -> List[Url]:
        return self._urls

    async def find_by_original_url(self, original_url: str) -> Optional[Url]:
        return next(
            filter(lambda x: (x.original_url == original_url), self._urls), None
        )

    async def find_by_short_code(self, short_url: str) -> Optional[Url]:
        return next(filter(lambda x: (x.short_code == short_url), self._urls), None)

    async def get_next_id(self) -> int:
        return len(self._urls) + 1

    def clear(self):
        self._urls = []
