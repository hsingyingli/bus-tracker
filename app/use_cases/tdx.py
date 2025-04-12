from abc import ABC, abstractmethod


class TdxUseCaseInterface(ABC):
    @abstractmethod
    def estimated_time_of_arrival(self, city: str, route: str):
        raise NotImplementedError


class TdxUseCase(TdxUseCaseInterface):
    def __init__(self, tdx_client):
        self.client = tdx_client

    def estimated_time_of_arrival(self, city: str, route: str):
        return self.client.request(
            "GET",
            f"https://tdx.transportdata.tw/api/basic/v2/Bus/EstimatedTimeOfArrival/City/{city}/{route}",
        )
