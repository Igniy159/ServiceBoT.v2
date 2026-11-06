from os import name

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from typing_extensions import AsyncGenerator
from app.models import User, Branch
from app.repository.user_repo import UserRepo
from app.setting_app import setting_app

@pytest_asyncio.fixture(scope="session")
async def test_engine():
    engine = create_async_engine(setting_app.url_test_db)
    yield engine
    await engine.dispose()

@pytest.fixture
def session_factory(test_engine)->async_sessionmaker:
    factory = async_sessionmaker(
        test_engine,
        expire_on_commit=False)
    return factory


@pytest_asyncio.fixture
async def session(session_factory)->AsyncGenerator[AsyncSession]:
    async with session_factory() as session:
        try:
            yield session
        finally:
            await session.rollback()

@pytest_asyncio.fixture
async def user_factory(session):
    async def create_users(users: list[User]):
        session.add_all(users)
        await session.flush()
        return users
    return create_users

@pytest_asyncio.fixture
async def branch_factory(session):
    async def create_branch(branches: list[Branch]):
        session.add_all(branches)
        await session.flush()
        return branches
    return create_branch

@pytest_asyncio.fixture
async def receive_users(branch_factory, branches, user_factory):
    await branch_factory(branches.all())
    users = [User(
        name='Alice',
        tg_id=1001,
        role_id=4,
        department_id=None,
        branch_id=branches.dragon.id,
        is_active=True,
    ),
    User(
        name='Bob',
        tg_id=1002,
        role_id=4,
        department_id=None,
        branch_id=branches.wolf.id,
        is_active=True,
    ),
    User(
        name='Carol',
        tg_id=1003,
        role_id=4,
        department_id=None,
        branch_id=branches.dragon.id,
        is_active=False,
    ),
    User(
        name='Dave',
        tg_id=1004,
        role_id=3,
        department_id=None,
        branch_id=branches.dragon.id,
        is_active=True,
    )]

    await user_factory(users)

    return {
        'alice': users[0],
        'bob': users[1],
        'carol': users[2],
        'dave': users[3],
    }

