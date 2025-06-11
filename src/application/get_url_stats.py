from typing import Dict, Optional

from src.infrastructure.storage.analytics_repository import AnalyticsRepository


class GetUrlStatsUseCase:
    def __init__(self, analytics_repository: AnalyticsRepository):
        self._analytics_repository = analytics_repository

    async def execute(self, short_code: str) -> Optional[Dict]:
        return await self._analytics_repository.get_url_stats(short_code)
