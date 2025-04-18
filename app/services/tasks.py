# # app/services/tasks.py
# from app.services.downloader import download_with_yt_dlp, download_with_pytube
# from app.db.database import SessionLocal
# from app.models.history import DownloadHistory
# from celery import shared_task
# from datetime import datetime

# @shared_task
# def download_video_task(url: str, format: str = "mp4", quality: str = "720p"):
#     try:
#         file_path = download_with_yt_dlp(url, format, quality)
#     except Exception:
#         file_path = download_with_pytube(url, format, quality)
    
#     # Save history to DB (sync way)
#     db = SessionLocal()
#     history = DownloadHistory(
#         url=url,
#         status="Completed",
#         downloaded_at=datetime.utcnow()
#     )
#     db.add(history)
#     db.commit()
#     db.close()
    
#     return "Download completed"

# from celery import Celery
# from app.services.downloader import download_with_yt_dlp, download_with_pytube

# celery_app = Celery(
#     "worker",
#     broker="redis://localhost:6379/0",
#     backend="redis://localhost:6379/0"
# )

# @celery_app.task
# def download_video_task(url: str, format: str, quality: str):
#     try:
#         download_with_yt_dlp(url, format, quality)
#     except Exception:
#         try:
#             download_with_pytube(url, format, quality)
#         except Exception as e:
#             print(f"Fallback failed: {str(e)}")


import os
from celery import Celery
#from app.services.downloader import download_with_yt_dlp, download_with_pytube#, save_download_history
from app.services.downloader import download_with_yt_dlp, download_with_pytube, save_download_history
from dotenv import load_dotenv

load_dotenv()

celery_app = Celery(
    "worker",
    #broker="redis://localhost:6379/0",
    #backend="redis://localhost:6379/0"
    broker=os.getenv("REDIS_BROKER_URL","redis://localhost:6379/0"),
    backend=os.getenv("REDIS_BROKER_URL","redis://localhost:6379/0")
)

@celery_app.task
def download_video_task(url: str, format: str, quality: str):
    try:
        download_with_yt_dlp(url, format, quality)
        save_download_history(url, "Completed")
    except Exception:
        try:
            download_with_pytube(url, format, quality)
            save_download_history(url, "Completed")
        except Exception as e:
            save_download_history(url, f"Failed: {str(e)}")
            print(f"Fallback failed: {str(e)}")
