from unittest.mock import AsyncMock

from app.enums import State
from app.policy.escalation_policy import EscalationPolicy
import pytest
from tests.unit.conftest import manager


@pytest.fixture
def escalation()->EscalationPolicy:
    return EscalationPolicy(session=AsyncMock())


@pytest.mark.asyncio
async def test_resolve_state_if_manager(escalation, manager):
    escalation.get_branch_manager = AsyncMock(return_value=manager)
    res = await escalation.resolve_state(1, {'ticket:create',})
    assert res == State.NEW

@pytest.mark.asyncio
async def test_resolve_state_if_not_manager(escalation, manager):
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