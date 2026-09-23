"""preset_permissions

Revision ID: 847bc6cdc951
Revises: 2a7f34bd0736
Create Date: 2026-09-21 05:36:50.919429

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '847bc6cdc951'
down_revision: Union[str, Sequence[str], None] = '2a7f34bd0736'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

set_permissions = frozenset([
    'alert:create',
   'alert:receive',
   'branch:create',
   'branch:rename',
   'branch:receive',
   'branch:deactivate',
   'department:create',
   'department:receive',
   'department:deactivate',
   'role:create',
   'rule:create',
   'rule:delete',
   'rule:receive',
   'ticket:create',
    'ticket:confirm',
    'ticket:accept',
    'ticket:close',
    'ticket:cancel',
   'ticket:receive',
    'full_access'])

permissions_table = sa.table('permissions',
                             sa.column('name', sa.String()))

def upgrade() -> None:
    """Upgrade schema."""
    permissions = [{'name': p} for p in set_permissions]
    op.bulk_insert(permissions_table,permissions)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(permissions_table.delete())
