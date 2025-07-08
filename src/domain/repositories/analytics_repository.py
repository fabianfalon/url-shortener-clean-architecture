from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict


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
