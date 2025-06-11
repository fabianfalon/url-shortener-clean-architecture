import os
from abc import ABC
from typing import List, Optional
import logging

import motor.motor_asyncio

from src.config import settings
from src.domain.url import Url
from src.domain.url_repository import UrlRepository
from src.domain.value_objects import ShortCode, OriginalUrl


class AbstractMongoRepository(ABC):
    def __init__(self) -> None:
        self.client = motor.motor_asyncio.AsyncIOMotorClient(settings.mongo_url)
        self.database = self.client["url-shortener"]
        self.collection = self.database["urls"]


class MongoRepository(AbstractMongoRepository, UrlRepository):
    def __init__(self) -> None:
        super().__init__()
        self._logger = logging.getLogger(__name__)

    async def save(self, aggregate_root: Url) -> Url:
        """Save a new URL or update an existing one."""
        primitive_data = aggregate_root.to_primitive()
        self._logger.info(f"Saving URL with data: {primitive_data}")

        existing = await self.collection.find_one({"id": primitive_data["id"]})
        if existing:
            self._logger.info(f"Updating existing URL with id: {primitive_data['id']}")
            await self.collection.update_one(
                {"id": primitive_data["id"]}, {"$set": primitive_data}
            )
        else:
            self._logger.info(f"Inserting new URL with id: {primitive_data['id']}")
            await self.collection.insert_one(primitive_data)

        return Url(
            url_id=aggregate_root.id,
            original_url=aggregate_root.original_url,
            short_code=aggregate_root.short_code,
            created_at=aggregate_root.created_at,
            updated_at=aggregate_root.updated_at,
        )

    async def find_by_id(self, url_id: str) -> Optional[Url]:
        document = await self.collection.find_one({"id": int(url_id)})
        return self._create_url(document) if isinstance(document, dict) else None

    async def find_by_original_url(self, original_url: OriginalUrl) -> Optional[Url]:
        document = await self.collection.find_one({"url": str(original_url)})
        return self._create_url(document) if isinstance(document, dict) else None

    async def find_by_short_code(self, short_code: ShortCode) -> Optional[Url]:
        document = await self.collection.find_one({"short_url": str(short_code)})
        return self._create_url(document) if isinstance(document, dict) else None

    async def get_next_id(self) -> int:
        count = await self.collection.count_documents({})
        return count + 1

    async def find_all(self) -> List[Url]:
        urls = []
        async for doc in self.collection.find({}):
            urls.append(self._create_url(doc))
        self._logger.info(f"Total URLs found: {len(urls)}")
        return urls

    async def delete(self, url_id: str) -> None:
        await self.collection.delete_one({"id": int(url_id)})

    @staticmethod
    def _create_url(raw_data: dict) -> Url:
        return Url.from_primitive(raw_data)
