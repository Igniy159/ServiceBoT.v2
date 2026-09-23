from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Select

from app.enums import ClassRule
from app.models import Role, Ticket, User, Responsibility, Permission, Alert, Rule


class Policy:
    def __init__(self,session:AsyncSession):
        self.session = session

    async def get_executors(self, rule: Rule)->list[User]:
        stmt = (Select(User)
                .join(User.role)
                .join(Role.responsibilities)
                .where(User.branch_id == rule.target_id)
                .where(Responsibility.class_rule == rule.class_rule)
                .where(User.is_active))
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_owner(self):
        stmt = (Select(User)
                .join(User.role)
                .join(Role.responsibilities)
                .where(Responsibility.class_rule == ClassRule.ALL)
                .limit(1))
        result = await self.session.execute(stmt)
        return [result.scalar_one()]

    async def get_branch_manager(self, ticket: Ticket | Alert)->list[User]:
        stmt = (Select(User)
                .join(User.role)
                .join(Role.permissions)
                .where(User.branch_id == ticket.branch_id)
                .where(Permission.name == 'ticket:confirm')
                .where(User.is_active)
                .limit(1))
        result = await self.session.execute(stmt)
        return [result.scalar_one()]

class TicketLifecycle:
    def __init__(self):
        pass