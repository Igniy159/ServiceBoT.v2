from app.enums import State
from app.usecase.base_usecase import UseCase

class TicketUseCase(UseCase):
    fsm_mapper = {
        State.NEW: {State.CONFIRMED, State.CANCELLED},
        State.CONFIRMED: {State.IN_PROGRESS, State.CANCELLED},
        State.IN_PROGRESS: {State.WAITING_EXTERNAL, State.RESOLVED, State.CANCELLED},
        State.WAITING_EXTERNAL: {State.IN_PROGRESS, State.RESOLVED, State.CANCELLED},
        State.RESOLVED: {State.CLOSED, State.CANCELLED},
        State.CLOSED: set(),
        State.CANCELLED: set()}

    def _allowed_transition(self,current_state: State,
                            next_state: State)-> bool:

        allowed_steps = self.fsm_mapper[current_state]
        return next_state in allowed_steps


    async def create(self):
        pass

    async def update_state(self):
        pass

    async def receive(self):
        pass

