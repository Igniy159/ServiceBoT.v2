import pytest
from app.errors import AuthorizeError, AlreadyExistsError, ResourceNotFound
from app.models import Department
from app.schemas.schemas_department import CreateDepartment, ReceiveDepartment, DeactivateDepartment
from app.usecase import DepartmentUseCase

@pytest.mark.asyncio
async def test_only_admin_create_depart(session,users):
    use_case = DepartmentUseCase(session,users.admin)
    cmd = CreateDepartment(name='Тестовое имя')
    res = await use_case.create(cmd)
    assert res.is_active is True
    assert res.name == 'Тестовое имя'
    assert isinstance(res, Department)

@pytest.mark.asyncio
async def test_other_can_not_create_department(session,users):
    for user in users.not_admin():
        cmd = CreateDepartment(name='Тестовое имя')
        use_case = DepartmentUseCase(session, user)
        with pytest.raises(AuthorizeError):
            await use_case.create(cmd)

@pytest.mark.asyncio
async def test_double_create_department(session, users):
    use_case = DepartmentUseCase(session,users.admin)
    cmd = CreateDepartment(name='Тестовое имя')
    await use_case.create(cmd)
    with pytest.raises(AlreadyExistsError):
        await use_case.create(cmd)


@pytest.mark.asyncio
async def test_admin_and_owner_can_receive_depart(session, users):
    use_case = DepartmentUseCase(session, users.admin)
    cmd = CreateDepartment(name='Тестовое имя')
    new_dep = await use_case.create(cmd)
    cmd = ReceiveDepartment()
    departments = await use_case.receive(cmd)
    assert new_dep in departments

    use_case = DepartmentUseCase(session, users.owner)
    departments = await use_case.receive(cmd)
    assert new_dep in departments

@pytest.mark.asyncio
async def test_receive_deactivated_department(session,users):
    use_case = DepartmentUseCase(session, users.admin)
    cmd = CreateDepartment(name='Тестовое имя')
    new_dep = await use_case.create(cmd)
    cmd = DeactivateDepartment(department_id=new_dep.id)
    await use_case.deactivate(cmd)
    cmd = ReceiveDepartment(is_active=False)
    res = await use_case.receive(cmd)
    assert new_dep in res

@pytest.mark.asyncio
async def test_only_admin_deactivate_department(session, users):
    use_case = DepartmentUseCase(session, users.admin)
    cmd = CreateDepartment(name='Тестовое имя')
    new_dep = await use_case.create(cmd)
    cmd = DeactivateDepartment(department_id=new_dep.id)
    await use_case.deactivate(cmd)
    cmd = ReceiveDepartment()
    result = await use_case.receive(cmd)
    assert new_dep not in result

@pytest.mark.asyncio
async def test_other_can_not_deactivated_department(session, users):
    use_case = DepartmentUseCase(session, users.admin)
    cmd = CreateDepartment(name='Тестовое имя')
    new_dep = await use_case.create(cmd)
    cmd = DeactivateDepartment(department_id=new_dep.id)
    for u in users.executors():
        use_case = DepartmentUseCase(session, u)
        with pytest.raises(AuthorizeError):
            await use_case.deactivate(cmd)

@pytest.mark.asyncio
async def test_deactivate_not_exist_department(session, users):
    use_case = DepartmentUseCase(session, users.admin)
    cmd = DeactivateDepartment(department_id=999)
    with pytest.raises(ResourceNotFound):
        await use_case.deactivate(cmd)

@pytest.mark.asyncio
async def test_double_deactivate_department(session, users):
    use_case = DepartmentUseCase(session, users.admin)
    cmd = CreateDepartment(name='Тестовое имя')
    new_dep = await use_case.create(cmd)
    cmd = DeactivateDepartment(department_id=new_dep.id)
    await use_case.deactivate(cmd)
    await use_case.deactivate(cmd)