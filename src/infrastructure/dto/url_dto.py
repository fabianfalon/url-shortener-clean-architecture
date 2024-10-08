from typing import List

from pydantic import AnyHttpUrl, BaseModel


class UrlPayloadIn(BaseModel):
    url: AnyHttpUrl


class UrlResponseOut(BaseModel):
    url: AnyHttpUrl


class UrlOut(BaseModel):
    id: int
    short_url: str


class UrlListResponse(BaseModel):
    urls: List[UrlOut]
