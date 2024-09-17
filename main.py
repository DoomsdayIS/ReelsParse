import asyncio
import atexit
import json
import logging.config
import logging.handlers
import os

from src.ReelsParser import ReelsParser
from src.database.google_spreadsheets.google_spreadsheets import GoogleSpreadSheets
from src.social_media.youtube.youtube import Youtube
from src.social_media.youtube.youtube_api import YtAPI
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger('reels_parser')

if __name__ == '__main__':
    logger_config_filepath = os.getenv("LOGGER_CONFIG_FILEPATH")
    with open(logger_config_filepath) as f_in:
        config = json.load(f_in)
    logging.config.dictConfig(config)
    queue_handler = logging.getHandlerByName("queue_handler")
    if queue_handler is not None:
        queue_handler.listener.start()
        atexit.register(queue_handler.listener.stop)

    spreadsheets_url = os.getenv("SPREADSHEETS_URL")
    service_file = os.getenv("SERVICE_FILE")
    spreadsheets = GoogleSpreadSheets(
        spreadsheets_url=spreadsheets_url,
        service_file=service_file)

    rapidapi_user_key = os.getenv("RAPIDAPI_USER_KEY")
    youtube_api = YtAPI(rapidapi_user_key)
    youtube = Youtube(api=youtube_api, rate_limit=2)

    parser = ReelsParser(database=spreadsheets, media=[youtube])
    asyncio.run(parser.parse_reels())
