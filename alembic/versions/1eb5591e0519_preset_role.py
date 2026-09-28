"""preset_role

Revision ID: 1eb5591e0519
Revises: 847bc6cdc951
Create Date: 2026-09-22 05:47:26.026339
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.enums import ClassRule
from app.models import Role, Permission, Responsibility, Subscribe

# revision identifiers, used by Alembic.
revision: str = '1eb5591e0519'
down_revision: Union[str, Sequence[str], None] = '847bc6cdc951'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def matrix_role(session:Session):
    with session:
        permissions = {
            p.name: p
            for p in session.scalars(select(Permission))
        }

        roles = [
    Role(name="Админ",
                 need_branch=False,
                 need_department=False,
                permissions=[permissions['full_access']]),
    Role(name='Владелец',
         need_branch=False,
         need_department=False,
         permissions=[
            permissions['alert:create'],
            permissions['alert:receive'],
            permissions['branch:receive'],
            permissions['ticket:create'],
            permissions['ticket:confirm'],
            permissions['ticket:accept'],
            permissions['ticket:resolve'],
            permissions['ticket:close'],
            permissions['ticket:cancel'],
            permissions['ticket:receive'],
            permissions['user:create'],
            permissions['user:rename'],
            permissions['user:deactivate'],
            permissions['user:activate'],
            permissions['user:change'],
            permissions['user:receive']
                      ],
         responsibilities=[Responsibility(class_rule=ClassRule.ALL)],
         subscriptions=[Subscribe(class_rule=ClassRule.CRITICAL_ALERTS),
                        Subscribe(class_rule=ClassRule.SECURITY_ALERTS)]
         ),
    Role(name='Управляющий филиала',
         need_branch=True,
         need_department=False,
         permissions = [
        permissions['alert:create'],
        permissions['alert:receive'],
        permissions['ticket:create'],
        permissions['ticket:confirm'],
        permissions['ticket:close'],
        permissions['ticket:cancel'],
        permissions['ticket:receive'],
        permissions['user:create'],
        permissions['user:rename'],
        permissions['user:deactivate'],
        permissions['user:activate'],
        permissions['user:receive']
    ],
        responsibilities = [Responsibility(class_rule=ClassRule.ALL)],
        subscriptions = [Subscribe(class_rule=ClassRule.ALL)]
    ),
    Role(name='Сотрудник филиала',
         need_branch=True,
         need_department=False,
         permissions=[
         permissions['alert:create'],
         permissions['ticket:create']
         ],
        responsibilities = [],
        subscriptions = []

    ),
    Role(name='Сотрудник ARS',
         need_branch=False,
         need_department=True,
         permissions= [
             permissions['alert:receive'],
             permissions['ticket:accept'],
             permissions['ticket:resolve'],
             permissions['ticket:receive']
         ],
         responsibilities=[Responsibility(class_rule=ClassRule.CLIMATE),
                           Responsibility(class_rule=ClassRule.PLUMBING),
                           Responsibility(class_rule=ClassRule.FURNITURE),
                           Responsibility(class_rule=ClassRule.BAR_EQUIPMENT),
                           Responsibility(class_rule=ClassRule.REFRIGERATION)],
         subscriptions=[]
         ),
    Role(name='Сотрудник СБ',
         need_branch=False,
         need_department=True,
         permissions=[
             permissions['alert:receive'],
             permissions['ticket:accept'],
             permissions['ticket:resolve'],
             permissions['ticket:receive']
         ],
         responsibilities=[Responsibility(class_rule=ClassRule.SECURITY_REQUEST)],
         subscriptions=[Subscribe(class_rule=ClassRule.SECURITY_ALERTS)]
         ),
    Role(name='Сотрудник IT',
         need_branch=False,
         need_department=True,
         permissions=[
             permissions['ticket:accept'],
             permissions['ticket:resolve'],
             permissions['ticket:receive']
         ],
         responsibilities=[Responsibility(class_rule=ClassRule.IT_REQUEST)],
         subscriptions=[]
         ),
    Role(name='Сотрудник снабжения',
         need_branch=False,
         need_department=True,
         permissions=[
             permissions['ticket:accept'],
             permissions['ticket:resolve'],
             permissions['ticket:receive']
         ],
         responsibilities=[Responsibility(class_rule=ClassRule.INVENTORY_REQUEST)],
         subscriptions=[]
         ),
    Role(name='Бухгалтер',
         need_branch=False,
         need_department=True,
         responsibilities=[],
         permissions=[
             permissions['alert:receive']
         ],
         subscriptions=[Subscribe(class_rule=ClassRule.CASH_ALERTS)]
         ),
    Role(name='Сотрудник склада',
         need_branch=False,
        need_department=True,
         permissions=[
             permissions['ticket:accept'],
             permissions['ticket:resolve'],
             permissions['ticket:receive']
         ],
         responsibilities=[Responsibility(class_rule=ClassRule.STORE_REQUEST)],
         subscriptions=[]
         ),
    Role(name='Сотрудник маркетинга',
         need_branch=False,
         need_department=True,
         permissions=[
             permissions['ticket:accept'],
             permissions['ticket:resolve'],
             permissions['ticket:receive']
         ],
         responsibilities=[Responsibility(class_rule=ClassRule.MARKETING_REQUEST)],
         subscriptions=[]
         ),
    Role(name='Сервис менеджер',
         need_branch=False,
        need_department=True,
         permissions=[
             permissions['alert:receive']
         ],
         responsibilities=[],
         subscriptions=[Subscribe(class_rule=ClassRule.SERVICE_ALERTS)]
         ),
    Role(name='Сотрудник HR',
         need_branch=False,
        need_department=True,
         permissions=[
             permissions['alert:receive']
         ],
         responsibilities=[],
         subscriptions=[Subscribe(class_rule=ClassRule.HR_ALERTS)]
         ),
    ]
    return roles


def upgrade() -> None:
    """Upgrade schema."""
    with Session(bind=op.get_bind()) as session:
        roles = matrix_role(session)
        session.add_all(roles)
        session.commit()

def downgrade() -> None:
    """Downgrade schema."""
    with Session(bind=op.get_bind()) as session:
        roles = session.scalars(
            select(Role)
        ).all()
        session.delete(roles)
