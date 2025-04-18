# import os
# import time
# from datetime import datetime
# from yt_dlp import YoutubeDL
# from pytube import YouTube
# from sqlmodel import Session

# from app.db.database import engine
# from app.models.history import DownloadHistory

# DOWNLOAD_DIR = "downloads"
# os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# def download_with_yt_dlp(url: str, fmt: str, quality: str) -> str:
#     timestamp = int(time.time())
#     ext = fmt if fmt != "mp3" else "mp3"
#     file_name = f"file_{timestamp}.{ext}"
#     file_path = os.path.join(DOWNLOAD_DIR, file_name)

#     ydl_opts = {
#         "outtmpl": file_path,
#         "quiet": True,
#         "merge_output_format": None if fmt == "mp3" else fmt,
#         "format": (
#             "bestaudio/best" if fmt == "mp3"
#             else f"bestvideo[height<={quality.replace('p', '')}]+bestaudio/best"
#         ),
#         "postprocessors": [
#             {
#                 "key": "FFmpegExtractAudio",
#                 "preferredcodec": "mp3",
#                 "preferredquality": "192",
#             }
#         ] if fmt == "mp3" else [],
#     }

#     with YoutubeDL(ydl_opts) as ydl:
#         ydl.download([url])

#     if not os.path.exists(file_path):
#         raise Exception("Download failed with yt-dlp.")

#     save_download_history(url)
#     return file_path

# def download_with_pytube(url: str, fmt: str, quality: str) -> str:
#     yt = YouTube(url)
#     stream = yt.streams.filter(progressive=True, file_extension=fmt).get_by_resolution(quality)
#     if not stream:
#         raise Exception(f"No stream available for {quality} in {fmt}")

#     timestamp = int(time.time())
#     file_name = f"file_{timestamp}.{fmt}"
#     file_path = os.path.join(DOWNLOAD_DIR, file_name)

#     stream.download(output_path=DOWNLOAD_DIR, filename=file_name)

#     if not os.path.exists(file_path):
#         raise Exception("Download failed with pytube.")

#     save_download_history(url)
#     return file_path

# def save_download_history(url: str):
#     history = DownloadHistory(
#         url=url,
#         status="Completed",
#         downloaded_at=datetime.now()
#     )
#     with Session(engine) as session:
#         session.add(history)
#         session.commit()


import os
import time
from datetime import datetime
from yt_dlp import YoutubeDL
from pytube import YouTube
from sqlmodel import Session
from app.db.database import engine
from app.models.history import DownloadHistory
#from app.services.tasks import download_video_task  # Celery task import

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def download_with_yt_dlp(url: str, fmt: str, quality: str) -> str:
    timestamp = int(time.time())
    ext = fmt if fmt != "mp3" else "mp3"
    file_name = f"file_{timestamp}.{ext}"
    file_path = os.path.join(DOWNLOAD_DIR, file_name)

    ydl_opts = {
        "outtmpl": file_path,
        "quiet": True,
        "merge_output_format": None if fmt == "mp3" else fmt,
        "format": (
            "bestaudio/best" if fmt == "mp3"
            else f"bestvideo[height<={quality.replace('p', '')}]+bestaudio/best"
        ),
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ] if fmt == "mp3" else [],
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    if not os.path.exists(file_path):
        raise Exception("Download failed with yt-dlp.")

    #save_download_history(url)
    return file_path

def download_with_pytube(url: str, fmt: str, quality: str) -> str:
    yt = YouTube(url)
    stream = yt.streams.filter(progressive=True, file_extension=fmt).get_by_resolution(quality)
    if not stream:
        raise Exception(f"No stream available for {quality} in {fmt}")

    timestamp = int(time.time())
    file_name = f"file_{timestamp}.{fmt}"
    file_path = os.path.join(DOWNLOAD_DIR, file_name)

    stream.download(output_path=DOWNLOAD_DIR, filename=file_name)

    if not os.path.exists(file_path):
        raise Exception("Download failed with pytube.")

    return file_path

def save_download_history(url: str, status: str):##for db
    history = DownloadHistory(
       url=url,
       status=status,
       downloaded_at=datetime.now()
    )
    with Session(engine) as session:
        session.add(history)
        session.commit()

# This is the actual background task that will be run by Celery.
# def download_video_task(url: str, fmt: str, quality: str):
#     try:
#         # Download using yt-dlp first
#         file_path = download_with_yt_dlp(url, fmt, quality)
#     except Exception:
#         # Fallback to pytube if yt-dlp fails
#         try:
#             file_path = download_with_pytube(url, fmt, quality)
#         except Exception as e:
#             save_download_history(url, "Failed")
#             raise Exception(f"Download failed: {str(e)}")
    
#     save_download_history(url, "Completed")
#     return file_path


# Changes Explained:
# Moved the download logic to Celery: The actual download is now part of the download_video_task function, which will run asynchronously in the background using Celery.

# History saving: The save_download_history function is still in place to save the history, but it is now called from the Celery task after a successful or failed download. This ensures that the download history is recorded properly even if the download happens asynchronously.

# Asynchronous execution: The Celery task will be executed asynchronously, and the FastAPI request will respond immediately with a "Download started" message.