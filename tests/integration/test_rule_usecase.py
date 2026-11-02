import pytest

from app.enums import ClassRule, KindRule
from app.errors import AuthorizeError, IncorrectFieldsCmd, ResourceNotFound
from app.schemas.schemas_rule import CreateRule, DeleteRule
from app.usecase import RuleUseCase


@pytest.mark.asyncio
async def test_only_admin_create_new_rule(session,users):
    use_case = RuleUseCase(session,users.admin)
    cmd = CreateRule(class_rule=ClassRule.HR_ALERTS, name='Тестовое правило', department_id=1)
    res = await use_case.create(cmd)
    assert res.name == 'Тестовое правило'
    assert res.kind == KindRule.ALERT
    assert res.class_rule == ClassRule.HR_ALERTS

@pytest.mark.asyncio
async def test_other_can_not_create_new_rule(session,users):
    cmd = CreateRule(class_rule=ClassRule.HR_ALERTS, name='Тестовое правило', department_id=1)
    for user in users.not_admin():
        use_case = RuleUseCase(session,user)
        with pytest.raises(AuthorizeError):
            await use_case.create(cmd)

@pytest.mark.asyncio
async def test_create_rule_with_not_found_department(session,users):
    use_case = RuleUseCase(session,users.admin)
    cmd = CreateRule(class_rule=ClassRule.HR_ALERTS, name='Тестовое правило', department_id=999)
    with pytest.raises(IncorrectFieldsCmd):
        await use_case.create(cmd)

@pytest.mark.asyncio
async def test_admin_receive_rule(session,users):
    use_case = RuleUseCase(session,users.admin)
    cmd = CreateRule(class_rule=ClassRule.HR_ALERTS, name='Тестовое правило', department_id=1)
    new_rule = await use_case.create(cmd)
    res = await use_case.receive()
    assert new_rule in res

@pytest.mark.asyncio
async def test_other_can_not_receive_rule(session,users):
    for user in users.not_admin():
        use_case = RuleUseCase(session,user)
        with pytest.raises(AuthorizeError):
            await use_case.receive()

@pytest.mark.asyncio
async def test_admin_can_deactivate_rule(session, users):
    use_case = RuleUseCase(session, users.admin)
    cmd = CreateRule(class_rule=ClassRule.HR_ALERTS, name='Тестовое правило', department_id=1)
    new_rule = await use_case.create(cmd)
    cmd = DeleteRule(rule_id=new_rule.id)
    await use_case.deactivate(cmd)
    rules = await use_case.receive()
    assert new_rule not in rules

@pytest.mark.asyncio
async def test_other_can_not_deactivate_rule(session,users):
    for user in users.not_admin():
        use_case = RuleUseCase(session,user)
        cmd = DeleteRule(rule_id=1)
        with pytest.raises(AuthorizeError):
            await use_case.deactivate(cmd)

@pytest.mark.asyncio
async def test_deactivate_not_found_rule(session,users):
    use_case = RuleUseCase(session, users.admin)
    cmd = DeleteRule(rule_id=999)
    with pytest.raises(ResourceNotFound):
        await use_case.deactivate(cmd)

@pytest.mark.asyncio
async def test_double_deactivate_rule(session,users):
    use_case = RuleUseCase(session, users.admin)
    cmd = CreateRule(class_rule=ClassRule.HR_ALERTS, name='Тестовое правило', department_id=1)
    new_rule = await use_case.create(cmd)
    cmd = DeleteRule(rule_id=new_rule.id)
    await use_case.deactivate(cmd)
    await use_case.deactivate(cmd)
