import logging
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, Optional

import motor.motor_asyncio

from src.config import settings


class AnalyticsRepository(ABC):
    @abstractmethod
    def record_url_creation(
        self, url_id: int, original_url: str, short_code: str, created_at: datetime
    ) -> None:
        """Record when a URL is shortened"""
        pass

    @abstractmethod
    def record_url_access(
        self, url_id: int, short_code: str, accessed_at: datetime
    ) -> None:
        """Record when a URL is accessed"""
        pass

    @abstractmethod
    async def get_url_stats(self, short_code: str) -> Dict:
        """Get URL statistics"""
        pass


class InMemoryAnalyticsRepository(AnalyticsRepository):
    def __init__(self):
        self._url_creations = []
        self._url_accesses = []

    def record_url_creation(
        self, url_id: int, original_url: str, short_code: str, created_at: datetime
    ) -> None:
        self._url_creations.append(
            {
                "url_id": url_id,
                "original_url": original_url,
                "short_code": short_code,
                "created_at": created_at,
            }
        )

    def record_url_access(
        self, url_id: int, short_code: str, accessed_at: datetime
    ) -> None:
        self._url_accesses.append(
            {"url_id": url_id, "short_code": short_code, "accessed_at": accessed_at}
        )

    def get_url_creations(self):
        return self._url_creations

    def get_url_accesses(self):
        return self._url_accesses

    async def get_url_stats(self, short_code: str) -> Dict:
        # Implementation of get_url_stats method for InMemoryAnalyticsRepository
        # This method is not implemented in the InMemoryAnalyticsRepository
        raise NotImplementedError(
            "get_url_stats method is not implemented in InMemoryAnalyticsRepository"
        )


class MongoAnalyticsRepository(AnalyticsRepository):
    def __init__(self):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(settings.mongo_url)
        self.database = self.client["url-shortener"]
        self.collection = self.database["analytics"]
        self._logger = logging.getLogger(__name__)

    async def record_url_creation(
        self, url_id: int, original_url: str, short_code: str, created_at: datetime
    ) -> None:
        try:
            self._logger.info(f"Recording URL creation for short_code: {short_code}")
            await self.collection.insert_one(
                {
                    "type": "url_creation",
                    "url_id": url_id,
                    "original_url": original_url,
                    "short_code": short_code,
                    "created_at": created_at,
                }
            )
            self._logger.info(
                f"URL creation recorded successfully for short_code: {short_code}"
            )
        except Exception as e:
            self._logger.error(f"Error recording URL creation: {str(e)}")
            raise

    async def record_url_access(
        self, url_id: int, short_code: str, accessed_at: datetime
    ) -> None:
        try:
            self._logger.info(f"Recording URL access for short_code: {short_code}")
            await self.collection.insert_one(
                {
                    "type": "url_access",
                    "url_id": url_id,
                    "short_code": short_code,
                    "accessed_at": accessed_at,
                }
            )
            self._logger.info(
                f"URL access recorded successfully for short_code: {short_code}"
            )
        except Exception as e:
            self._logger.error(f"Error recording URL access: {str(e)}")
            raise

    async def get_url_stats(self, short_code: str) -> Optional[Dict]:
        try:
            self._logger.info(f"Getting stats for short_code: {short_code}")

            # Primero obtenemos el url_id asociado al short_code
            url_doc = await self.collection.find_one(
                {"short_code": short_code},
                sort=[("created_at", -1)],  # Obtenemos el más reciente
            )

            if not url_doc:
                self._logger.warning(f"No documents found for short_code: {short_code}")
                return None

            url_id = url_doc["url_id"]
            self._logger.info(f"Found url_id: {url_id} for short_code: {short_code}")

            # Agregamos índices para mejorar el rendimiento si no existen
            await self.collection.create_index("short_code")
            await self.collection.create_index("url_id")
            await self.collection.create_index("type")

            # Obtenemos las estadísticas
            stats = await self.collection.aggregate(
                [
                    {"$match": {"url_id": url_id}},
                    {
                        "$group": {
                            "_id": "$type",
                            "count": {"$sum": 1},
                            "last_occurrence": {
                                "$max": {
                                    "$cond": [
                                        {"$eq": ["$type", "url_access"]},
                                        "$accessed_at",
                                        "$created_at",
                                    ]
                                }
                            },
                        }
                    },
                ]
            ).to_list(length=None)

            self._logger.info(f"Aggregation results: {stats}")

            total_creations = 0
            total_accesses = 0
            last_accessed = None

            for stat in stats:
                if stat["_id"] == "url_creation":
                    total_creations = stat["count"]
                elif stat["_id"] == "url_access":
                    total_accesses = stat["count"]
                    last_accessed = stat["last_occurrence"]

            result = {
                "short_code": short_code,
                "url_id": url_id,
                "total_creations": total_creations,
                "total_accesses": total_accesses,
                "last_accessed": last_accessed,
            }

            self._logger.info(f"Final stats result: {result}")
            return result

        except Exception as e:
            self._logger.error(f"Error getting URL stats: {str(e)}")
            raise
