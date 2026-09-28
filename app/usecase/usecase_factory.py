from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User
from app.usecase.usecase_alert import AlertUseCase
from app.usecase.usecase_ticket import TicketUseCase
from app.usecase.usecase_user import UserUseCase


class UseCaseFactory:
    def __init__(self,
                 session: AsyncSession,
                 actor: User):
        self.alert = AlertUseCase(actor=actor,
                                  session=session)
        self.ticket = TicketUseCase(actor=actor,
                                    session=session)
        self.user = UserUseCase(actor=actor,session=session)