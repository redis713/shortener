from pydantic import BaseModel, HttpUrl
from typing import List
from datetime import datetime

class URLCreate(BaseModel):
    original_url: HttpUrl

class URLResponse(BaseModel):
    short_code: str

class URLInfo(BaseModel):
    original_url: str
    short_code: str
    clicks: int
    created_at: datetime
    expires_at: datetime

class URLList(BaseModel):
    urls: List[URLInfo]
