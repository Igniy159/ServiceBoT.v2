from unittest.mock import AsyncMock

import pytest

from app.enums import State, Severity
from app.models import Ticket, User
from app.policy.assigned_policy import AssignmentPolicy
from app.policy.base_policy import Policy


@pytest.fixture
def new_ticket() -> Ticket:
    return Ticket(rule_id=1,
                  branch_id=1,
                  creator_id=2,
                  comment='Новая заявка!',
                  state=State.NEW,
                  severity=Severity.FULL_FAILURE)


@pytest.fixture
def confirm_ticket() -> Ticket:
    return Ticket(rule_id=1,
                  branch_id=1,
                  creator_id=2,
                  comment='Подтвержденная заявка!',
                  state=State.CONFIRMED,
                  severity=Severity.FULL_FAILURE)


@pytest.fixture
def manager() -> User:
    return User(name='Действующий менеджер!',
                tg_id=123456,
                role_id=3,
                branch_id=1)


@pytest.fixture
def executors() -> list[User]:
    return [User(name='Действующий специалист!',
                 tg_id=987654,
                 role_id=5,
                 department_id=2),
            User(name='Действующий специалист 2!',
                 tg_id=548128,
                 role_id=5,
                 department_id=2)]


@pytest.fixture
def owner() -> User:
    return User(name='Операционный директор',
                tg_id=155483,
                role_id=1)




