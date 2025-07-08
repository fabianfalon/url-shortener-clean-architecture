from expects import be, expect, equal
from fastapi.testclient import TestClient
from starlette import status
from src.main import app
from tests.conftest import MOCK_ORIGINAL_URL, MOCK_SHORT_URL
from src.infrastructure.storage.in_memory import InMemoryRepository
from src.infrastructure.storage.cache import InMemoryCacheRepository
from src.infrastructure.storage.analytics_repository import InMemoryAnalyticsRepository
from src.delivery.api.dependencies import (
    mongo_repository,
    get_url_cache_memcached_repository,
    get_analytics_repository,
)
import pytest


# Sobrescribir la dependencia de mongo_repository por InMemoryRepository
@pytest.fixture(autouse=True)
def override_repo_dependency():
    repo = InMemoryRepository()
    cache = InMemoryCacheRepository()
    analytics = InMemoryAnalyticsRepository()
    app.dependency_overrides[mongo_repository] = lambda: repo
    app.dependency_overrides[get_url_cache_memcached_repository] = lambda: cache
    app.dependency_overrides[get_analytics_repository] = lambda: analytics
    yield
    app.dependency_overrides.clear()


class TestApi:
    client = TestClient(app)


class TestURLShortenerApi(TestApi):

    def test_create_short_url(self, mock_create_short_url_use_case):
        data = {"url": MOCK_ORIGINAL_URL}
        response = self.client.post("/shortener", json=data)
        expect(response.status_code).to(be(status.HTTP_200_OK))
        expect(response.json().get("url")).to(equal(f"http://localhost:5000/{MOCK_SHORT_URL}"))

    def test_get_original_url(self, mock_create_short_url_use_case, mock_get_original_url_use_case):
        data = {"url": MOCK_ORIGINAL_URL}
        self.client.post("/shortener", json=data)

        response = self.client.get(f"/{MOCK_SHORT_URL}")
        expect(response.json()).to(equal({"url": MOCK_ORIGINAL_URL}))
        expect(response.status_code).to(be(status.HTTP_200_OK))

    def test_get_all_short_urls(self, mock_create_short_url_use_case, mock_get_original_url_use_case):
        data = {"url": MOCK_ORIGINAL_URL}
        self.client.post("/shortener", json=data)

        response = self.client.get("/urls")
        expect(response.status_code).to(be(status.HTTP_200_OK))
        expect(len(response.json())).to(equal(1))
