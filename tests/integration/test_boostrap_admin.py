import pytest
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.errors import AuthorizeError
from app.models import User, Role
from app.schemas.schemas_user import Registry
from app.usecase import RegistrationUseCase


@pytest.mark.asyncio
async def test_first_admin_registry(session):
    use_case = RegistrationUseCase(session)
    cmd = Registry(name='Имя админа',
                   email='my_email@.com',
                   password='111111',
                   tg_id=987654)
    res = await use_case.boostrap_admin_registry(cmd)
    assert res.name == 'Имя админа'
    assert res.email == 'my_email@.com'
    assert res.tg_id == 987654
    res = await session.execute(select(User).options(joinedload(User.role)))
    user = res.scalars().one()
    assert user.password_hash != '111111'
    assert user.role.name == 'Админ'


@pytest.mark.asyncio
async def test_double_admin_registry(session):
    use_case = RegistrationUseCase(session)
    cmd = Registry(name='Имя админа',
                   email='my_email@.com',
                   password='111111',
                   tg_id=987654)
    await use_case.boostrap_admin_registry(cmd)
    with pytest.raises(AuthorizeError):
        await use_case.boostrap_admin_registry(cmd)

@pytest.mark.asyncio
async def test_db_has_not_empty(session, users):
    session.add_all(users.executors())
    await session.flush()
    use_case = RegistrationUseCase(session)
    cmd = Registry(name='Имя админа',
                   email='my_email@.com',
                   password='111111',
                   tg_id=987654)
    with pytest.raises(AuthorizeError):
        await use_case.boostrap_admin_registry(cmd)
