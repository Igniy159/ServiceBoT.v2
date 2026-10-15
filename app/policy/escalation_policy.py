from app.enums import State
from app.repository.user_repo import UserRepo


class EscalationPolicy:

    @staticmethod
    async def resolve_state(repo: UserRepo,
                      branch_id: int,
                      permissions: set[str])->State:
        manager = await repo.get_branch_manager(branch_id)
        if not manager:
            return State.CONFIRMED
        if 'ticket:confirm' in permissions or 'full_access' in permissions:
            return State.CONFIRMED

        return State.NEW
