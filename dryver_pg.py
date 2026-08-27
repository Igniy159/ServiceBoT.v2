import asyncio
import sys
from os import getenv
from psycopg import connect, AsyncConnection
from dotenv import load_dotenv
from psycopg_pool import ConnectionPool, AsyncConnectionPool

load_dotenv()
PASS_BD = getenv('BD_PASS')

sync_con = connect(
    host="localhost",
    port=5432,
    dbname="ticket_service",
    user="postgres",
    password=PASS_BD)

pool = ConnectionPool(
    f'host=localhost port=5432 dbname="ticket_service" user="postgres" password={PASS_BD}',max_size=20)


async def get_async_pool():
    async_pool = AsyncConnectionPool(
    f'host=localhost port=5432 dbname="ticket_service" user="postgres" password={PASS_BD}',max_size=20)
    return async_pool


async def get_async_connect():
    async_con = await AsyncConnection.connect(host="localhost",
    port=5432,
    dbname="ticket_service",
    user="postgres",
    password=PASS_BD)
    return async_con


async def main():
    print(sync_con, 'синхронное соединение')
    print(pool, 'синхронный пул')
    a_con = await get_async_connect()
    print(a_con, 'асинхронное соединение')
    a_pool = await get_async_pool()
    print(a_pool, 'асинхронный пул')

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
if __name__== '__main__':
    asyncio.run(main())