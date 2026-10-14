from unittest.mock import AsyncMock, Mock
import pytest
from app.enums import State


@pytest.mark.parametrize(
    'state',
    (State.NEW, State.IN_PROGRESS, State.WAITING_EXTERNAL,State.RESOLVED, State.CANCELLED),
)
@pytest.mark.asyncio
async def test_notify_manager_if_manager_exist(
        notification,manager,
        managers,state, ticket_factory):
    notification.get_branch_manager = AsyncMock(return_value=manager)
    ticket = ticket_factory(state)
    res = await notification.ticket_push_notification_user(ticket)
    assert res == manager

    notification.get_branch_manager = AsyncMock(return_value=managers)
    ticket = ticket_factory(state)
    res = await notification.ticket_push_notification_user(ticket)
    assert res == managers

@pytest.mark.parametrize(
    'state',
    (State.CONFIRMED, State.CLOSED),
)
@pytest.mark.asyncio
async def test_notify_does_not_search_manager(
        notification,
        state,ticket_factory, owner):
    notification.get_branch_manager = Mock()
    notification.get_executors = AsyncMock(return_value=[])
    notification.get_owner = AsyncMock(return_value=owner)
    ticket = ticket_factory(state)
    await notification.ticket_push_notification_user(ticket)
    notification.get_branch_manager.assert_not_called()

@pytest.mark.parametrize(
    'state',
    ( State.IN_PROGRESS, State.WAITING_EXTERNAL,State.RESOLVED, State.CANCELLED),
)
@pytest.mark.asyncio
async def test_notify_creator_if_not_manager(
        notification,
        creator,
        state,
        ticket_factory):
    notification.get_branch_manager = AsyncMock(return_value=[])
    notification.get_user_by_id = AsyncMock(return_value=creator)
    ticket = ticket_factory(state)
    res = await notification.ticket_push_notification_user(ticket)
    assert res == [creator]

@pytest.mark.asyncio
async def test_notify_all_executors_if_exists(
        notification,executors,ticket_factory):
    notification.get_executors = AsyncMock(return_value=executors)
    ticket = ticket_factory(State.CONFIRMED)
    res = await notification.ticket_push_notification_user(ticket)
    assert res == executors

@pytest.mark.asyncio
async def test_notify_owner_if_not_exist_executors(
        notification,owner,ticket_factory):
    notification.get_executors = AsyncMock(return_value=[])
    notification.get_owner = AsyncMock(return_value=owner)
    ticket = ticket_factory(State.CONFIRMED)
    res = await notification.ticket_push_notification_user(ticket)
    assert res == [owner]


@pytest.mark.parametrize(
    'state',
    (State.NEW, State.IN_PROGRESS, State.WAITING_EXTERNAL,
     State.RESOLVED, State.CLOSED, State.CANCELLED),
)
@pytest.mark.asyncio
async def test_notify_does_not_search_executors(
        notification, executors,
        manager, state, ticket_factory):
    notification.get_executors = AsyncMock(return_value=executors)
    notification.get_branch_manager = AsyncMock(return_value=manager)
    ticket = ticket_factory(state)
    await notification.ticket_push_notification_user(ticket)
    notification.get_executors.assert_not_called()


@pytest.mark.parametrize(
    'state',
    (State.CLOSED, State.CANCELLED),
)
@pytest.mark.asyncio
async def test_notify_assigned_to(
        notification,assigned_to,
        manager, ticket_factory, state):
    notification.get_user_by_id = AsyncMock(return_value=assigned_to)
    notification.get_branch_manager = AsyncMock(return_value=manager)
    ticket = ticket_factory(state)
    ticket.assigned_to_id = 5
    res = await notification.ticket_push_notification_user(ticket)
    assert assigned_to in res

@pytest.mark.parametrize(
    'state',
    (State.NEW,State.CONFIRMED,
     State.IN_PROGRESS, State.WAITING_EXTERNAL, State.RESOLVED),
)
@pytest.mark.asyncio
async def test_notify_does_not_search_assigned(
        notification, executors,manager,
        assigned_to, state, ticket_factory):
    notification.get_executors = AsyncMock(return_value=executors)
    notification.get_branch_manager = AsyncMock(return_value=manager)
    ticket = ticket_factory(state)
    res = await notification.ticket_push_notification_user(ticket)
    assert assigned_to not in res
