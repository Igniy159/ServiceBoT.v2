from app.enums import State
from app.models import Ticket, User
from app.policy.base_policy import Policy


class AssignmentPolicy(Policy):


    async def get_assign_user(self, ticket: Ticket)->list[User]:
        if ticket.state == State.NEW:
            users = await self.get_branch_manager(ticket)
        else:
            users = await self.get_executors(ticket.rule)
        if not users:
            users = await self.get_owner()
        return users