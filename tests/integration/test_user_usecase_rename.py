import pytest

from app.errors import AuthorizeError, ResourceNotFound
from app.schemas.schemas_user import RenameUser
from app.usecase import UserUseCase


@pytest.mark.asyncio
async def test_admin_can_rename_user(session, users, user_factory):
    use_case = UserUseCase(session,users.admin)
    res = await user_factory([users.hr])
    user_hr = res[0]
    old_name = user_hr.name
    cmd = RenameUser(user_id=user_hr.id,
                     new_name='Измененное имя')
    renamed_user = await use_case.rename(cmd)
    assert renamed_user.name == 'Измененное имя'
    assert old_name != 'Измененное имя'

@pytest.mark.asyncio
async def test_executors_can_not_rename_user(session, users, user_factory):
    res = await user_factory([users.hr])
    user_hr = res[0]
    cmd = RenameUser(user_id=user_hr.id,
                     new_name='Измененное имя')
    for user in users.executors():
        use_case = UserUseCase(session, user)
        with pytest.raises(AuthorizeError):
            await use_case.rename(cmd)

@pytest.mark.asyncio
async def test_employee_can_not_rename_user(session, users, user_factory):
    res = await user_factory([users.hr])
    user_hr = res[0]
    cmd = RenameUser(user_id=user_hr.id,
                     new_name='Измененное имя')
    use_case = UserUseCase(session, users.employee)
    with pytest.raises(AuthorizeError):
        await use_case.rename(cmd)

@pytest.mark.asyncio
async def test_manager_rename_employee(session, users, branches, branch_factory, user_factory):
    await branch_factory([branches.dragon])
    await user_factory([users.manager, users.employee])
    users.manager.branch = branches.dragon
    users.employee.branch = branches.dragon
    old_name = users.employee.name
    use_case = UserUseCase(session, users.manager)
    cmd = RenameUser(user_id=users.employee.id,
                     new_name='Измененное имя')
    renamed_user = await use_case.rename(cmd)
    assert renamed_user.name == 'Измененное имя'
    assert renamed_user.name != old_name


@pytest.mark.asyncio
async def test_double_rename_user(session,users, user_factory):
    use_case = UserUseCase(session,users.admin)
    res = await user_factory([users.hr])
    user_hr = res[0]
    old_name = user_hr.name
    cmd = RenameUser(user_id=user_hr.id,
                     new_name='Измененное имя')
    await use_case.rename(cmd)
    renamed_user = await use_case.rename(cmd)
    assert renamed_user.name == 'Измененное имя'
    assert old_name != 'Измененное имя'

@pytest.mark.asyncio
async def test_manager_can_not_rename_other_branch_user(
        session,users,branches, branch_factory, user_factory):
    await branch_factory([branches.dragon, branches.wolf])
    await user_factory([users.manager, users.employee])
    users.manager.branch = branches.dragon
    users.employee.branch = branches.wolf
    use_case = UserUseCase(session, users.manager)
    cmd = RenameUser(user_id=users.employee.id,
                     new_name='Измененное имя')
    with pytest.raises(AuthorizeError):
        await use_case.rename(cmd)

@pytest.mark.asyncio
async def test_user_not_found(session,users):
    use_case = UserUseCase(session,users.admin)
    cmd = RenameUser(user_id=999,
                     new_name='Измененное имя')
    with pytest.raises(ResourceNotFound):
        await use_case.rename(cmd)
