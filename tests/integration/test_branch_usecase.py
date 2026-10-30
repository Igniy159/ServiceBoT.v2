import pytest
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from app.errors import AuthorizeError, ResourceNotFound
from app.schemas.schemas_branch import CreateBranch, RenameBranch, ReceiveBranch, DeactivateBranch
from app.usecase import BranchUseCase


@pytest.mark.asyncio
async def test_only_admin_create_new_branch(session, users):
    actor = users.admin
    service = BranchUseCase(session,actor)
    cmd = CreateBranch(name="Новый филиал")
    res = await service.create(cmd)
    assert res.name == "Новый филиал"

@pytest.mark.asyncio
async def test_create_branch_unique_violation(session,users):
    actor = users.admin
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
async def test_other_role_cannot_create_branch(session,users):
    other_users = users.not_admin()
    cmd = CreateBranch(name="Новый филиал")
    for actor in other_users:
        service = BranchUseCase(session, actor)
        with pytest.raises(AuthorizeError):
            await service.create(cmd)

@pytest.mark.asyncio
async def test_admin_can_rename_branch(session, users,branch_factory, branches):
    actor = users.admin
    service = BranchUseCase(session, actor)
    await branch_factory(branches.all())
    cmd = RenameBranch(branch_id=branches.dragon.id, new_name='Новое имя')
    res = await service.rename(cmd)
    assert res.id == branches.dragon.id
    assert res.name == 'Новое имя'


@pytest.mark.asyncio
async def test_rename_not_found_branch(session, users,branch_factory, branches):
    actor = users.admin
    service = BranchUseCase(session, actor)
    await branch_factory(branches.all())
    cmd = RenameBranch(branch_id=999, new_name='Новое имя')
    with pytest.raises(ResourceNotFound):
        await service.rename(cmd)


@pytest.mark.asyncio
async def test_other_role_cannot_rename_branch(session, users, branches,branch_factory):
    await branch_factory(branches.all())
    old_name = branches.dragon.name
    cmd = RenameBranch(branch_id=branches.dragon.id, new_name='Новое имя')
    for actor in users.not_admin():
        service = BranchUseCase(session, actor)
        with pytest.raises(AuthorizeError):
            await service.rename(cmd)

    assert branches.dragon.name != "Новое имя"
    assert branches.dragon.name == old_name


@pytest.mark.asyncio
async def test_admin_and_owner_can_receive_branches(session, users, branches,branch_factory):
    await branch_factory(branches.all())
    for actor in (users.admin, users.owner):
        service = BranchUseCase(session, actor)
        result = await service.receive(ReceiveBranch())
        assert {branch.id for branch in result} == {
            branch.id for branch in branches.all()
        }

        result = await service.receive(
            ReceiveBranch(is_active=False)
        )
        assert result == []

        branches.dragon.is_active = False
        await session.flush()
        result = await service.receive(
            ReceiveBranch(is_active=True)
        )

        assert {branch.id for branch in result} == {
            branches.boar.id,
            branches.pony.id,
            branches.wolf.id,
        }

        branches.dragon.is_active = True
        await session.flush()

@pytest.mark.asyncio
async def test_other_cannot_receive_branches(session,users, branches, branch_factory):
    await branch_factory(branches.all())
    cmd = ReceiveBranch()
    need_users = users.executors()
    need_users.append(users.manager)
    need_users.append(users.employee)
    for user in need_users:
        service = BranchUseCase(session, user)
        with pytest.raises(AuthorizeError):
            await service.receive(cmd)

@pytest.mark.asyncio
async def test_admin_deactivate_branches(session, users, branches, branch_factory):
    await branch_factory(branches.all())
    branch = branches.dragon
    cmd = DeactivateBranch(branch_id=branch.id)
    service = BranchUseCase(session, users.admin)
    res = await service.deactivate(cmd)
    assert res == branch
    assert res.is_active is False

@pytest.mark.asyncio
async def test_double_deactivate_branches(session,users, branches, branch_factory):
    branches = await branch_factory(branches.all())
    branch = branches[0]
    cmd = DeactivateBranch(branch_id=branch.id)
    service = BranchUseCase(session, users.admin)
    res = await service.deactivate(cmd)
    repeat_res = await service.deactivate(cmd)
    assert res == repeat_res

@pytest.mark.asyncio
async def test_cannot_deactivate_not_found_branch(session, users,branches, branch_factory):
    await branch_factory(branches.all())
    cmd = DeactivateBranch(branch_id=999)
    service = BranchUseCase(session, users.admin)
    with pytest.raises(ResourceNotFound):
        await service.deactivate(cmd)

@pytest.mark.asyncio
async def test_other_cannot_deactivate_branch(session, users, branches, branch_factory):
    branches =await branch_factory(branches.all())
    branch = branches[0]
    cmd = DeactivateBranch(branch_id=branch.id)
    other_users = users.not_admin()
    for user in other_users:
        service = BranchUseCase(session, user)
        with pytest.raises(AuthorizeError):
            await service.deactivate(cmd)
