from typing import List

from src.domain.url_repository import UrlRepository


class GetAllShortUrlsUseCase:
    def __init__(self, url_repository: UrlRepository):
        self._url_repository = url_repository

    async def execute(self) -> List[dict]:
        urls = await self._url_repository.find_all()
        return [url.to_primitive() for url in urls]
