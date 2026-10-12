from unittest.mock import AsyncMock
import pytest
from app.models import Ticket, User
from app.policy.assigned_policy import AssignmentPolicy


@pytest.fixture
def assigned_policy(manager,
                executors,
                owner
                ) -> AssignmentPolicy:
    policy = AssignmentPolicy(session=AsyncMock())
    policy.get_branch_manager = AsyncMock()
    policy.get_branch_manager.return_value = manager
    policy.get_executors = AsyncMock()
    policy.get_executors.return_value = executors
    policy.get_owner = AsyncMock()
    policy.get_owner.return_value = owner
    return policy

@pytest.mark.asyncio
async def test_get_managers_if_ticket_new(
        assigned_policy: AsyncMock,
        manager: User,
        new_ticket: Ticket
):
    result = await assigned_policy.get_assign_user(new_ticket)
    assert result == manager
    assigned_policy.get_branch_manager.assert_awaited_once_with(new_ticket)
    assigned_policy.get_executors.assert_not_awaited()
    assigned_policy.get_owner.assert_not_awaited()


@pytest.mark.asyncio
async def test_get_executors_if_ticket_confirm(
        assigned_policy: AsyncMock,
        executors: list[User],
        confirm_ticket: Ticket):
    result = await assigned_policy.get_assign_user(confirm_ticket)
    assert result == executors
    assigned_policy.get_branch_manager.assert_not_awaited()
    assigned_policy.get_owner.assert_not_awaited()


@pytest.mark.asyncio
async def test_get_owner_if_not_executors(
        assigned_policy: AsyncMock,
        owner: User,
        confirm_ticket: Ticket):
    assigned_policy.get_executors.return_value = []
    result = await assigned_policy.get_assign_user(confirm_ticket)
    assert result == owner
    assigned_policy.get_branch_manager.assert_not_awaited()


