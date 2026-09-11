from datetime import datetime

from sqlalchemy import Select
from sqlalchemy.orm import selectinload

from app.errors import AuthorizeError, ResourceNotFound, ProhibitFSM
from app.models import Ticket, Rule
from app.enums import State
from app.policy.authorize_user import Authorize
from app.schemas.schemas_ticket import CreateTicket, ChangeStateTicket, ReceiveTickets
from app.usecase.base_usecase import UseCase

class TicketUseCase(UseCase):
    _fsm_mapper = {
        State.NEW: {State.CONFIRMED, State.CANCELLED},
        State.CONFIRMED: {State.IN_PROGRESS, State.CANCELLED},
        State.IN_PROGRESS: {State.WAITING_EXTERNAL, State.RESOLVED, State.CANCELLED},
        State.WAITING_EXTERNAL: {State.IN_PROGRESS, State.RESOLVED, State.CANCELLED},
        State.RESOLVED: {State.CLOSED, State.CANCELLED},
        State.CLOSED: set(),
        State.CANCELLED: set()}

    _permission_mapper = {
        State.NEW: 'ticket:create',
        State.CONFIRMED: 'ticket:confirm',
        State.IN_PROGRESS: 'ticket:accept',
        State.WAITING_EXTERNAL: 'ticket:accept',
        State.RESOLVED: 'ticket:accept',
        State.CLOSED: 'ticket:close',
        State.CANCELLED: 'ticket:cancel'}

    async def create(self, cmd: CreateTicket):
        await self.auth.load_role()
        state_ticket = self._resolve_state(self.auth)
        await self._check_rule(cmd.rule_id)
        now = datetime.now()
        branch_id = self.auth.resolve_branch(cmd)
        new_ticket = Ticket(rule_id=cmd.rule_id,
                        created_at=now,
                        branch_id=branch_id,
                        creator_id=self.actor.id,
                        comment=cmd.comment,
                        state=state_ticket,
                        severity=cmd.severity,
                        file_id=cmd.file_id)
        self.session.add(new_ticket)
        await self.session.flush()



    async def update_state(self, cmd: ChangeStateTicket):
        self.auth.load_role()
        need_permission = self._required_permission(cmd.new_state)
        self.auth.check(need_permission)
        ticket = await self._get_ticket(cmd.ticket_id)
        if not self._allowed_transition(ticket.state, cmd.new_state):
            raise ProhibitFSM(
                f'Ticket has not transition {ticket.state.name} -> {cmd.new_state.name}')
        ticket.state = cmd.new_state
        ticket.comment = cmd.comment
        await self.session.flush()


    async def receive(self, cmd: ReceiveTickets)->list[Ticket]:
        await self.auth.load_role()
        self.auth.check('ticket:receive')
        cmd = self.auth.check_restricts(cmd)
        stmt = Select(Ticket)
        if cmd.class_rule or cmd.department_id:
            stmt = stmt.join(Rule)
        if cmd.ticket_id is not None:
            stmt = stmt.where(Ticket.id == cmd.ticket_id)
        if cmd.branch_id is not None:
            stmt = stmt.where(Ticket.branch_id == cmd.branch_id)
        if cmd.department_id is not None:
            stmt = stmt.where(Rule.target_id == cmd.department_id)
        if cmd.creator_id is not None:
            stmt = stmt.where(Ticket.creator_id == cmd.creator_id)
        if cmd.class_rule is not None:
            stmt = stmt.where(Rule.class_rule == cmd.class_rule)
        if cmd.created_from is not None:
            stmt = stmt.where(Ticket.created_at >= cmd.created_from)
        if cmd.created_to is not None:
            stmt = stmt.where(Ticket.created_at < cmd.created_to)

        if cmd.limit is not None:
            stmt = stmt.limit(cmd.limit)
        if cmd.offset is not None:
            stmt = stmt.offset(cmd.offset)

        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    def _allowed_transition(self,current_state: State,
                            next_state: State)-> bool:
        allowed_steps = self._fsm_mapper[current_state]
        return next_state in allowed_steps

    def _required_permission(self, next_state: State)->str:
        return self._permission_mapper[next_state]

    @staticmethod
    def _resolve_state(auth:Authorize)->State:
        if 'ticket:confirm' in auth.permissions:
            return State.CONFIRMED
        if 'ticket:create' in auth.permissions:
            return State.NEW
        raise AuthorizeError(f'User {auth.actor.name} has not permission create ticket')

    async def _check_rule(self,rule_id:int):
        result = await self.session.execute(Select(Rule).where(Rule.id == rule_id))
        rule = result.scalar_one_or_none()
        if rule is None:
            raise ResourceNotFound(f"Rule {rule_id} not found")

    async def _get_ticket(self,ticket_id: int)->Ticket:
        result = await self.session.execute(Select(Ticket)
                                            .options(selectinload(Ticket.rule))
                                            .where(Ticket.id == ticket_id))
        ticket = result.scalar_one_or_none()
        if ticket is None:
            raise ResourceNotFound(f'Ticket {ticket_id} not found')
        return ticket
