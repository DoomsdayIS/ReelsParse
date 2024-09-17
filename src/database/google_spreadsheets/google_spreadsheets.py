import logging
import time
import typing
import gspread

from datetime import datetime
from src.database.database import Database
from src.logging.util import with_default_logging
from google.oauth2 import service_account
from gspread.exceptions import APIError

logger = logging.getLogger('reels_parser')


class GoogleSpreadSheets(Database):
    expected_columns_names = {
        'Просмотры рилс': 'alltime_views_column',
        'Ссылка на рилс': 'reels_link_column',
        'Просмотры за последний день': 'yesterday_views_column',
        'Дата обновления': 'date_column'
    }

    columns_indexes: dict[str, typing.Optional[int]] = {
        'alltime_views_column': None,
        'reels_link_column': None,
        'yesterday_views_column': None,
        'date_column': None,
    }

    @with_default_logging
    def __init__(self, spreadsheets_url: str, service_file: str):
        self.spreadsheets_url = spreadsheets_url
        self.service_file = service_file
        self.credentials = service_account.Credentials.from_service_account_file(self.service_file,
                                                                                 scopes=[
                                                                                     'https://spreadsheets.google.com/feeds',
                                                                                     'https://www.googleapis.com/auth/drive'])
        self.worksheets = self._get_worksheets()
        logger.info('Successfully got worksheets')

    def _get_worksheets(self):
        gc = gspread.authorize(self.credentials)
        sh = gc.open_by_url(self.spreadsheets_url)
        return sh.worksheets()

    def _prepare_worksheet(self, worksheet):
        data = worksheet.get_all_values()
        try:
            column_names = [i.strip() for i in data[0]]
            for column_name_rus, column_name_eng in self.expected_columns_names.items():
                self.columns_indexes[column_name_eng] = column_names.index(column_name_rus)
        except (ValueError, IndexError):
            return None
        return data

    @with_default_logging
    def get_reels_urls(self) -> typing.List[str]:
        reels_urls = []
        for worksheet in self.worksheets:
            data = self._prepare_worksheet(worksheet)
            if not data:
                logger.info(f"Skipping worksheet: {worksheet.title}. Incorrect column names")
                continue
            logger.info(f"Getting urls from the worksheet: {worksheet.title}")
            for row_index, row in enumerate(data):
                try:
                    reels_link = row[self.columns_indexes['reels_link_column']]
                    reels_urls.append(reels_link)
                except Exception:
                    pass
        return reels_urls

    @with_default_logging
    def update_reels_views(self, reels_views: typing.Dict[str, int]):
        updated_rows = 0
        for worksheet in self.worksheets:
            data = self._prepare_worksheet(worksheet)
            if not data:
                continue
            for row_index, row in enumerate(data):
                try:
                    reels_link = row[self.columns_indexes['reels_link_column']]
                    views_alltime = int(row[self.columns_indexes['alltime_views_column']]) if row[self.columns_indexes[
                        'alltime_views_column']] != '' else 0
                except Exception:
                    continue
                if reels_link in reels_views:
                    time.sleep(0.2)
                    yesterday_views = reels_views[reels_link] - views_alltime
                    while True:
                        date = datetime.now().strftime("%d.%m.%Y, %H:%M:%S")
                        try:
                            worksheet.update_cell(row_index + 1, self.columns_indexes['alltime_views_column'] + 1,
                                                  str(reels_views[reels_link]))
                            worksheet.update_cell(row_index + 1, self.columns_indexes['yesterday_views_column'] + 1,
                                                  str(yesterday_views))
                            worksheet.update_cell(row_index + 1, self.columns_indexes['date_column'] + 1, date)
                            updated_rows += 1
                        except APIError as e:
                            time.sleep(5)
                            continue
                        break
        logger.info(f"Updated rows {updated_rows}")