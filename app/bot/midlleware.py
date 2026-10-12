from aiogram import BaseMiddleware, Bot
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User
from app.bot.identification import Identification
from app.errors import AuthorizeError
from app.usecase import UseCaseFactory
from app.policy.authorize_user import Authorize

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
        self.auth = Authorize(session,actor)

class AuthMiddleware(BaseMiddleware):
    def __init__(self, session:AsyncSession, fake_user_id: int | None = None):
        self.session = session
        self.fake = fake_user_id

    async def __call__(self,
                handler,
                event,
                data
                 ):
        tg_user = data.get("event_from_user")
        if not tg_user:
            return await handler(event, data)
        tg_id = self.fake or tg_user.id
        actor = await Identification(tg_id, self.session).get_actor()
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
