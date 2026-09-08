from decimal import Decimal
from uuid import UUID
from enum import Enum
from datetime import datetime
from sqlalchemy import Enum as SqlEnum, Numeric
from sqlalchemy import ForeignKey, UUID as SqlUUID, DateTime as SqlDatetime
from sqlalchemy.dialects.postgresql import JSONB

from _not_use.alchemy_connect import engine
from sqlalchemy.orm import Session, DeclarativeBase, Mapped, mapped_column

con = engine.connect()
session = Session(con)
session_1 = Session(engine)
#можно создать сессию как и из соединения, так и передать engine

#
# class Base(DeclarativeBase):
#     """Создаём декларативный класс для объявления ORM моделей"""
#     pass
#
# class Roles(Enum):
#     OWNER = 'owner'
#     EMPLOYEE = 'employee'
#     SPECIALIST = 'specialist'
#     MANAGER = 'manager'
#
# class TestSpecificType(Base):
#     __tablename__ = 'not_use'
#     uuid: Mapped[UUID] = mapped_column(SqlUUID, primary_key=True)
#     amount: Mapped[Decimal] = mapped_column(Numeric,nullable=True)
#     another: Mapped[dict] = mapped_column(JSONB)
#     created_at: Mapped[datetime] = mapped_column(SqlDatetime(timezone=True))
#
# class Branch(Base):
#     __tablename__ = 'branches'
#     id: Mapped[int]= mapped_column(primary_key=True, autoincrement=True)
#     name: Mapped[str] = mapped_column(nullable=False)
#     is_active: Mapped[bool] = mapped_column(default=True)
#
# class Department(Base):
#     __tablename__  = 'departments'
#     id: Mapped[int]= mapped_column(primary_key=True, autoincrement=True)
#     name: Mapped[str] = mapped_column(nullable=False)
#     is_active: Mapped[bool] = mapped_column(default=True)
#
# class User(Base):
#     __tablename__ = 'users'
#     id: Mapped[int]= mapped_column(primary_key=True, autoincrement=True)
#     name: Mapped[str] = mapped_column(nullable=False)
#     branch_id: Mapped[int| None] = mapped_column(ForeignKey('branches.id'))
#     depart_id: Mapped[int| None] = mapped_column(ForeignKey('departments.id'))
#     role: Mapped[Roles] = mapped_column(SqlEnum(Roles))
#     is_active: Mapped[bool] = mapped_column(default=True)
