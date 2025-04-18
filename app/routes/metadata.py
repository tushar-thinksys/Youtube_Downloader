from fastapi import APIRouter, HTTPException
from app.models.schemas import MetadataResponse
from app.services.metadata_extractor import extract_metadata

router = APIRouter()

@router.get("/metadata", response_model=MetadataResponse)
async def get_metadata(url: str):
    try:
        data = await extract_metadata(url)
        return MetadataResponse(**data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Metadata extraction failed: {str(e)}")
