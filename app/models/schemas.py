from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class DownloadRequest(BaseModel):
    url: str
    format: Optional[str] = "mp4"
    quality: Optional[str] = "720p"

class DownloadResponse(BaseModel):
    status: str
    message: str

class MetadataResponse(BaseModel):
    title: str
    duration: str
    views: Optional[int]
    likes: Optional[int]
    channel: str
    published_date: str
    thumbnail_url: str
    size: int


class HistoryResponse(BaseModel):
    url:str
    status:str
    downloaded_at:datetime

class Config:
    orm_mode=True