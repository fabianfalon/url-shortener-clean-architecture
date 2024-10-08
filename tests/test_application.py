import pytest
from expects import expect, equal

from src.infrastructure.shortener.shortener import URLShortenerSHA2
from src.infrastructure.storage.in_memory import InMemoryRepository
from src.infrastructure.storage.cache import InMemoryCacheRepository
from src.application.get_all_short_urls import GetAllShortUrls
from src.application.get_original_url import GetOriginalUrlUseCase
from src.application.create_short_url import CreateShortUrlUseCase
from tests.conftest import MOCK_ORIGINAL_URL, MOCK_SHORT_URL


class TestShortenerUrlUseCases:
    @pytest.mark.asyncio
    async def test_create_new_short_url(self):
        use_case = CreateShortUrlUseCase(
            url_repository=InMemoryRepository(),
            shorter=URLShortenerSHA2(),
            cache=InMemoryCacheRepository(),
        )
        url = await use_case.execute(original_url=MOCK_ORIGINAL_URL)
        expect(url).to(equal(MOCK_SHORT_URL))

    @pytest.mark.asyncio
    async def test_get_short_url(self):
        use_case = GetOriginalUrlUseCase(
            url_repository=InMemoryRepository(),
            cache=InMemoryCacheRepository(),
        )
        url = await use_case.execute(short_url=MOCK_SHORT_URL)
        expect(url).to(equal(MOCK_ORIGINAL_URL))

    @pytest.mark.asyncio
    async def test_get_all_short_url(self):
        use_case = GetAllShortUrls(
            url_repository=InMemoryRepository(),
        )
        url = await use_case.execute()
        expect(len(url)).to(equal(1))
