from pydantic import AnyHttpUrl, BaseModel


class UrlPayloadIn(BaseModel):
    url: AnyHttpUrl


class UrlResponseOut(BaseModel):
    url: AnyHttpUrl
