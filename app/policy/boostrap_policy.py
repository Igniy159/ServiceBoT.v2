from sqlalchemy import select
from app.models import User, Role
from app.policy.base_policy import Policy


class BoostrapPolicy(Policy):

    async def has_user_in_db(self)->bool:
        stmt = select(
            select(User.id).exists()
        )
        result = await self.session.execute(stmt)
        return result.scalar()

    async def get_owner_id(self)->int:
        stmt = select(Role.id).where(Role.name == 'Владелец')
        result = await self.session.execute(stmt)
        return result.scalar()
