from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User
from app.api.routers.depends import authenticate, get_session
from app.schemas.schemas_ticket import ReceiveTickets, TicketDTO
from app.usecase.usecase_ticket import TicketUseCase

ticket_rout = APIRouter(prefix='/v1/ticket')

def get_ticket_use_case(session: AsyncSession = Depends(get_session),
    actor: User = Depends(authenticate)
    ) -> TicketUseCase:
    return TicketUseCase(session, actor)

@ticket_rout.get('',
                tags=['Заявки'],
                response_model=list[TicketDTO])
async def receive_tickets(cmd: ReceiveTickets,
                         use_case: TicketUseCase = Depends(get_ticket_use_case)
                         )->list[TicketDTO]:
    tickets = await use_case.receive(cmd)
    if not tickets:
        raise HTTPException(status_code=404,detail='Tickets not found')
    return tickets
