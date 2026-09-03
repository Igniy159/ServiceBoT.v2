from __future__ import annotations
from sqlalchemy import String, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from app.base import Base

if TYPE_CHECKING:
    from .model_user import User


class Ticket(Base):
    __tablename__ = 'tickets'
    __table_args__ = (Index('idx_ticket_user','user_id'),)
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    title: Mapped[str] = mapped_column(String(20), nullable=True)
    description: Mapped[str] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped[User] = relationship(
        back_populates="tickets")
