from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User
from app.errors import AuthorizeError


class Identification:
    def __init__(self, tg_id:int,
                 session: AsyncSession):
        self.tg_id = tg_id
        self.session = session

    async def get_actor(self)->User:
        stmt = select(User).where(User.tg_id == self.tg_id)
        result = await self.session.execute(stmt)
        actor = result.scalar_one_or_none()
        if actor is None:
            raise AuthorizeError('User not found')
        if not actor.is_active:
            raise AuthorizeError('User has deactivated')
        return actor
