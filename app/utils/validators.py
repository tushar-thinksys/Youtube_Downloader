import os
import re#for regex
from fastapi import HTTPException
from yt_dlp import YoutubeDL
from app.services.downloader import save_download_history
from dotenv import load_dotenv

load_dotenv()

def is_valid_youtube_url(url: str) -> bool:
    # Check if the URL contains more than one 'http://' or 'https://'
    if url.count("http://") > 1 or url.count("https://") > 1:
        return False
    
    # Check if the URL contains more than one 'www.'
    if url.count("www.") > 1:
        return False

    # Regex pattern to match valid YouTube URLs with various formats
    youtube_pattern = (
        r'^(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/'
        r'(watch\?v=|(?:v|e(?:mbed)?)\/|.*[?&]v=|.*[?&]embed\/|.*\/)([a-zA-Z0-9_-]{11})'
    )
    
    # Ensure it matches the valid YouTube URL format
    match = re.match(youtube_pattern, url.strip())

    # Return True if it's a valid YouTube URL and there are no other issues
    if match:
        return True

    return False

#####sizelimit

#load_dotenv()

def validate_video_constraints(url: str, fmt: str, quality: str ):
    #max_filesize=1073741824
    max_filesize=int(os.getenv("MAX_FILESIZE",1073741824))
    #max_duration=18000
    
    max_duration=int(os.getenv("MAX_DURATION",18000))
    #print(max_duration)
    try:
        with YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)
    except Exception:
        raise HTTPException(status_code=400, detail="Failed to extract video metadata")
    
    duration = info.get("duration", 0)
    #print(duration)
    if duration > max_duration:
        save_download_history(url, "Failed")
        raise HTTPException(status_code=400, detail=f"Video longer than 5hours, video is {round(duration / 60/60, 2)} hours")

    #filesize
    #quality_int=int(quality)
    if fmt == "mp3":
        filesize = info.get("filesize_approx", 0)
    else:
        '''formats = info.get("formats", [])
        for f in formats:
            if f.get("height") == quality_int and f.get("ext") == fmt:
                filesize = f.get("filesize") or f.get("filesize_approx", 0)
                break'''
        filesize = info.get("filesize") or info.get("filesize_approx", 0)


    if filesize > max_filesize:
        save_download_history(url, "Failed")
        raise HTTPException(status_code=400, detail=f"File larger than 3GB,filesize is : {round(filesize / 1024 / 1024/1024, 2)} GB")