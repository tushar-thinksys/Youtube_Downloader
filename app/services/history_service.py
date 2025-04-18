from sqlmodel import Session, select
from app.models.history import DownloadHistory

def get_all_history(session: Session):
    statement = select(DownloadHistory).order_by(DownloadHistory.downloaded_at.desc())
    return session.exec(statement).all()
