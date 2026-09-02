from os import getenv

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


class SettingApp:
    def __init__(self):
        load_dotenv()
        self.url_bd = getenv('URL_BD')
        self.engine = create_engine(url=self.url_bd)
        self.session = Session(self.engine)

setting_app = SettingApp()