import typing

from abc import ABCMeta, abstractmethod


class Database(metaclass=ABCMeta):

    @abstractmethod
    def get_reels_urls(self) -> typing.List[str]:
        pass

    @abstractmethod
    def update_reels_views(self, reels_views: typing.Dict[str, int]):
        pass
