import httpx

from abc import abstractmethod, ABCMeta


class MediaAPI(metaclass=ABCMeta):
    @abstractmethod
    def create_request_arguments(self, url: str) -> dict:
        pass

    @staticmethod
    @abstractmethod
    def get_views_from_response(response: httpx.Response) -> int:
        pass
