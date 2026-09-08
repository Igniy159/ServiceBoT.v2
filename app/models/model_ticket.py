from __future__ import annotations

from datetime import datetime

from sqlalchemy import ForeignKey, TIMESTAMP, Enum as SqlEnum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from app.models.base import Base
from app.enums import State, Severity

if TYPE_CHECKING:
    from app.models.model_user import User
    from app.models.model_branch import Branch
    from app.models.model_rule import Rule


class Ticket(Base):
    __tablename__ = 'tickets'
    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    rule_id: Mapped[int] = mapped_column(ForeignKey('rules.id'))
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))
    branch_id: Mapped[int] = mapped_column(ForeignKey('branches.id'))
    creator_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    comment: Mapped[str | None] = mapped_column(String)
    state: Mapped[State] = mapped_column(SqlEnum(State))
    file_id: Mapped[int | None] = mapped_column(nullable=True)
    assigned_to_id: Mapped[int | None] = mapped_column(ForeignKey('users.id'), nullable=True)
    severity: Mapped[Severity] = mapped_column(SqlEnum(Severity))
    creator: Mapped[User] = relationship(back_populates='send_tickets')
    branch: Mapped[Branch] = relationship(back_populates='send_tickets')
    assigned_to: Mapped[User] = relationship(back_populates='assigned_tickets')
    rule: Mapped[Rule] = relationship(back_populates='tickets')

