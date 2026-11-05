import pytest
from app.errors import AuthorizeError, ResourceNotFound, ProhibitSelfModification
from app.schemas.schemas_user import  ChangeUser
from app.usecase import UserUseCase


@pytest.mark.asyncio
async def test_admin_can_change_user(session, users, user_factory):
    use_case = UserUseCase(session,users.admin)
    await user_factory([users.hr])

    ars_role_id = users.ars.role_id
    ars_id = users.ars.department_id

    cmd = ChangeUser(user_id=users.hr.id,
                     role_id=ars_role_id,
                     department_id=ars_id,
                     branch_id=None)
    changed = await use_case.change(cmd)
    assert changed.department_id == ars_id
    assert changed.role_id == ars_role_id

@pytest.mark.asyncio
async def test_owner_can_change_user(session, users, user_factory, branches, branch_factory):
    await branch_factory(branches.all())
    use_case = UserUseCase(session,users.owner)
    users.employee.branch = branches.dragon
    await user_factory([users.employee])
    cmd = ChangeUser(user_id=users.employee.id,
                     role_id=users.employee.role_id,
                     department_id=None,
                     branch_id=branches.wolf.id)

    changed = await use_case.change(cmd)
    assert changed.branch_id == branches.wolf.id


@pytest.mark.asyncio
async def test_other_can_not_change_user(session, users, user_factory):
    await user_factory([users.hr])
    ars_role_id = users.ars.role_id
    ars_id = users.ars.department_id
    cmd = ChangeUser(user_id=users.hr.id,
                     role_id=ars_role_id,
                     department_id=ars_id,
                     branch_id=None)
    all_users = [users.manager,users.employee]
    all_users.extend(users.executors())
    for user in all_users:
        use_case = UserUseCase(session, user)
        with pytest.raises(AuthorizeError):
            await use_case.change(cmd)


@pytest.mark.asyncio
async def test_double_change_user(session,users, user_factory):
    use_case = UserUseCase(session,users.admin)
    await user_factory([users.hr])
    ars_role_id = users.ars.role_id
    ars_id = users.ars.department_id

    cmd = ChangeUser(user_id=users.hr.id,
                     role_id=ars_role_id,
                     department_id=ars_id,
                     branch_id=None)
    await use_case.change(cmd)
    changed = await use_case.change(cmd)
    assert changed.department_id == ars_id
    assert changed.role_id == ars_role_id

@pytest.mark.asyncio
async def test_change_user_not_found(session,users):
    use_case = UserUseCase(session,users.admin)
    ars_role_id = users.ars.role_id
    ars_id = users.ars.department_id

    cmd = ChangeUser(user_id=999,
                     role_id=ars_role_id,
                     department_id=ars_id,
                     branch_id=None)
    with pytest.raises(ResourceNotFound):
        await use_case.change(cmd)


@pytest.mark.asyncio
async def test_self_modification(session, users, user_factory):
    await user_factory([users.admin])
    ars_role_id = users.ars.role_id
    ars_id = users.ars.department_id
    use_case = UserUseCase(session, users.admin)
    cmd = ChangeUser(user_id=users.admin.id,
                     role_id=ars_role_id,
                     department_id=ars_id,
                     branch_id=None)
    with pytest.raises(ProhibitSelfModification):
        await use_case.change(cmd)
