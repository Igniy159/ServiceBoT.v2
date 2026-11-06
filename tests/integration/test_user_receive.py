import pytest

from app.errors import AuthorizeError
from app.schemas.schemas_user import ReceiveUser
from app.usecase import UserUseCase

@pytest.mark.asyncio
async def test_executors_not_receive_users(users,session):
    cmd = ReceiveUser()
    for user in users.executors():
        use_case = UserUseCase(session,user)
        with pytest.raises(AuthorizeError):
            await use_case.receive(cmd)

@pytest.mark.asyncio
async def test_employee_not_receive_users(users,session):
    cmd = ReceiveUser()
    use_case = UserUseCase(session,users.employee)
    with pytest.raises(AuthorizeError):
        await use_case.receive(cmd)

@pytest.mark.asyncio
async def test_admin_receive_all_users(users,session,user_factory):
    cmd = ReceiveUser()
    use_case =  UserUseCase(session,users.admin)
    await user_factory(users.executors())
    view_users = await use_case.receive(cmd)
    assert set(u.name for u in view_users) == set(u.name for u in users.executors())

@pytest.mark.asyncio
async def test_admin_receives_active_users(users, session, receive_users, user_factory):
    cmd = ReceiveUser(is_active=True)
    await user_factory([users.admin])
    use_case = UserUseCase(session, users.admin)

    result = await use_case.receive(cmd)
    names = {item.name for item in result}
    assert names == {
        users.admin.name,
        'Alice',
        'Bob',
        'Dave',
    }
    assert 'Carol' not in names

@pytest.mark.asyncio
async def test_admin_receives_inactive_users(users, session, receive_users, user_factory):
    cmd = ReceiveUser(is_active=False)
    await user_factory([users.admin])
    use_case = UserUseCase(session, users.admin)
    result = await use_case.receive(cmd)
    assert result[0].name == 'Carol'

@pytest.mark.asyncio
async def test_receive_active_and_inactive_users(
    session,
    users,
    user_factory,
        receive_users,
):
    await user_factory([users.admin])
    use_case = UserUseCase(session, users.admin)
    result = await use_case.receive(
        ReceiveUser(is_active=None)
    )
    assert {item.name for item in result} == {
        users.admin.name,
        'Alice',
        'Bob',
        'Carol',
        'Dave',
    }

@pytest.mark.asyncio
async def test_receive_by_user_id(
    session,
    users,
    user_factory,
    receive_users,
):
    await user_factory([users.admin])
    target = receive_users['alice']
    use_case = UserUseCase(session, users.admin)
    result = await use_case.receive(
        ReceiveUser(user_id=target.id)
    )
    assert len(result) == 1
    assert result[0].id == target.id
    assert result[0].name == 'Alice'

@pytest.mark.asyncio
async def test_receive_by_tg_id(
    session,
    users,
    user_factory,
    receive_users,
):
    await user_factory([users.admin])
    target = receive_users['bob']
    use_case = UserUseCase(session, users.admin)
    result = await use_case.receive(
        ReceiveUser(tg_id=target.tg_id)
    )
    assert len(result) == 1
    assert result[0].id == target.id

@pytest.mark.asyncio
async def test_receive_by_branch(
    session,
    users,
    user_factory,
    receive_users,
):
    await user_factory([users.admin])
    branch_id = receive_users['alice'].branch_id
    use_case = UserUseCase(session, users.admin)
    result = await use_case.receive(
        ReceiveUser(branch_id=branch_id)
    )
    assert {item.name for item in result} == {
        'Alice',
        'Dave',
    }

@pytest.mark.asyncio
async def test_receive_by_department(session, users, user_factory):
    await user_factory([users.admin])
    await user_factory(users.executors())
    use_case = UserUseCase(session, users.admin)
    depart_id = users.ars.department_id
    cmd = ReceiveUser(department_id=depart_id)
    result = await use_case.receive(cmd)
    assert len(result) == 1
    assert result[0].name == users.ars.name

@pytest.mark.asyncio
async def test_receive_order_and_pagination(
    session,
    users,
    user_factory,
    receive_users,
):
    await user_factory([users.admin])
    use_case = UserUseCase(session, users.admin)
    result = await use_case.receive(
        ReceiveUser(
            role_id=4,
            is_active=True,
            limit=2,
            offset=0,
        )
    )
    assert [item.name for item in result] == [
        'Alice',
        'Bob',
    ]


@pytest.mark.asyncio
async def test_manager_receive_only_own_branch(session, users, receive_users):
    #dave is manager, alice is active user
    use_case = UserUseCase(session, receive_users['dave'])
    cmd = ReceiveUser()
    result = await use_case.receive(cmd)
    names =  {u.name for u in result}
    assert names == {'Alice','Dave'}

@pytest.mark.asyncio
async def test_manager_can_not_receive_other_branch(session, users, receive_users, branches):
    use_case = UserUseCase(session, receive_users['dave'])
    cmd = ReceiveUser(branch_id=branches.wolf.id)
    with pytest.raises(AuthorizeError):
        await use_case.receive(cmd)

