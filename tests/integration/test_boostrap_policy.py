import pytest
from app.policy.boostrap_policy import BoostrapPolicy
from tests.conftest import FakeUsers


@pytest.mark.asyncio
async def test_has_user_in_db(session, user_factory):
    policy = BoostrapPolicy
    res = await policy.has_user_in_db(session)
    admin = [FakeUsers.admin]
    assert res is False
    await user_factory(admin) #write admin in DB
    res = await policy.has_user_in_db(session)
    assert res is True

@pytest.mark.asyncio
async def test_get_admin_id(session):
    policy = BoostrapPolicy
    role_admin_id = await policy.get_admin_id(session)
    #role admin in preset role. Preset role not mutable migration!
    assert role_admin_id == 1
