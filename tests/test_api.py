from expects import be, expect, equal
from fastapi.testclient import TestClient
from starlette import status
from src.main import app
from tests.conftest import MOCK_ORIGINAL_URL, MOCK_SHORT_URL


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