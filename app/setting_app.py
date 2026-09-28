from os import getenv
from typing import AsyncGenerator

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, engine, AsyncSession


class SettingApp:
    def __init__(self):
        load_dotenv()
        self.url_bd = getenv('URL_BD')
        self.engine = create_async_engine(url=self.url_bd,
            pool_size=10,
            max_overflow=20)
        self.session_factory = async_sessionmaker(
            self.engine,
            expire_on_commit=False)

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session_factory() as session:
            yield session
            await session.commit()

setting_app = SettingApp()

