from abc import ABC, abstractmethod
from uuid import uuid4

from asyncpg import Connection
from celery.schedules import crontab
from redbeat import RedBeatSchedulerEntry

from app.repositories.tdx_repository import TdxRepositoryInterface
from app.schemas.user import User
from app.services.tdx import TdxClient
from worker.celery import celery_app


class TdxUseCaseInterface(ABC):
    @abstractmethod
    def estimated_time_of_arrival(self, city: str, route: str):
        raise NotImplementedError

    @abstractmethod
    def subscribe_arrival(
        self,
        user: User,
        city: str,
        route_id: str,
        direction: int,
        target_stop_uid: str,
        notify_before_minutes: int,
        email: str,
    ):
        raise NotImplementedError


class TdxUseCase(TdxUseCaseInterface):
    def __init__(
        self,
        tdx_client: TdxClient,
        tdx_repository: TdxRepositoryInterface,
        db_conn: Connection,
    ):
        self.client = tdx_client
        self.repository = tdx_repository
        self.db_conn = db_conn

    async def estimated_time_of_arrival(self, city: str, route: str):
        return await self.client.request(
            "GET",
            f"https://tdx.transportdata.tw/api/basic/v2/Bus/EstimatedTimeOfArrival/City/{city}/{route}",
        )

    async def subscribe_arrival(
        self,
        user: User,
        city: str,
        route_id: str,
        direction: int,
        target_stop_uid: str,
        notify_before_minutes: int,
        email: str,
    ):
        async with self.db_conn.transaction():
            schedule_name = f"tdx-subscription:{user.id}-{uuid4().hex[:6]}"
            await self.repository.subscribe(
                user.id,
                city,
                route_id,
                direction,
                target_stop_uid,
                notify_before_minutes,
                email,
                schedule_name,
            )

            entry = RedBeatSchedulerEntry(
                name=schedule_name,
                task="worker.tasks.subscribe_arrival",
                schedule=crontab(minute="*/1"),  # 每分鐘
                args=[
                    city,
                    route_id,
                    direction,
                    target_stop_uid,
                    notify_before_minutes,
                    email,
                    schedule_name,
                ],
                app=celery_app,
            )
            entry.save()
