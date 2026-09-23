from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import VARCHAR, Enum as SqlEnum, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship


from app.models.base import Base
if TYPE_CHECKING:
    from app.models.model_ticket import Ticket
    from app.models.model_department import Department
    from app.models.model_branch import Branch
    from app.models.model_alert import Alert
    from app.models.model_permission import Role


class User(Base):
    __tablename__ = 'users'
    __table_args__ = (CheckConstraint('NOT (branch_id IS NOT NULL AND department_id IS NOT NULL)',
                                     'not_depart_and_branch_on_user'),
                      CheckConstraint('NOT (tg_id IS NULL AND email IS NULL)',
                                      'not null tg and email from user'))
    id: Mapped[int] = mapped_column(primary_key=True,autoincrement= True)
    name: Mapped[str] = mapped_column(VARCHAR(20), nullable=False)
    tg_id: Mapped[int] = mapped_column(unique=True, nullable=True)

    email: Mapped[str] = mapped_column(unique=True, nullable=True)
    password_hash: Mapped[str] = mapped_column(nullable=True)

    is_active: Mapped[bool] = mapped_column(default=True)
    role_id: Mapped[int] =  mapped_column(ForeignKey('roles.id'),nullable=True)
    role: Mapped[Role] = relationship(back_populates='users')
    branch_id: Mapped[int | None] = mapped_column(ForeignKey('branches.id'),nullable=True)
    department_id: Mapped[int | None] = mapped_column(ForeignKey('departments.id'),nullable=True)
    branch: Mapped[Branch | None] = relationship(back_populates='work_users')
    department: Mapped[Department | None] = relationship(back_populates='work_users')

    send_tickets: Mapped[list[Ticket]] = relationship(back_populates="user")
    assigned_tickets: Mapped[list[Ticket]] = relationship(back_populates='assigned_to')
    send_alerts: Mapped[list[Alert]] = relationship(back_populates='creator')
