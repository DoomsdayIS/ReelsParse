import httpx

from src.social_media.media_api import MediaAPI
from src.social_media.util import get_youtube_id_from_url


class YtAPI(MediaAPI):
    """
    This class implements interaction with https://rapidapi.com/ytjar/api/yt-api
    """

    def __init__(self, user_key: str):
        self.headers = {
            "x-rapidapi-key": user_key,
            "x-rapidapi-host": "yt-api.p.rapidapi.com"
        }

    def create_request_arguments(self, reels_url: str) -> dict:
        request_arguments = {
            "url": "https://yt-api.p.rapidapi.com/shorts/info",
            "headers": self.headers,
            "params": {"id": get_youtube_id_from_url(reels_url)}
        }
        return request_arguments

    @staticmethod
    def get_views_from_response(response: httpx.Response) -> int:
        return int(response.json()['viewCount'])
