import asyncio
import time
import typing
import httpx

from abc import abstractmethod, ABCMeta
from src.social_media.media_api import MediaAPI


class Media(metaclass=ABCMeta):
    def __init__(self, *, api: MediaAPI, rate_limit: int = 1):
        self.api = api
        self.semaphore = asyncio.Semaphore(rate_limit)

    async def get_views_count(self, url: str) -> typing.Tuple[str, int] | None:
        """
        This function gets the number of views using API
        Returns a tuple of (url, reels views count) if everything went well, otherwise None
        """
        request_arguments = self.api.create_request_arguments(url)
        async with self.semaphore:
            async with httpx.AsyncClient() as client:
                try:
                    response = await client.get(**request_arguments, timeout=10)
                    time.sleep(0.5)
                    try:
                        views = self.api.get_views_from_response(response)
                    except (KeyError, TypeError):
                        return
                    return url, views
                except httpx.TimeoutException:
                    time.sleep(10)

    @staticmethod
    @abstractmethod
    def is_valid_url(url: str) -> bool:
        pass
