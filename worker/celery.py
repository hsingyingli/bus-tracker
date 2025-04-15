from celery import Celery

from config.config import get_worker_settings

settings = get_worker_settings()

celery_app = Celery(
    "worker",
    broker=settings.BROKER_URL,
    backend=settings.RESULT_BACKEND,
    include=["worker.tasks"],
)

celery_app.conf.beat_scheduler = "redbeat.RedBeatScheduler"
celery_app.conf.redbeat_redis_url = settings.BROKER_URL
celery_app.conf.beat_max_loop_interval = 5
celery_app.conf.redbeat_lock_timeout = 10
