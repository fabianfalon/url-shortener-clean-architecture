from typing import List, Dict
import logging

from src.domain.url_repository import UrlRepository


class GetAllShortUrlsUseCase:
    def __init__(self, url_repository: UrlRepository):
        self._url_repository = url_repository
        self._logger = logging.getLogger(__name__)

    async def execute(self) -> List[Dict]:
        self._logger.info("Getting all short URLs")
        urls = await self._url_repository.find_all()
        unique_urls = {
            str(url.short_code): {
                "id": int(url.id),
                "url": str(url.original_url),
                "short_code": str(url.short_code),
                "created_at": url.created_at,
                "updated_at": url.updated_at,
                "access_count": url.access_count,
            }
            for url in urls
        }
        return list(unique_urls.values())
