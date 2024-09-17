import asyncio
import logging
import typing

from src.database.database import Database
from src.logging.util import with_default_logging
from src.social_media.media import Media

logger = logging.getLogger('reels_parser')


class ReelsParser:

    def __init__(self, database: Database, media: typing.List[Media]):
        self.db = database
        self.media = media

    @with_default_logging
    async def parse_reels(self):
        reels_urls = self.db.get_reels_urls()
        reels_views = {}
        for media in self.media:
            logger.info(f'Working to get views from urls of the media: {media.__class__} using API {media.api.__class__}')
            tasks = []
            async with asyncio.TaskGroup() as tg:
                for reels_url in reels_urls:
                    if media.is_valid_url(reels_url):
                        task = tg.create_task(media.get_views_count(reels_url))
                        tasks.append(task)
            reels_views.update({task.result()[0]: task.result()[1] for task in tasks if task})
            logger.info(f'Ended work with media: {media.__class__}')
        self.db.update_reels_views(reels_views)
