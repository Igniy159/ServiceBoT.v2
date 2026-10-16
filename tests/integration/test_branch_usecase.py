import pytest
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from app.errors import AuthorizeError, ResourceNotFound
from app.schemas.schemas_branch import CreateBranch, RenameBranch, ReceiveBranch, DeactivateBranch
from app.usecase import BranchUseCase
from tests.conftest import FakeUsers


@pytest.mark.asyncio
async def test_only_admin_create_new_branch(session):
    actor = FakeUsers.admin
    service = BranchUseCase(session,actor)
    cmd = CreateBranch(name="Новый филиал")
    res = await service.create(cmd)
    assert res.name == "Новый филиал"

@pytest.mark.asyncio
async def test_create_branch_unique_violation(session):
    actor = FakeUsers.admin
    service = BranchUseCase(session,actor)
    cmd = CreateBranch(name="Новый филиал")
    await service.create(cmd)
    with pytest.raises(IntegrityError):
        await service.create(cmd)


def test_invalid_cmd():
    with pytest.raises(ValidationError):
        CreateBranch(name="Длина названия филиала больше 20 символов")
    with pytest.raises(ValidationError):
        RenameBranch(branch_id=1,
                     new_name="Длина названия филиала больше 20 символов")


@pytest.mark.asyncio
async def test_other_role_cannot_create_branch(session,all_users):
    #delete only admin
    other_users = all_users[1:]
    cmd = CreateBranch(name="Новый филиал")
    for actor in other_users:
        service = BranchUseCase(session, actor)
        with pytest.raises(AuthorizeError):
            await service.create(cmd)

@pytest.mark.asyncio
async def test_admin_can_rename_branch(session, branch_factory, branches):
    actor = FakeUsers.admin
    service = BranchUseCase(session, actor)
    branch = (await branch_factory(branches))[0]
    cmd = RenameBranch(branch_id=branch.id, new_name='Новое имя')
    res = await service.rename(cmd)
    assert res.id == branch.id
    assert res.name == 'Новое имя'


@pytest.mark.asyncio
async def test_rename_not_found_branch(session, branch_factory, branches):
    actor = FakeUsers.admin
    service = BranchUseCase(session, actor)
    await branch_factory(branches)
    cmd = RenameBranch(branch_id=999, new_name='Новое имя')
    with pytest.raises(ResourceNotFound):
        await service.rename(cmd)


@pytest.mark.asyncio
async def test_other_role_cannot_rename_branch(session, all_users, branches,branch_factory):
    # delete only admin
    del all_users[0]

    branch = (await branch_factory(branches))[0]
    old_name = branch.name
    cmd = RenameBranch(branch_id=branch.id, new_name='Новое имя')
    for actor in all_users:
        service = BranchUseCase(session, actor)
        with pytest.raises(AuthorizeError):
            await service.rename(cmd)

    await session.refresh(branch)
    assert branch.name != "Новое имя"
    assert branch.name == old_name


@pytest.mark.asyncio
@pytest.mark.parametrize('actor', [FakeUsers.admin, FakeUsers.owner])
async def test_admin_and_owner_can_receive_branches(session, actor, branches,branch_factory):
    branches = await branch_factory(branches)
    cmd = ReceiveBranch()
    service = BranchUseCase(session, actor)
    res = await service.receive(cmd)
    assert branches == res

    cmd = ReceiveBranch(is_active=False)
    res = await service.receive(cmd)
    assert res == []

    branches[0].is_active = False
    branches = await branch_factory(branches)
    res = await service.receive(cmd)
    assert res == [branches[0]]

    cmd = ReceiveBranch(is_active=True)
    res = await service.receive(cmd)
    assert branches[0] not in res
    assert res == branches[1:]

@pytest.mark.asyncio
async def test_other_cannot_receive_branches(session,all_users, branches, branch_factory):
    await branch_factory(branches)
    cmd = ReceiveBranch()
    other_users = all_users[2:]
    for user in other_users:
        service = BranchUseCase(session, user)
        with pytest.raises(AuthorizeError):
            await service.receive(cmd)

@pytest.mark.asyncio
@pytest.mark.parametrize('actor', [FakeUsers.admin])
async def test_admin_deactivate_branches(session, actor, branches, branch_factory):
    branches = await branch_factory(branches)
    branch = branches[0]
    cmd = DeactivateBranch(branch_id=branch.id)
    service = BranchUseCase(session, actor)
    res = await service.deactivate(cmd)
    assert res == branch
    assert res.is_active is False

async def test_double_deactivate_branches(session, branches, branch_factory):
    branches = await branch_factory(branches)
    branch = branches[0]
    cmd = DeactivateBranch(branch_id=branch.id)
    service = BranchUseCase(session, FakeUsers.admin)
    res = await service.deactivate(cmd)
    repeat_res = await service.deactivate(cmd)
    assert res == repeat_res

@pytest.mark.asyncio
async def test_cannot_deactivate_not_found_branch(session, branches, branch_factory):
    await branch_factory(branches)
    actor = FakeUsers.admin
    cmd = DeactivateBranch(branch_id=999)
    service = BranchUseCase(session, actor)
    with pytest.raises(ResourceNotFound):
        await service.deactivate(cmd)

@pytest.mark.asyncio
async def test_other_cannot_deactivate_branch(session, all_users, branches, branch_factory):
    branches =await branch_factory(branches)
    branch = branches[0]
    cmd = DeactivateBranch(branch_id=branch.id)
    other_users = all_users[1:]
    for user in other_users:
        service = BranchUseCase(session, user)
        with pytest.raises(AuthorizeError):
            await service.deactivate(cmd)
