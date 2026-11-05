from unittest.mock import Mock

import pytest

from app.errors import AuthorizeError
from app.policy.management_policy import ManagementPolicy


def test_allowed_management_operations():
    actor_role = Mock()
    actor_role.name = 'Админ'
    desired_role = Mock()
    names = ('Владелец','Управляющий филиала', 'Сотрудник филиала','Сотрудник ARS')
    for name in names:
        desired_role.name = name
        ManagementPolicy().check_management(actor_role,desired_role)

    actor_role.name = 'Владелец'
    names = ('Управляющий филиала', 'Сотрудник филиала', 'Сотрудник ARS')
    for name in names:
        desired_role.name = name
        ManagementPolicy().check_management(actor_role,desired_role)

    actor_role.name = 'Управляющий филиала'
    desired_role.name = 'Сотрудник филиала'
    ManagementPolicy().check_management(actor_role, desired_role)

def test_prohibit_management_operations():
    actor_role = Mock()
    actor_role.name = 'Админ'
    desired_role = Mock()
    desired_role.name = 'Админ'
    with pytest.raises(AuthorizeError):
        ManagementPolicy().check_management(actor_role, desired_role)


    actor_role.name = 'Владелец'
    names = ('Админ', 'Владелец')
    for name in names:
        desired_role.name = name
        with pytest.raises(AuthorizeError):
            ManagementPolicy().check_management(actor_role, desired_role)

    actor_role.name = 'Управляющий филиала'
    names = ('Админ','Владелец', 'Управляющий филиала', 'Сотрудник ARS')
    for name in names:
        desired_role.name = name
        with pytest.raises(AuthorizeError):
            ManagementPolicy().check_management(actor_role, desired_role)
