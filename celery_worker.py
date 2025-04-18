# celery_worker.py
from celery import Celery
import os

celery_app = Celery(
    "worker",
    broker=os.getenv("REDIS_BROKER_URL"),  # Redis broker
    backend=os.getenv("REDIS_BROKER_URL") # Redis result backend
)

celery_app.conf.task_routes = {
    "app.services.tasks.download_video_task": {"queue": "downloads"}
}
