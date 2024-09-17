from src.social_media.media import Media


class Youtube(Media):

    @staticmethod
    def is_valid_url(url: str) -> bool:
        return url.startswith('https://youtube.com/shorts/') or url.startswith('https://www.youtube.com/shorts/')
