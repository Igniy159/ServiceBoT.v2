from app.errors import ResourceNotFound
from app.models import Rule
from app.schemas.schemas_rule import CreateRule, DeleteRule
from app.usecase.base_usecase import UseCase
from sqlalchemy import Select
from app.enums import KindRule,ClassRule

class RuleUseCase(UseCase):
    async def create(self, cmd: CreateRule)->Rule:
        await self.auth.load_role()
        self.auth.check('rule:create')
        need_kind = self._get_kind(cmd)
        new_rule = Rule(kind=need_kind,
                        class_rule=cmd.class_rule,
                        name=cmd.name,
                        target_id=cmd.department_id)
        self.session.add(new_rule)
        await self.session.flush()
        return new_rule

    @staticmethod
    def _get_kind(cmd: CreateRule)-> KindRule:
        alerts = frozenset([ClassRule.CRITICAL_ALERTS,
                       ClassRule.HR_ALERTS,
                       ClassRule.CASH_ALERTS,
                       ClassRule.SERVICE_ALERTS,
                       ClassRule.SECURITY_ALERTS])
        requests = frozenset([ClassRule.STORE_REQUEST,
                       ClassRule.INVENTORY_REQUEST,
                       ClassRule.MARKETING_REQUEST,
                       ClassRule.SECURITY_REQUEST,
                       ClassRule.IT_REQUEST])
        if cmd.class_rule in alerts:
            return KindRule.ALERT
        if cmd.class_rule in requests:
            return KindRule.REQUEST
        return KindRule.OBJECT

    async def delete(self, cmd: DeleteRule):
        await self.auth.load_role()
        self.auth.check('rule:delete')
        result = await self.session.execute(Select(Rule).where(Rule.id == cmd.rule_id))
        rule =  result.scalar_one_or_none()
        if not rule:
            raise ResourceNotFound
        await self.session.delete(rule)
        await self.session.flush()
