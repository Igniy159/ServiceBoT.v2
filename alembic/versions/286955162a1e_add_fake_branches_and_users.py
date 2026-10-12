"""add_fake_branches_and_users

Revision ID: 286955162a1e
Revises: 85bfb07828ab
Create Date: 2026-09-30 11:56:14.227541

"""
from os import name
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Branch, User

# revision identifiers, used by Alembic.
revision: str = '286955162a1e'
down_revision: Union[str, Sequence[str], None] = '85bfb07828ab'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def get_fake_branches()->list[Branch]:
    branches = [
        Branch(name='Летящий дракон'),
        Branch(name='Раненный вепрь'),
        Branch(name='Гарцующий пони'),
        Branch(name='Старый волк')
    ]
    return branches

def get_fake_users()->list[User]:
    users = [
        User(name='Великий АДМИН',tg_id=8752047609,role_id=1),
        User(name='Владыка Системы', tg_id= 38923424542, role_id=2),
        User(name='Управляющий драконом',tg_id=2934632345, role_id=3,branch_id=1),
        User(name='Управляющий вепрем', tg_id=29134643342, role_id=3, branch_id=2),
        User(name='Культист дракона', tg_id=234234446354, role_id=4, branch_id=1),
        User(name='Прислужник волка', tg_id=2312446354, role_id=4, branch_id=4),
        User(name='Служащий вепрю',tg_id=1352436543,role_id=4, branch_id=2),
        User(name='Великий исправитель',tg_id=2422434553, role_id=5,department_id=6),
        User(name='Страж порядка', tg_id= 134112352313, role_id=6,department_id=4),
        User(name='Повелитель молний', tg_id=13412432213, role_id=7, department_id=7),
        User(name='Доставляющий грузы', tg_id=134344537313, role_id=8, department_id=8),
        User(name='Считающий золото', tg_id=671387533, role_id=9, department_id=9),
        User(name='Хранящий блага', tg_id=987646847313, role_id=10, department_id=10),
        User(name='Возглашающий истину', tg_id=21242531, role_id=11, department_id=11),
        User(name='Умиротворитель приходящих', tg_id=34562847313, role_id=12, department_id=12),
        User(name='Нанимающий адептов', tg_id=4245233847313, role_id=13, department_id=5),
    ]
    return users




def upgrade() -> None:
    """Upgrade schema."""
    with Session(bind=op.get_bind()) as session:
        branches = get_fake_branches()
        session.add_all(branches)
        users = get_fake_users()
        session.add_all(users)
        session.commit()



def downgrade() -> None:
    """Downgrade schema."""
    with Session(bind=op.get_bind()) as session:
        branches = session.scalars(
            select(Branch)
        ).all()
        session.delete(branches)
        users = session.scalars(
            select(User)
        ).all()
        session.delete(users)
