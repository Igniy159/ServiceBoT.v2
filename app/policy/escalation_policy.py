from app.enums import State
from app.policy.base_policy import Policy


class EscalationPolicy(Policy):


    async def resolve_state(self,
                      branch_id: int,
                      permissions: set[str])->State:
        manager = await self.get_branch_manager(branch_id)
        if not manager:
            return State.CONFIRMED
        if 'ticket:confirm' in permissions or 'full_access' in permissions:
            return State.CONFIRMED

        return State.NEW
