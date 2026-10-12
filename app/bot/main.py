import asyncio
import sys
from os import getenv
from aiogram import Bot, Dispatcher
from app.bot.midlleware import AuthMiddleware
from dotenv import load_dotenv

from app.models import User
from app.setting_app import setting_app
from handlers import routers

class FakeUsers:
    users = [User(name='Великий АДМИН',tg_id=8752047609,role_id=1),
        User(name='Владыка Системы', tg_id= 38923424542, role_id=2),
        User(name='Управляющий драконом',tg_id=2934632345, role_id=3,branch_id=1),
        User(name='Управляющий вепрем', tg_id=29134643342, role_id=3, branch_id=2),
        User(name='Культист дракона', tg_id=234234446354, role_id=4, branch_id=1),
        User(name='Прислужник волка', tg_id=2312446354, role_id=4, branch_id=4),
        User(name='Служащий вепрю',tg_id=1352436543,role_id=4, branch_id=2),
        User(name='Великий исправитель',tg_id=2422434553, role_id=5,department_id=6),
        User(name='Страж порядка', tg_id= 134112352313, role_id=6,department_id=4),
        User(name='Повелитель молний', tg_id=13412432213, role_id=7, department_id=7),
        User(name='Доставляющий грузы', tg_id=134344537313, role_id=8, department_id=8),
        User(name='Считающий золото', tg_id=671387533, role_id=9, department_id=9),
        User(name='Хранящий блага', tg_id=987646847313, role_id=10, department_id=10),
        User(name='Возглашающий истину', tg_id=21242531, role_id=11, department_id=11),
        User(name='Умиротворитель приходящих', tg_id=34562847313, role_id=12, department_id=12),
        User(name='Нанимающий адептов', tg_id=4245233847313, role_id=13, department_id=5)]

async def main():
    dp = Dispatcher()
    bot = Bot(token=getenv("BOT_TOKEN"))
    session = setting_app.session_factory()
    middleware = AuthMiddleware(session,234234446354)
    for router in routers:
        router.message.middleware(middleware)
        router.callback_query.middleware(middleware)
        dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    load_dotenv()
    print("Бот успешно запущен")
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(
            asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
