from abc import ABC, abstractmethod


class TdxRepositoryInterface(ABC):
    @abstractmethod
    async def subscribe(
        self,
        user_id: int,
        city: str,
        route_id: str,
        direction: int,
        target_stop_uid: str,
        notify_before_minutes: int,
        email: str,
        schedule_name: str,
    ) -> int:
        raise NotImplementedError


INSERT_SUBSCRIPTION_QUERY = """
    INSERT INTO tdx_subscriptions (user_id, city, route_id, direction, target_stop_uid, notify_before_minutes, email, schedule_name)
    VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
    RETURNING id
"""


class TdxRepository(TdxRepositoryInterface):
    def __init__(self, conn):
        self.conn = conn

    async def subscribe(
        self,
        user_id: int,
        city: str,
        route_id: str,
        direction: int,
        target_stop_uid: str,
        notify_before_minutes: int,
        email: str,
        schedule_name: str,
    ) -> int:
        return await self.conn.fetchval(
            INSERT_SUBSCRIPTION_QUERY,
            user_id,
            city,
            route_id,
            direction,
            target_stop_uid,
            notify_before_minutes,
            email,
            schedule_name,
        )
