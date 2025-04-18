from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class DownloadHistory(SQLModel, table=True):
    __tablename__="download_history"
    id: Optional[int] = Field(default=None, primary_key=True)
    url: str
    status: str
    downloaded_at: datetime
