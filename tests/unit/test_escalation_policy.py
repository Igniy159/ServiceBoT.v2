from unittest.mock import AsyncMock
import pytest

from app.enums import State


@pytest.mark.asyncio
async def test_resolve_state_if_manager(escalation, manager):
    escalation.get_branch_manager = AsyncMock(return_value=manager)
    res = await escalation.resolve_state(1, {'ticket:create',})
    assert res == State.NEW

@pytest.mark.asyncio
async def test_resolve_state_if_not_manager(escalation):
    escalation.get_branch_manager = AsyncMock()
    escalation.get_branch_manager.return_value = None
    res = await escalation.resolve_state(1, {'ticket:create',})
    assert res == State.CONFIRMED

@pytest.mark.asyncio
async def test_resolve_state_if_user_have_confirm(escalation, manager):
    escalation.get_branch_manager = AsyncMock(return_value=manager)
    res = await escalation.resolve_state(1, {'ticket:confirm',})
    assert res == State.CONFIRMED
    res = await escalation.resolve_state(1, {'full_access', })
    assert res == State.CONFIRMED
