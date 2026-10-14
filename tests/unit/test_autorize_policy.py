import pytest
from unittest.mock import Mock
from app.enums import ClassRule
from app.errors import AuthorizeError, ProhibitNullBranch


@pytest.mark.asyncio
async def test_positive_load_role(authorize, role_admin):
    result = Mock()
    result.scalar_one.return_value = role_admin
    authorize.session.execute.return_value = result
    await authorize.load_role()
    assert authorize.role == role_admin
    assert authorize.permissions == {'full_access',}
    assert set(authorize.responsibilities) == {ClassRule.ALL}
    authorize.session.execute.assert_awaited_once()

@pytest.mark.asyncio
async def test_load_permissions(authorize, role_employee):
    result = Mock()
    result.scalar_one.return_value = role_employee
    authorize.session.execute.return_value = result
    await authorize.load_role()
    assert authorize.permissions == {'alert:create', 'ticket:create'}
    assert authorize.responsibilities == set()

@pytest.mark.asyncio
async def test_check_permissions_full_access(authorize):
    authorize.permissions = {'full_access',}
    assert authorize.check('ticket:create') is None
    assert authorize.check('alert:create') is None
    assert authorize.check('branch:receive') is None


def test_check_permissions_partial_access(authorize):
    authorize.permissions = {'ticket:create',}
    assert authorize.check('ticket:create') is None
    with pytest.raises(AuthorizeError) as exc_info:
        authorize.check('alert:create')
    assert str(exc_info.value) == 'User can not use this action alert:create'

def test_check_permission_not_loaded(authorize):
    authorize.permissions = None
    with pytest.raises(AuthorizeError) as exc_info:
        authorize.check('alert:create')
    assert str(exc_info.value) == "Permissions have not been loaded"


def test_restrict_branch(authorize):
    authorize.role = Mock()
    authorize.role.need_branch = True
    authorize.actor.branch_id = 1
    cmd = Mock()
    cmd.branch_id = None
    authorize.restrict_for_branch(cmd)
    assert cmd.branch_id == authorize.actor.branch_id == 1
    authorize.role.need_branch = False
    cmd.branch_id = 5
    cmd = authorize.restrict_for_branch(cmd)
    assert cmd.branch_id == 5

def test_cmd_and_actor_branch_must_be_eq(authorize):
    authorize.role = Mock()
    authorize.role.need_branch = True
    authorize.actor.branch_id = 1
    cmd = Mock()
    cmd.branch_id = 2
    with pytest.raises(AuthorizeError):
        authorize.restrict_for_branch(cmd)


def test_restrict_department(authorize):
    authorize.role = Mock()
    authorize.role.need_department = True
    authorize.actor.department_id = 1
    cmd = Mock()
    cmd.department_id = None
    authorize.restrict_for_depart(cmd)
    assert cmd.department_id == authorize.actor.department_id == 1
    authorize.role.need_department = False
    cmd.department_id = 5
    cmd = authorize.restrict_for_depart(cmd)
    assert cmd.department_id == 5

def test_cmd_and_actor_department_must_be_eq(authorize):
    authorize.role = Mock()
    authorize.role.need_department = True
    authorize.actor.department_id = 1
    cmd = Mock()
    cmd.department_id = 2
    with pytest.raises(AuthorizeError):
        authorize.restrict_for_depart(cmd)


def test_restrict_for_query(authorize):
    cmd = Mock()
    cmd.class_rule = ClassRule.HR_ALERTS
    authorize.responsibilities = {ClassRule.HR_ALERTS}
    assert authorize.restrict_for_query(cmd) == cmd

    cmd.class_rule = ClassRule.MARKETING_REQUEST
    authorize.responsibilities = {ClassRule.ALL}
    assert authorize.restrict_for_query(cmd) == cmd

    cmd.class_rule = ClassRule.MARKETING_REQUEST
    authorize.responsibilities = {ClassRule.STORE_REQUEST}
    with pytest.raises(AuthorizeError):
        authorize.restrict_for_query(cmd)

    cmd.class_rule = None
    authorize.responsibilities = {ClassRule.PLUMBING, ClassRule.CLIMATE}
    with pytest.raises(AuthorizeError):
        authorize.restrict_for_query(cmd)

    cmd.class_rule = None
    authorize.responsibilities = set()
    with pytest.raises(AuthorizeError):
        authorize.restrict_for_query(cmd)

    authorize.responsibilities = {ClassRule.PLUMBING}
    cmd.class_rule = None
    cmd = authorize.restrict_for_query(cmd)
    assert cmd.class_rule == ClassRule.PLUMBING

def test_resolve_branch(authorize):
    cmd = Mock()
    authorize.actor.branch_id = 1
    branch_id = authorize.resolve_branch(cmd)
    assert branch_id == 1

    authorize.actor.branch_id = None
    cmd.branch_id = 2
    branch_id = authorize.resolve_branch(cmd)
    assert branch_id == 2

    authorize.actor.branch_id = None
    cmd.branch_id = None
    with pytest.raises(ProhibitNullBranch):
        authorize.resolve_branch(cmd)

    authorize.actor.branch_id = 1
    cmd.branch_id = 2
    branch_id = authorize.resolve_branch(cmd)
    assert branch_id == 1
