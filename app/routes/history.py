from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.db.database import get_session
from app.services.history_service import get_all_history
from app.models.schemas import HistoryResponse

router = APIRouter()

@router.get("/history",response_model=list[HistoryResponse])
def fetch_download_history(session: Session = Depends(get_session)):
    return get_all_history(session)
