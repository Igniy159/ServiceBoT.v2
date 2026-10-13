from app.enums import State
from app.models import User, Ticket
from app.policy.base_policy import Policy

class NotificationPolicy(Policy):
    target_mapper = {
        State.NEW: ('manager',),
        State.CONFIRMED: ('executor',),
        State.IN_PROGRESS: ('manager',),
        State.WAITING_EXTERNAL: ('manager',),
        State.RESOLVED: ('manager',),
        State.CLOSED: ('assigned',),
        State.CANCELLED: ('assigned', 'manager')
    }

    async def ticket_push_notification_user(self, ticket: Ticket)->list[User]:
        users = []
        target = self.target_mapper[ticket.state]
        if 'manager' in target:
            manager = await self.get_branch_manager(ticket.branch_id)
            if not manager:
                creator = await self.get_user_by_id(ticket.creator_id)
                users.append(creator)
            else:
                users.extend(manager)
        if 'executor' in target:
            executors = await self.get_executors(ticket.rule)
            if not executors:
                owner = await self.get_owner()
                users.append(owner)
            else:
                users.extend(executors)
        if 'assigned' in target and ticket.assigned_to_id is not None:
            assigned_to = await self.get_user_by_id(ticket.assigned_to_id)
            if assigned_to:
                users.append(assigned_to)
        return users
