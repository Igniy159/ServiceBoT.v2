from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import VARCHAR, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.base import Base

if TYPE_CHECKING:
    from .model_ticket import Ticket

class User(Base):
    __tablename__ = 'users'
    __table_args__ = (Index('ix_users_name','name'),)
    id: Mapped[int] = mapped_column(primary_key=True,autoincrement= True)
    name: Mapped[str] = mapped_column(VARCHAR(20), nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)

    tickets: Mapped[list[Ticket]] = relationship(
        back_populates="user"
    )
