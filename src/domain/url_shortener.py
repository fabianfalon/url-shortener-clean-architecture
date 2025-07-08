from abc import ABC, abstractmethod


class URLShortener(ABC):
    @abstractmethod
    def shorten_url(self, auto_increment_id: int) -> str: ...

    @abstractmethod
    def convert(self, auto_increment_id: int) -> str: ...
