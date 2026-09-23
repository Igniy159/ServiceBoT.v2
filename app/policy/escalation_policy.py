from app.models import Ticket
from app.enums import State
from app.policy.base_policy import Policy


class EscalationPolicy(Policy):

    async def escalate(self, ticket: Ticket)->Ticket:
        manager = await self.get_branch_manager(ticket)
        if not manager:
            ticket.state = State.CONFIRMED
        return ticket
