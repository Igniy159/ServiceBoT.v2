import asyncio
import sys

from sqlalchemy import create_engine, URL, text
from dotenv import load_dotenv
from os import getenv

from sqlalchemy.ext.asyncio import create_async_engine

load_dotenv()
PASS_BD = getenv('BD_PASS')

# dialect+driver://username:password@host:port/database
url_from_engine = f"postgresql+psycopg://postgres:{PASS_BD}@localhost:5432/ticket_service"

url_obj = URL.create(drivername='postgresql+psycopg',
              username='postgres',
              password=PASS_BD,
              host='localhost',
              port=5432,
              database='ticket_service')

engine = create_engine(url_from_engine, pool_size=5, max_overflow=10, pool_pre_ping=True, echo=True)

async_engine = create_async_engine(url_obj)



async def get_async_con():
    async_con = await async_engine.connect()
    return async_con

async def main():
    con = engine.connect()
    print(url_obj, 'объект для инициализации engine')
    print(url_from_engine, 'тоже только в формате f строки')
    print(engine, 'класс ORM который непосредственно связывает с БД, через драйвер')
    print(con, 'синхронное соединение с БД как объект ORM')
    with engine.connect() as con:
        result = con.execute(text("SELECT 1"))
        print(result.scalar(), 'ответ на синхронный запрос')
    acon = await get_async_con()
    print(acon, 'асинхронное соединение')
    print(engine.pool, 'синхронный пул')

    print(async_engine.pool, 'асинхронный пул')
    async with async_engine.connect() as con:
        result = await con.execute(text("SELECT 1"))
        print(result.scalar(),'ответ на асинхронный запрос')
    await acon.close()


if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

if __name__== '__main__':
    asyncio.run(main())
