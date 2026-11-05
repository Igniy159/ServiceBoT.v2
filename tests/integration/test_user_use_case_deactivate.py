import pytest

from app.errors import AuthorizeError, ResourceNotFound
from app.schemas.schemas_user import DeactivateUser
from app.usecase import UserUseCase


@pytest.mark.asyncio
async def test_admin_can_deactivate_user(session, users, user_factory):
    use_case = UserUseCase(session,users.admin)
    res = await user_factory([users.hr])
    user_hr = res[0]
    cmd = DeactivateUser(user_id=user_hr.id)
    deleted_user = await use_case.deactivate(cmd)
    assert deleted_user.is_active is False


@pytest.mark.asyncio
async def test_executors_can_not_deactivate_user(session, users, user_factory):
    res = await user_factory([users.hr])
    user_hr = res[0]
    cmd = DeactivateUser(user_id=user_hr.id)
    for user in users.executors():
        use_case = UserUseCase(session, user)
        with pytest.raises(AuthorizeError):
            await use_case.deactivate(cmd)

@pytest.mark.asyncio
async def test_employee_can_not_deactivate_user(session, users, user_factory):
    res = await user_factory([users.hr])
    user_hr = res[0]
    cmd = DeactivateUser(user_id=user_hr.id)
    use_case = UserUseCase(session, users.employee)
    with pytest.raises(AuthorizeError):
        await use_case.deactivate(cmd)

@pytest.mark.asyncio
async def test_manager_deactivate_employee(
        session, users, branches, branch_factory, user_factory):
    await branch_factory([branches.dragon])
    await user_factory([users.manager, users.employee])
    users.manager.branch = branches.dragon
    users.employee.branch = branches.dragon
    use_case = UserUseCase(session, users.manager)
    cmd = DeactivateUser(user_id=users.employee.id)
    deleted_user = await use_case.deactivate(cmd)
    assert deleted_user.is_active is False


@pytest.mark.asyncio
async def test_double_deactivate_user(session,users, user_factory):
    use_case = UserUseCase(session,users.admin)
    res = await user_factory([users.hr])
    user_hr = res[0]
    cmd = DeactivateUser(user_id=user_hr.id)
    deleted_user = await use_case.deactivate(cmd)
    assert deleted_user.is_active is False
    with pytest.raises(ResourceNotFound):
        await use_case.deactivate(cmd)


@pytest.mark.asyncio
async def test_manager_can_not_del_other_branch_user(
        session,users,branches, branch_factory, user_factory):
    await branch_factory([branches.dragon, branches.wolf])
    await user_factory([users.manager, users.employee])
    users.manager.branch = branches.dragon
    users.employee.branch = branches.wolf
    use_case = UserUseCase(session, users.manager)
    cmd = DeactivateUser(user_id=users.employee.id)
    with pytest.raises(AuthorizeError):
        await use_case.deactivate(cmd)

@pytest.mark.asyncio
async def test_user_not_found(session,users):
    use_case = UserUseCase(session,users.admin)
    cmd = DeactivateUser(user_id=999)
    with pytest.raises(ResourceNotFound):
        await use_case.deactivate(cmd)
