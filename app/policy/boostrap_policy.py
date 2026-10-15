from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User, Role


class BoostrapPolicy:

    @staticmethod
    async def has_user_in_db(session:AsyncSession)->bool:
        stmt = select(
            select(User.id).exists()
        )
        result = await session.execute(stmt)
        return result.scalar()

    @staticmethod
    async def get_admin_id(session: AsyncSession)->int:
        stmt = select(Role.id).where(Role.name == 'Админ')
        result = await session.execute(stmt)
        return result.scalar()
