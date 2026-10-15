import asyncio
import sys
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

@pytest.fixture
def admin():
    return [User(name="ADMIN",
                 tg_id=159357,
                 role_id=1)]


@pytest.fixture(scope="session", autouse=True)
def set_event_loop_policy():
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(
            asyncio.WindowsSelectorEventLoopPolicy())

@pytest.fixture
def user_repo(session:AsyncSession):
    return UserRepo(session)

@pytest_asyncio.fixture
async def preset_fake_db(branch_factory, user_factory, fake_users, fake_branches):
    branches = await branch_factory(fake_branches)
    fake_users[2].branch_id = branches[0].id
    fake_users[3].branch_id = branches[1].id
    fake_users[4].branch_id = branches[0].id
    fake_users[5].branch_id = branches[3].id
    fake_users[6].branch_id = branches[1].id

    await user_factory(fake_users)
    return fake_users, branches