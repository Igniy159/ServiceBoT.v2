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
def user_repo(session:AsyncSession):
    return UserRepo(session)
