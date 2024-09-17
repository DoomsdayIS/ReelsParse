import httpx

from src.social_media.media_api import MediaAPI
from src.social_media.util import get_inst_shortcode_from_url


class InstagramScraperAPI(MediaAPI):
    """
    This class implements interaction with https://rapidapi.com/social-api1-instagram/api/instagram-scraper-api2
    """

    def __init__(self, user_key: str):
        self.headers = {
            "x-rapidapi-key": user_key,
            "x-rapidapi-host": "instagram-scraper-api2.p.rapidapi.com"
        }

    def create_request_arguments(self, reels_url: str) -> dict:
        request_arguments = {
            "url": "https://instagram-scraper-api2.p.rapidapi.com/v1/post_info",
            "headers": self.headers,
            "params": {"code_or_id_or_url": reels_url, "include_insights": "true"}
        }
        return request_arguments

    @staticmethod
    def get_views_from_response(response: httpx.Response) -> int:
        return response.json()['data']['metrics']['play_count']


class InstagramBulkScraperAPI(MediaAPI):
    """
    This class implements interaction with https://rapidapi.com/mrngstar/api/instagram-bulk-scraper-latest
    """

    def __init__(self, user_key: str):
        self.headers = {
            "x-rapidapi-key": user_key,
            "x-rapidapi-host": "instagram-bulk-scraper-latest.p.rapidapi.com"
        }

    def create_request_arguments(self, reels_url: str) -> dict:
        request_arguments = {
            "url": f"https://instagram-bulk-scraper-latest.p.rapidapi.com/media_info_from_shortcode/{get_inst_shortcode_from_url(reels_url)}",
            "headers": self.headers
        }
        return request_arguments

    @staticmethod
    def get_views_from_response(response: httpx.Response) -> int:
        if response.json()['message']:
            if response.json()['message'].startswith('You have exceeded'):
                raise httpx.TimeoutException(message=response.json()['message'])
        return int(response.json()['data']['video_play_count'])
