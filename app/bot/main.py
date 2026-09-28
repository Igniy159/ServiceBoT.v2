import asyncio
from os import getenv
from aiogram import Bot, Dispatcher
from app.bot.midlleware import AuthMiddleware
from dotenv import load_dotenv
from app.setting_app import setting_app
from handlers import routers


async def main():
    dp = Dispatcher()
    bot = Bot(token=getenv("BOT_TOKEN"))
    session = await setting_app.get_session()
    middleware = AuthMiddleware(session)
    for router in routers:
        router.message.middleware(middleware)
        router.callback_query.middleware(middleware)
        dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    load_dotenv()
    asyncio.run(main())
