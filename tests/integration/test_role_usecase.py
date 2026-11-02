import pytest
from app.enums import ClassRule
from app.schemas.schemas_role import CreateRole
from app.usecase import RoleUseCase
from app.errors import AuthorizeError, IncorrectFieldsCmd, AlreadyExistsError


@pytest.mark.asyncio
async def test_only_admin_create_new_role(users,session):
    use_case = RoleUseCase(session,users.admin)
    cmd = CreateRole(name="Тестовая роль",
                     need_branch=True,
                     need_department=False,
                     responsibilities={ClassRule.ALL},
                     subscriptions={ClassRule.ALL},
                     permissions={'full_access'})
    res = await use_case.create(cmd)
    assert res.name == 'Тестовая роль'


@pytest.mark.asyncio
async def test_other_not_created_role(users,session):
    cmd = CreateRole(name="Тестовая роль",
                     need_branch=True,
                     need_department=False,
                     responsibilities={ClassRule.ALL},
                     subscriptions={ClassRule.ALL},
                     permissions={'full_access'})
    for user in users.not_admin():
        use_case = RoleUseCase(session, user)
        with pytest.raises(AuthorizeError):
            await use_case.create(cmd)

@pytest.mark.asyncio
async def test_role_not_have_branch_and_dep(users,session):
    use_case = RoleUseCase(session,users.admin)
    cmd = CreateRole(name="Тестовая роль",
                     need_branch=True,
                     need_department=True,
                     responsibilities={ClassRule.ALL},
                     subscriptions={ClassRule.ALL},
                     permissions={'full_access'})
    with pytest.raises(IncorrectFieldsCmd):
        await use_case.create(cmd)

@pytest.mark.asyncio
async def test_role_have_only_incorrect_permission(users,session):
    use_case = RoleUseCase(session,users.admin)
    cmd = CreateRole(name="Тестовая роль",
                     need_branch=True,
                     need_department=False,
                     responsibilities={ClassRule.ALL},
                     subscriptions={ClassRule.ALL},
                     permissions={'incorrect_value'})
    cmd1 = CreateRole(name="Тестовая роль",
                     need_branch=True,
                     need_department=False,
                     responsibilities={ClassRule.ALL},
                     subscriptions={ClassRule.ALL},
                     permissions={'full_access','incorrect_value'})
    with pytest.raises(IncorrectFieldsCmd):
        await use_case.create(cmd)
    with pytest.raises(IncorrectFieldsCmd):
        await use_case.create(cmd1)

@pytest.mark.asyncio
async def test_role_not_unique_name(users,session):
    use_case = RoleUseCase(session,users.admin)
    cmd = CreateRole(name="Тестовая роль",
                     need_branch=True,
                     need_department=False,
                     responsibilities={ClassRule.ALL},
                     subscriptions={ClassRule.ALL},
                     permissions={'full_access'})
    await use_case.create(cmd)
    with pytest.raises(AlreadyExistsError):
        await use_case.create(cmd)
