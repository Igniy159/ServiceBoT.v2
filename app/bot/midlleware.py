from aiogram import BaseMiddleware, Bot
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User
from app.bot.identification import Identification
from app.errors import AuthorizeError
from app.usecase import UseCaseFactory

class RequestContext:
    def __init__(self, session:AsyncSession,
                 actor: User,
                 bot: Bot):
        use_case_factory = UseCaseFactory(session, actor)
        self.alerts = use_case_factory.alert
        self.tickets = use_case_factory.ticket
        self.users = use_case_factory.user
        self.session = session
        self.actor = actor
        self.bot = bot

class AuthMiddleware(BaseMiddleware):
    def __init__(self, session:AsyncSession):
        self.session = session

    async def __call__(self,
                 data,
                 event,
                 handler):
        tg_user = data.get("event_from_user")
        if not tg_user:
            return await handler(event, data)
        actor = await Identification(tg_user.id, self.session).get_actor()
        bot = data.get('bot')
        try:
            data['ctx'] = RequestContext(self.session, actor, bot)
            result = await handler(event, data)
        except AuthorizeError:
            await event.answer(
                    f"Вы не зарегистрированы.Обратитесь к администратору.\nВаш id: {tg_user.id}")
        except Exception:
            raise
        return result
