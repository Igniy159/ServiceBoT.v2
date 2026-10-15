from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Select
from app.enums import State
from app.models import User, Ticket, Rule, Role, Subscribe
from app.repository.user_repo import UserRepo


class NotificationPolicy:
    target_mapper = {
        State.NEW: ('manager',),
        State.CONFIRMED: ('executor',),
        State.IN_PROGRESS: ('manager',),
        State.WAITING_EXTERNAL: ('manager',),
        State.RESOLVED: ('manager',),
        State.CLOSED: ('assigned',),
        State.CANCELLED: ('assigned', 'manager')
    }

    async def ticket_push_notification_user(self, repo: UserRepo, ticket: Ticket)->list[User]:
        users = []
        target = self.target_mapper[ticket.state]
        if 'manager' in target:
            manager = await repo.get_branch_manager(ticket.branch_id)
            if not manager:
                creator = await repo.get_user_by_id(ticket.creator_id)
                users.append(creator)
            else:
                users.extend(manager)
        if 'executor' in target:
            executors = await repo.get_executors(ticket.rule)
            if not executors:
                owner = await repo.get_users_by_role_name('Владелец')
                users.extend(owner)
            else:
                users.extend(executors)
        if 'assigned' in target and ticket.assigned_to_id is not None:
            assigned_to = await repo.get_user_by_id(ticket.assigned_to_id)
            if assigned_to:
                users.append(assigned_to)
        return users

    @staticmethod
    async def get_subscribers(session:AsyncSession, rule: Rule)-> list[User]:
        stmt = (Select(User)
                .join(User.role)
                .join(Role.subscriptions)
                .join(Subscribe)
                .where(Subscribe.class_rule == rule.class_rule)
                .where(User.is_active))
        result = await session.execute(stmt)
        return list(result.scalars().all())
