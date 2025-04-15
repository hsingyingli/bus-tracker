import asyncio

from redbeat import RedBeatSchedulerEntry

from app.services.email_service import EmailService
from app.services.tdx import TdxClient
from config.config import get_worker_settings
from worker.celery import celery_app

settings = get_worker_settings()


@celery_app.task(bind=True)
def subscribe_arrival(
    self,
    city,
    route_id,
    direction,
    target_stop_uid,
    notify_before_minutes,
    email,
    schedule_name,
):
    client = TdxClient()
    schedules = asyncio.run(
        client.request(
            "GET",
            f"https://tdx.transportdata.tw/api/basic/v2/Bus/EstimatedTimeOfArrival/City/{city}/{route_id}",
        )
    )

    estimate_time = None
    for schedule in schedules:
        if (
            schedule["Direction"] == direction
            and schedule["StopUID"] == target_stop_uid
            and schedule["StopStatus"] <= 1
        ):
            estimate_time = schedule.get("EstimateTime", None)

    if estimate_time is None:
        return

    if estimate_time > notify_before_minutes * 60:
        return

    EmailService().send_email(
        email, subject="即將到達的公車", body=f"公車即將在 {estimate_time} 秒後到達"
    )

    entry = RedBeatSchedulerEntry.from_key(f"redbeat:{schedule_name}", celery_app)
    entry.delete()
