from redbeat import RedBeatSchedulerEntry

from worker.celery import celery_app


@celery_app.task(bind=True)
def subscribe_arrival(self, schedule_name):
    print(f"Running job: {schedule_name}")

    # 假設我們判斷某條件為 true 就移除自己
    should_remove = True
    if should_remove:
        print(f"Removing job: {schedule_name}")
        entry = RedBeatSchedulerEntry.from_key(f"redbeat:{schedule_name}", celery_app)
        entry.delete()
