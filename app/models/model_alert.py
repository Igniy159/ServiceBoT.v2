from __future__ import annotations
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, TIMESTAMP, String
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.models.base import Base
if TYPE_CHECKING:
    from app.models.model_user import User
    from app.models.model_branch import Branch
    from app.models.model_rule import Rule


class Alert(Base):
    __tablename__ = 'alerts'
    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    rule_id: Mapped[int] = mapped_column(ForeignKey('rules.id'))
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))
    branch_id: Mapped[int] = mapped_column(ForeignKey('branches.id'))
    creator_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    comment: Mapped[str | None] = mapped_column(String, nullable=True)
    creator: Mapped[User] = relationship(back_populates='send_alerts')
    branch: Mapped[Branch] = relationship(back_populates='send_alerts')
    rule: Mapped[Rule] = relationship(back_populates='alerts')
