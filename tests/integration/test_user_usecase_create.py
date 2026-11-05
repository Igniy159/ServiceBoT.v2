import pytest
from sqlalchemy import select
from app.errors import AuthorizeError, AlreadyExistsError
from app.models import User, Role
from app.schemas.schemas_user import CreateUser
from app.usecase.usecase_user import UserUseCase


@pytest.mark.asyncio
async def test_admin_can_create_owner_user(session, users):
    cmd = CreateUser(name='Новый владелец',
                     tg_id=159,
                     role_id=2)
    use_case = UserUseCase(session,users.admin)
    res = await use_case.create(cmd)
    assert isinstance(res, User)
    assert res.name == 'Новый владелец'
    assert res.is_active is True
    assert res.tg_id == 159

@pytest.mark.asyncio
async def test_executors_can_not_create_user(session, users):
    cmd = CreateUser(name='Новый владелец',
                     tg_id=159,
                     role_id=2)
    for user in users.executors():
        use_case = UserUseCase(session, user)
        with pytest.raises(AuthorizeError):
            await use_case.create(cmd)

@pytest.mark.asyncio
async def test_employee_can_not_create_user(session, users):
    cmd = CreateUser(name='Новый владелец',
                     tg_id=159,
                     role_id=2)
    use_case = UserUseCase(session, users.employee)
    with pytest.raises(AuthorizeError):
        await use_case.create(cmd)

@pytest.mark.asyncio
async def test_manager_create_employee(session, users, branches, branch_factory, user_factory):
    write_branch = await branch_factory([branches.dragon])
    branch = write_branch[0]
    await user_factory([users.manager])
    users.manager.branch = branch
    cmd = CreateUser(name='Василий Игнатович',
                     tg_id=456,
                     role_id=4,
                     branch_id=branch.id)
    use_case = UserUseCase(session, users.manager)
    res = await use_case.create(cmd)
    assert isinstance(res, User)
    assert res.name == 'Василий Игнатович'
    assert res.is_active is True
    assert res.tg_id == 456
    assert res.branch_id == branch.id

    res = await session.execute(
        select(Role.name).join(User.role).where(User.name == 'Василий Игнатович'))
    user_role = res.scalars().one()
    assert user_role == 'Сотрудник филиала'

@pytest.mark.asyncio
async def test_double_create_new_user(session,users):
    cmd = CreateUser(name='Новый владелец',
                     tg_id=159,
                     role_id=2)
    use_case = UserUseCase(session,users.admin)
    await use_case.create(cmd)
    with pytest.raises(AlreadyExistsError):
        await use_case.create(cmd)

@pytest.mark.asyncio
async def test_manager_can_not_create_other_branch_user(
        session,users,branches, branch_factory, user_factory):
    await branch_factory([branches.dragon, branches.wolf])
    await user_factory([users.manager])
    users.manager.branch = branches.dragon
    cmd = CreateUser(name='Василий Игнатович',
                     tg_id=456,
                     role_id=4,
                     branch_id=branches.wolf.id)
    use_case = UserUseCase(session, users.manager)
    with pytest.raises(AuthorizeError):
        await use_case.create(cmd)

