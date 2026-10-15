from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Select
from app.models import User, Rule, Role, Responsibility


class UserRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_executors(self, rule: Rule)->list[User]:
        stmt = (Select(User)
                .join(User.role)
                .join(Role.responsibilities)
                .join(Responsibility)
                .where(Responsibility.class_rule == rule.class_rule)
                .where(User.department_id == rule.target_id)
                .where(User.is_active))
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_users_by_role_name(self, name: str)->list[User]:
        stmt = (Select(User)
                .join(User.role)
                .where(Role.name == name)
                .where(User.is_active)
                )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_branch_manager(self, branch_id: int)-> list[User]:
        stmt = (Select(User)
                .join(User.role)
                .where(User.branch_id == branch_id)
                .where(Role.name == 'Управляющий филиала')
                .where(User.is_active)
                )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())


    async def get_user_by_id(self, user_id: int)->User:
        stmt = (Select(User)
                .where(User.id == user_id)
                .where(User.is_active)
                )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
