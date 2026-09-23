"""preset_role

Revision ID: 1eb5591e0519
Revises: 847bc6cdc951
Create Date: 2026-09-22 05:47:26.026339

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from app.models import Role

# revision identifiers, used by Alembic.
revision: str = '1eb5591e0519'
down_revision: Union[str, Sequence[str], None] = '847bc6cdc951'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


owner = Role(name='Владелец',
             need_branch=False,
             need_department=False)

branch_manager = Role(name='Управляющий филиала',
             need_branch=True,
             need_department=False)

line_personal =  Role(name='Сотрудник филиала',
             need_branch=True,
             need_department=False)

department_manager = Role(name='Глава отдела',
             need_branch=False,
             need_department=True)

executor = Role(name='Сотрудник отдела',
             need_branch=False,
             need_department=True)

def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
