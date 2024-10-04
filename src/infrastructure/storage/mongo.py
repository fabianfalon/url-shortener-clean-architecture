import os
from abc import ABC
from typing import Dict, List, Optional

import motor.motor_asyncio

from src.domain.url import AggregateRoot, Url
from src.domain.url_repository import UrlRepository

MONGO_URL = os.environ.get("MONGO_URL", "mongodb://url-shortener-mongodb:27017")


class AbstractMongoRepository(ABC):
    def __init__(self) -> None:
        self.client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
        self.database = self.client["url-shortener"]
        self.collection = self.database["urls"]

    async def save(self, aggregate_root: AggregateRoot) -> None:
        document = aggregate_root.to_primitive()
        document["id"] = int(document["id"]) + 1
        await self.collection.insert_one(aggregate_root.to_primitive())


class MongoRepository(AbstractMongoRepository, UrlRepository):
    def __init__(self) -> None:
        super().__init__()

    async def find_one(self, url_id: str) -> Optional[Url]:
        document = await self.collection.find_one({"id": url_id})
        return self._create_url(document)

    async def find_all(self) -> List[Url]:
        urls = []
        async for url in self.collection.find({}):
            urls.append(self._create_url(url))
        return urls

    async def get_by_original_url(self, original_url: str) -> Optional[Url]:
        url = await self.collection.find_one({"url": original_url})
        return self._create_url(dict(url)) if url else None

    async def get_by_short_url(self, short_url: str) -> Optional[Url]:
        url = await self.collection.find_one({"short_url": short_url})
        return self._create_url(dict(url)) if url else None

    @staticmethod
    def _create_url(raw_data: Dict) -> Url:
        return Url.from_primitive(raw_data)

    async def delete(self, url_id: str) -> None:  # Noncompliance - method is empty
        pass
