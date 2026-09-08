from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy import VARCHAR
from app.models.base import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship

if TYPE_CHECKING:
    from app.models.model_user import User
    from app.models.model_rule import Rule

class Department(Base):
    __tablename__ = 'departments'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(VARCHAR(20), unique=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    work_users: Mapped[list[User]] = relationship(back_populates='department')
    rules: Mapped[list[Rule]] = relationship(back_populates='target')
