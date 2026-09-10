from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.policy.authorize_user import Authorize


class UseCase:
    def __init__(self,
                 session: AsyncSession,
                 actor: User):
        self.session = session
        self.actor = actor
        self.auth = Authorize(session, actor)