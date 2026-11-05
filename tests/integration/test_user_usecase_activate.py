import pytest

from app.errors import AuthorizeError, ResourceNotFound, ProhibitSelfModification
from app.schemas.schemas_user import ActivateUser
from app.usecase import UserUseCase


@pytest.mark.asyncio
async def test_admin_can_activate_user(session, users, user_factory):
    use_case = UserUseCase(session,users.admin)
    users.hr.is_active = False
    res = await user_factory([users.hr])
    user_hr = res[0]
    cmd = ActivateUser(user_id=user_hr.id)
    activated_user = await use_case.activate(cmd)
    assert activated_user.is_active is True


@pytest.mark.asyncio
async def test_executors_can_not_activate_user(session, users, user_factory):
    users.hr.is_active = False
    res = await user_factory([users.hr])
    user_hr = res[0]
    cmd = ActivateUser(user_id=user_hr.id)
    for user in users.executors():
        use_case = UserUseCase(session, user)
        with pytest.raises(AuthorizeError):
            await use_case.activate(cmd)

@pytest.mark.asyncio
async def test_employee_can_not_activate_user(session, users, user_factory):
    users.hr.is_active = False
    res = await user_factory([users.hr])
    user_hr = res[0]
    cmd = ActivateUser(user_id=user_hr.id)
    use_case = UserUseCase(session, users.employee)
    with pytest.raises(AuthorizeError):
        await use_case.activate(cmd)

@pytest.mark.asyncio
async def test_manager_activate_employee(
        session, users, branches, branch_factory, user_factory):
    await branch_factory([branches.dragon])
    users.employee.is_active = False
    await user_factory([users.manager, users.employee])
    users.manager.branch = branches.dragon
    users.employee.branch = branches.dragon
    use_case = UserUseCase(session, users.manager)
    cmd = ActivateUser(user_id=users.employee.id)
    activated_user = await use_case.activate(cmd)
    assert activated_user.is_active is True


@pytest.mark.asyncio
async def test_double_activate_user(session,users, user_factory):
    use_case = UserUseCase(session,users.admin)
    res = await user_factory([users.hr])
    user_hr = res[0]
    cmd = ActivateUser(user_id=user_hr.id)
    await use_case.activate(cmd)
    deleted_user = await use_case.activate(cmd)
    assert deleted_user.is_active is True


@pytest.mark.asyncio
async def test_manager_can_not_act_other_branch_user(
        session,users,branches, branch_factory, user_factory):
    await branch_factory([branches.dragon, branches.wolf])
    await user_factory([users.manager, users.employee])
    users.manager.branch = branches.dragon
    users.employee.branch = branches.wolf
    use_case = UserUseCase(session, users.manager)
    cmd = ActivateUser(user_id=users.employee.id)
    with pytest.raises(AuthorizeError):
        await use_case.activate(cmd)

@pytest.mark.asyncio
async def test_activate_user_not_found(session,users):
    use_case = UserUseCase(session,users.admin)
    cmd = ActivateUser(user_id=999)
    with pytest.raises(ResourceNotFound):
        await use_case.activate(cmd)


@pytest.mark.asyncio
async def test_self_activate(session,users, user_factory):
    await user_factory([users.admin])
    use_case = UserUseCase(session, users.admin)
    cmd = ActivateUser(user_id=users.admin.id)
    with pytest.raises(ProhibitSelfModification):
        await use_case.activate(cmd)
