from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy import String, ForeignKey, Table, Column, CheckConstraint, Enum

from app.enums import ClassRule
from app.models.base import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship

if TYPE_CHECKING:
    from app.models.model_user import User

class Role(Base):
    __tablename__ = 'roles'
    __table_args__ = (CheckConstraint('NOT (need_branch AND need_department)',
                                      'not_depart_and_branch_on_role'),)
    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    name: Mapped[str] = mapped_column(String,unique=True)
    users: Mapped[list[User]] = relationship(back_populates='role')

    need_branch: Mapped[bool]
    need_department: Mapped[bool]
    responsibilities: Mapped[list[ClassRule]] = relationship(secondary='role_responsibility')
    notifications: Mapped[list[ClassRule]] = relationship(secondary='role_subscribers')

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
role_responsibility = Table(
    'role_responsibility',
    Base.metadata,
    Column('role_id',ForeignKey('roles.id'),primary_key=True),
    Column('class_rule',Enum(ClassRule),primary_key=True)
)
role_subscribers = Table(
    'role_subscribers',
    Base.metadata,
    Column('role_id',ForeignKey('roles.id'),primary_key=True),
    Column('class_rule',Enum(ClassRule),primary_key=True)
)