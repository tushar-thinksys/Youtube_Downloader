#  FastAPI YouTube Downloader

A FastAPI-based REST API to download YouTube videos and audio using `yt-dlp` with fallback to `pytube`, supports background processing with Celery + Redis, video size/duration limits, and stores download history in PostgreSQL using SQLModel.

---

##  Features

- ✅ Video/audio download with format & quality selection
- ✅ Async background tasks using **Celery + Redis**
- ✅ Validates max duration (default: 5 hours) & file size (default: 3 GB)
- ✅ Fallback: Tries `yt-dlp` first, uses `pytube` on failure
- ✅ Download history saved using SQLModel
- ✅ API key protection & rate limiting(default:100 times per day)
- ✅ Clean modular codebase

---

# 🎨 FastAPI YouTube Downloader API

A **REST API** built with **FastAPI** that enables users to **download YouTube videos**, **extract audio**, and **retrieve video metadata** using a valid YouTube URL.

---

## 🚀 Features

- ✅ Download YouTube videos in multiple formats (MP4, WEBM, MKV, etc.)
- 🎷 Extract and download audio-only (MP3)
- 📊 Retrieve video metadata: title, duration, views, likes, channel name, publish date, thumbnail
- 📁 Temporary file storage with automatic cleanup
- 🔁 Fallback mechanism: uses `yt-dlp` with `pytube` as a backup
- ⚡ Fully async API for high performance
- 🧠 Modular and clean project structure
- 🛠️ Optional Celery + Redis for background task processing
- 🔒 Environment-based limits (e.g., max file size, max duration)
- 🔐 Ready for authentication, rate-limiting, and Docker deployment

---

## 🧱 Project Structure

```
.
youtube_downloader/
├── app/
│   ├── db/
│   │   └── database.py
│   ├── dependencies/
│   │   ├── auth.py
│   │   └── rate_limiter.py
│   ├── models/
│   │   ├── history.py
│   │   └── schemas.py
│   ├── routes/
│   │   ├── download.py
│   │   ├── history.py
│   │   └── metadata.py
│   ├── services/
│   │   ├── downloader.py
│   │   ├── history_service.py
│   │   ├── metadata_extractor.py
│   │   └── tasks.py
│   ├── utils.py/
│   │   └── validators.py   
│   └── main.py                 ✅ FastAPI entry point (inside app)
├── celery_worker.py            ✅ Celery worker (outside app)
├── .env
├── README.md
└── requirements.txt
```

---

## 📦 API Endpoints

### 🎥 Download Video

```http
POST /download
```

**Request Body (JSON):**

```json
{
  "url": "https://www.youtube.com/watch?v=example",
  "format": "mp4",
  "quality": "720p"
}
```

**Response:**

- File as downloadable attachment

---

### 🎷 Download Audio

Use `"format": "mp3"` in the `/download` request to download audio only.

---

### 🦾 Get Metadata

```http
GET /metadata?url=https://www.youtube.com/watch?v=example
```

**Response:**

```json
{
  "title": "Sample Video",
  "duration": 540,
  "views": 100000,
  "likes": 5000,
  "channel": "Sample Channel",
  "published_date": "2022-01-01",
  "thumbnail": "https://example.com/thumbnail.jpg"
}
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/fastapi-youtube-downloader.git
cd fastapi-youtube-downloader
```

### 2. Create a Virtual Environment

```bash
python -m venv .env
source .env/bin/activate  # Linux/macOS
.env\Scripts\activate     # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Create `.env` File

```env
DATABASE_URL = "postgresql://postgres:tushar@localhost:5432/yt_downloader"
API_KEY=password123
REDIS_BROKER_URL=redis://localhost:6379/0
RATE_LIMIT=100
TIME_WINDOW=86400
MAX_DURATION=18000
MAX_FILESIZE=3221225472
```

---

### 5. Run FastAPI Server

```bash
uvicorn app.main:app --reload
```

Visit the interactive API docs at: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🥪 Optional: Background Downloads with Celery + Redis

1. Start Redis server
2. Launch Celery worker:
   ```
   celery -A celery_worker.celery_app worker --loglevel=info
   ```

---

## 📤 Future Enhancements

- ✅ OAuth2 / API key authentication
- ✅ Docker + Gunicorn deployment
- ✅ PostgreSQL-based download history
- ✅ Frontend UI with download progress
- ✅ Caching, and analytics

---

## 📄 License

This project is licensed under the MIT License.

---

## 🙌 Contributing

Contributions, issues, and feature requests are welcome!

---

## ✨ Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com/)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [pytube](https://github.com/pytube/pytube)
- [Celery](https://docs.celeryq.dev/en/stable/)

