from dataclasses import dataclass
from urllib.parse import urlparse


@dataclass(frozen=True)
class OriginalUrl:
    value: str

    def __post_init__(self):
        self._validate_url()

    def _validate_url(self):
        if not self.value:
            raise ValueError("URL cannot be empty")

        try:
            result = urlparse(self.value)
            if not all([result.scheme, result.netloc]):
                raise ValueError("Invalid URL format")
        except Exception as e:
            raise ValueError(f"Invalid URL: {str(e)}")

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class ShortCode:
    value: str

    def __post_init__(self):
        self._validate_short_code()

    def _validate_short_code(self):
        if not self.value:
            raise ValueError("Short code cannot be empty")

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class UrlId:
    value: int

    def __post_init__(self):
        if self.value < 0:
            raise ValueError("URL ID must be a positive number")

    def __int__(self) -> int:
        return self.value
