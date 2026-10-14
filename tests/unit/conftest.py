from unittest.mock import AsyncMock, Mock

import pytest

from app.enums import State, Severity, ClassRule
from app.models import Ticket, User, Role, Permission, Responsibility
from app.policy.authorize_user import Authorize
from app.policy.escalation_policy import EscalationPolicy
from app.policy.notification_policy import NotificationPolicy


@pytest.fixture
def ticket_factory():
    def factory(state: State) -> Ticket:
        return Ticket(
            rule_id=1,
            branch_id=1,
            creator_id=2,
            comment='Новая заявка!',
            state=state,
            severity=Severity.FULL_FAILURE
        )

    return factory

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
def managers()-> list[User]:
    return [User(name='Действующий менеджер!',
                tg_id=123456,
                role_id=3,
                branch_id=1),
            User(name='Менеджер стажер!',
                 tg_id=123453,
                 role_id=3,
                 branch_id=1)
            ]

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

@pytest.fixture
def authorize()-> Authorize:
    policy = Authorize(session=AsyncMock(),
                       actor=Mock())
    return policy


@pytest.fixture
def role_admin():
    return Role(id=1, name='роль админа',
                permissions=[Permission(name='full_access')],
                responsibilities= [Responsibility(role_id=1,class_rule=ClassRule.ALL)])

@pytest.fixture
def role_employee():
    return   Role(name='Сотрудник филиала',
         need_branch=True,
         need_department=False,
         permissions=[
         Permission(name='alert:create'),
         Permission(name='ticket:create')
         ],
        responsibilities = [],
        subscriptions = []
    )

@pytest.fixture
def notification():
    return NotificationPolicy(session=AsyncMock())

@pytest.fixture
def escalation()->EscalationPolicy:
    return EscalationPolicy(session=AsyncMock())

