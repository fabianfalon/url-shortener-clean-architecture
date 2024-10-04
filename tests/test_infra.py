import json

import pytest
from pydantic import ValidationError

from src.infrastructure.dto.url_dto import UrlResponseOut
from src.infrastructure.shortener.shortener import URLShortenerBase62, URLShortenerSHA2
from expects import expect, equal


class TestInfrastructure:
    def test_shortener_base62(self):
        result = URLShortenerBase62().shorten_url(1000)
        expect(result).to(equal("g8"))

    def test_shortener_sha2(self):
        result = URLShortenerSHA2().shorten_url(1000)
        expect(result).to(equal("40510175"))

    def test_dto_url_out_ok(self):
        response = UrlResponseOut(url="http://localhost:8000/40510175")
        expect(response.model_dump_json()).to(equal('{"url":"http://localhost:8000/40510175"}'))

    def test_dto_url_out_ko(self):
        with pytest.raises(ValidationError) as error:
            UrlResponseOut(url="invalid-url")
        expect(
            json.loads(error.value.json())[0].get("msg")).to(
            equal("Input should be a valid URL, relative URL without a base")
        )
