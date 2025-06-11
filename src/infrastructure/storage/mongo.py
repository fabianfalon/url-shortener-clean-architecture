import os
from abc import ABC
from typing import List, Optional

import motor.motor_asyncio

from src.domain.url import Url
from src.domain.url_repository import UrlRepository
from src.domain.value_objects import ShortCode, OriginalUrl

MONGO_URL = os.environ.get("MONGO_URL", "mongodb://url-shortener-mongodb:27017")


class AbstractMongoRepository(ABC):
    def __init__(self) -> None:
        self.client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
        self.database = self.client["url-shortener"]
        self.collection = self.database["urls"]


class MongoRepository(AbstractMongoRepository, UrlRepository):
    def __init__(self) -> None:
        super().__init__()

    async def save(self, aggregate_root: Url) -> Url:
        """Guarda el URL como dict serializado y retorna el objeto actualizado"""
        primitive_data = aggregate_root.to_primitive()
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
        return urls

    async def delete(self, url_id: str) -> None:
        await self.collection.delete_one({"id": int(url_id)})

    @staticmethod
    def _create_url(raw_data: dict) -> Url:
        return Url.from_primitive(raw_data)

    async def exists_by_short_code(self, short_code: str) -> bool:
        url = await self.collection.find_one({"short_url": short_code})
        return url is not None
