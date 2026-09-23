from sqlalchemy import Select
from app.enums import State
from app.models import User, Role, Ticket, Rule, Alert, Subscribe
from app.policy.base_policy import Policy


class NotificationPolicy(Policy):
    target_mapper = {
        State.NEW: ('manager',),
        State.CONFIRMED: ('executor','subscriber'),
        State.IN_PROGRESS: ('manager',),
        State.WAITING_EXTERNAL: ('manager',),
        State.RESOLVED: ('manager',),
        State.CLOSED: ('executor',),
        State.CANCELLED: ('executor', 'manager')
    }
    async def _get_subscribers(self, rule: Rule)-> list[User]:
        stmt = (Select(User)
                .join(User.role)
                .join(Role.subscriptions)
                .join(Subscribe)
                .where(Subscribe.class_rule == rule.class_rule)
                .where(User.is_active))
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_notification_user(self, ticket: Ticket | Alert)->set[User]:
        state = State.CONFIRMED
        rule = ticket.rule
        users = set()
        if isinstance(ticket, Ticket):
            state = ticket.state
        target = self.target_mapper[state]
        if 'manager' in target:
            users.update(await self.get_branch_manager(ticket))
        if 'executor' in target:
            users.update(await self.get_executors(rule))
        if 'subscriber' in target:
            users.update(await self._get_subscribers(rule))
        return users
