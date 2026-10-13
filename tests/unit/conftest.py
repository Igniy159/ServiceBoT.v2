import pytest

from app.enums import State, Severity
from app.models import Ticket, User


@pytest.fixture
def fake_ticket(state: State) -> Ticket:
    return Ticket(rule_id=1,
                  branch_id=1,
                  creator_id=2,
                  comment='Новая заявка!',
                  state=state,
                  severity=Severity.FULL_FAILURE)

@pytest.fixture
def creator()-> User:
    return User(name='Линейный сотрудник!',
                tg_id=1432324,
                role_id=4,
                branch_id=1)

@pytest.fixture
def manager() -> list[User]:
    return [User(name='Действующий менеджер!',
                tg_id=123456,
                role_id=3,
                branch_id=1)]

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
def assigned_to()->User:
    return User(name='Действующий специалист!',
                 tg_id=987654,
                 role_id=5,
                 department_id=2)


@pytest.fixture
def owner() -> User:
    return User(name='Операционный директор',
                tg_id=155483,
                role_id=1)
