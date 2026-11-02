import pytest
from app.enums import ClassRule, KindRule
from app.errors import IncorrectFieldsCmd
from app.schemas.schemas_rule import CreateRule
from app.usecase import RuleUseCase

@pytest.mark.parametrize('class_alert',[ClassRule.CRITICAL_ALERTS,
                        ClassRule.HR_ALERTS,
                        ClassRule.CASH_ALERTS,
                        ClassRule.SERVICE_ALERTS,
                        ClassRule.SECURITY_ALERTS])
def test_get_kind_return_alerts(class_alert):
    cmd = CreateRule(class_rule=class_alert,name='Тест', department_id=1)
    assert RuleUseCase._get_kind(cmd) == KindRule.ALERT


@pytest.mark.parametrize('class_request', [ClassRule.STORE_REQUEST,
                          ClassRule.INVENTORY_REQUEST,
                          ClassRule.MARKETING_REQUEST,
                          ClassRule.SECURITY_REQUEST,
                          ClassRule.IT_REQUEST])
def test_get_kind_return_request(class_request):
    cmd = CreateRule(class_rule=class_request,name='Тест', department_id=1)
    assert RuleUseCase._get_kind(cmd) == KindRule.REQUEST

@pytest.mark.parametrize('class_object',[ClassRule.FURNITURE,
                      ClassRule.REFRIGERATION,
                      ClassRule.CLIMATE,
                      ClassRule.PLUMBING,
                      ClassRule.ELECTRICAL,
                        ClassRule.CONSUMABLE_EQUIPMENT,
                     ClassRule.BAR_EQUIPMENT])
def test_get_kind_return_object(class_object):
    cmd = CreateRule(class_rule=class_object,name='Тест', department_id=1)
    assert RuleUseCase._get_kind(cmd) == KindRule.OBJECT

def test_class_rule_has_all():
    cmd = CreateRule(class_rule=ClassRule.ALL,name='Тест', department_id=1)
    with pytest.raises(IncorrectFieldsCmd):
        RuleUseCase._get_kind(cmd)
