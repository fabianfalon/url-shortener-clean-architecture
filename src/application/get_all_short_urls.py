from typing import List

from src.domain.url import Url
from src.domain.url_repository import UrlRepository


class GetAllShortUrls:
    def __init__(self, url_repository: UrlRepository):
        self.repository = url_repository

    async def execute(self) -> List[Url]:
        urls = await self.repository.find_all()
        return urls
