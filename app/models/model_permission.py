from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy import String, ForeignKey,Table, Column
from app.models.base import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship

if TYPE_CHECKING:
    from app.models.model_user import User

class Role(Base):
    __tablename__ = 'roles'
    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    name: Mapped[str] = mapped_column(String,unique=True)
    users: Mapped[list[User]] = relationship(back_populates='role')

    permissions: Mapped[list[Permission]] = relationship(back_populates='roles',
                                                         secondary='role_permissions')


class Permission(Base):
    __tablename__ = 'permissions'
    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    name: Mapped[str] = mapped_column(String, unique=True)

    roles: Mapped[list[Role]] = relationship(back_populates='permissions',
                                             secondary='role_permissions')

role_permissions = Table(
    "role_permissions",
    Base.metadata,
    Column("role_id", ForeignKey("roles.id"), primary_key=True),
    Column("permission_id", ForeignKey("permissions.id"), primary_key=True),
)
