from typing import List, Optional, Dict
from datetime import datetime
from pydantic import AnyHttpUrl, BaseModel


class UrlPayloadIn(BaseModel):
    url: AnyHttpUrl


class UrlResponseOut(BaseModel):
    url: AnyHttpUrl


class UrlOut(BaseModel):
    id: int
    short_url: str


class UrlListResponse(BaseModel):
    urls: List[Dict]

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}


class UrlStatsResponse(BaseModel):
    short_code: str
    url_id: int
    total_creations: int
    total_accesses: int
    last_accessed: Optional[datetime]
