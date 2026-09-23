"""preset migration departments

Revision ID: 317b24b722f0
Revises: f7cd62729718
Create Date: 2026-09-21 02:52:24.548100

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '317b24b722f0'
down_revision: Union[str, Sequence[str], None] = 'f7cd62729718'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    department = sa.table(
        "departments",
        sa.column("name", sa.String()),
        sa.column('is_active', sa.Boolean())
    )

    departments = [
        {"name": "Руководство", 'is_active': True},
        {"name": "Служба безопасности",'is_active': True},
        {"name": "HR отдел",'is_active': True},
        {"name": "ARS отдел",'is_active': True},
        {"name": "IT отдел",'is_active': True},
        {"name": "Отдел снабжения",'is_active': True},
        {"name": "Бухгалтерия",'is_active': True},
        {"name": "Склад",'is_active': True},
        {"name": "Маркетинг",'is_active': True},
        {"name": "Сервис менеджер",'is_active': True},
    ]

    op.bulk_insert(department, departments)

def downgrade() -> None:
    """Downgrade schema."""
    department = sa.table(
        "departments",
        sa.column("name", sa.String()),
    )
    op.execute(
        department.delete().where(
            department.c.name.in_([
                "Руководство",
                "Служба безопасности",
                "HR отдел",
                "ARS отдел",
                "IT отдел",
                "Отдел снабжения",
                "Бухгалтерия",
                "Склад",
                "Маркетинг",
                "Сервис менеджер",
            ])
        )
    )
