import hashlib
import string
from abc import ABC, abstractmethod

BASE62_CHARS = string.digits + string.ascii_letters


class URLShortener(ABC):
    @abstractmethod
    def shorten_url(self, auto_increment_id): ...

    @abstractmethod
    def convert(self, auto_increment_id: int) -> str: ...


class URLShortenerBase62(URLShortener):
    def shorten_url(self, auto_increment_id):
        short_url = self.convert(auto_increment_id)
        return short_url

    def convert(self, number) -> str:
        if number == 0:
            return "0"

        base62 = ""
        while number:
            number, remainder = divmod(number, 62)
            base62 = BASE62_CHARS[remainder] + base62
        return base62


class URLShortenerSHA2(URLShortener):
    def shorten_url(self, auto_increment_id):
        short_url = self.convert(auto_increment_id)
        return short_url

    def convert(self, auto_increment_id: int) -> str:
        sha2_hash = hashlib.sha256()
        sha2_hash.update(str(auto_increment_id).encode("utf-8"))
        hash_hexadecimal = sha2_hash.hexdigest()
        return hash_hexadecimal[0:8]
