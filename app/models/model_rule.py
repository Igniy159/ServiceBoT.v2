from __future__ import annotations
from typing import TYPE_CHECKING

from app.enums import KindRule, ClassRule
from app.models.base import Base

from sqlalchemy import VARCHAR, Enum as SqlEnum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.models.model_department import Department
    from app.models.model_alert import Alert
    from app.models.model_ticket import Ticket


class Rule(Base):
    __tablename__ = 'rules'
    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    kind: Mapped[KindRule] = mapped_column(SqlEnum(KindRule))
    class_rule: Mapped[ClassRule] = mapped_column(SqlEnum(ClassRule))
    name: Mapped[str] = mapped_column(VARCHAR(30), unique=True)
    target_id: Mapped[int] = mapped_column(ForeignKey('departments.id'))
    target: Mapped[Department] = relationship(back_populates='rules')
    alerts: Mapped[list[Alert]] = relationship(back_populates='rule')
    tickets: Mapped[list[Ticket]] = relationship(back_populates='rule')
