import pytest

from app.errors import IncorrectFieldsCmd, ResourceNotFound
from app.schemas.schemas_user import CreateUser
from app.usecase import UserUseCase


@pytest.mark.asyncio
async def test_incorrect_role_id(session,users):
    use_case = UserUseCase(session,users.admin)
    cmd = CreateUser(name='Тестовое имя',
                     tg_id=987,
                     role_id=999)
    with pytest.raises(ResourceNotFound):
        await use_case.validate_role_assignment(cmd)

@pytest.mark.asyncio
async def test_incorrect_branch_id(session,users):
    use_case = UserUseCase(session,users.admin)
    cmd = CreateUser(name='Тестовое имя',
                     tg_id=987,
                     role_id=1,
                     branch_id=999)
    with pytest.raises(ResourceNotFound):
        await use_case.validate_role_assignment(cmd)

@pytest.mark.asyncio
async def test_incorrect_depart_id(session,users):
    use_case = UserUseCase(session,users.admin)
    cmd = CreateUser(name='Тестовое имя',
                     tg_id=987,
                     role_id=1,
                     department_id=999)
    with pytest.raises(ResourceNotFound):
        await use_case.validate_role_assignment(cmd)

@pytest.mark.asyncio
async def test_role_have_branch_and_depart(session,users):
    use_case = UserUseCase(session,users.admin)
    cmd = CreateUser(name='Тестовое имя',
                     tg_id=987,
                     role_id=1,
                     department_id=1,
                     branch_id=1)
    with pytest.raises(IncorrectFieldsCmd):
        await use_case.validate_role_assignment(cmd)

