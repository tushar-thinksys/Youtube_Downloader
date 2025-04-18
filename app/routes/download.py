from fastapi import APIRouter, Depends, HTTPException
from app.models.schemas import DownloadRequest, DownloadResponse
#from app.services.downloader import download_with_yt_dlp, download_with_pytube
from app.utils.validators import is_valid_youtube_url,validate_video_constraints
from app.dependencies.auth import verify_api_key
from app.services.tasks import download_video_task
from app.dependencies.rate_limiter import rate_limiter

router = APIRouter()

@router.post("/download", response_model=DownloadResponse,dependencies=[Depends(verify_api_key),Depends(rate_limiter)])
async def download_video(request: DownloadRequest):
    if not is_valid_youtube_url(request.url):  # Validate before processing
        raise HTTPException(status_code=400, detail="Invalid YouTube URL")

    validate_video_constraints(request.url,request.format,request.quality) # if exception raise then stop otherwise proceed download

    download_video_task.delay(request.url, request.format, request.quality)

    '''try:
        file_path = await download_with_yt_dlp(request.url, request.format, request.quality)
    except Exception:
        try:
            file_path = await download_with_pytube(request.url, request.format, request.quality)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Download failed: {str(e)}")'''
    
    return DownloadResponse(status="success", message="Download scheduled")
