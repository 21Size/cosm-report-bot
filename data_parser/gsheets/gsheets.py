import pygsheets

from data_parser.config import settings


class GSheets:
    def __init__(self):
        self.client = pygsheets.authorize(
            client_secret=settings.gsheets.client_secret_path,
            service_account_file=settings.gsheets.service_account_path
        )

gs = GSheets()