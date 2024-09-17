from src.social_media.media import Media


class Instagram(Media):

    @staticmethod
    def is_valid_url(url: str) -> bool:
        return url.startswith('https://www.instagram.com/reel/')
