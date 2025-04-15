from celery import Celery

from config.config import get_worker_settings

settings = get_worker_settings()

celery_app = Celery(
    "worker",
    broker=settings.BROKER_URL,
    backend=settings.RESULT_BACKEND,
    beat_scheduler="redbeat.RedBeatScheduler",
    redbeat_redis_url=settings.BROKER_URL,
    include=["worker.tasks"],  # Include your task modules here
)
