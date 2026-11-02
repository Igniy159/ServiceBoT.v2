from app.errors import ResourceNotFound, IncorrectFieldsCmd
from app.models import Rule, Department
from app.schemas.schemas_rule import CreateRule, DeleteRule
from app.usecase.base_usecase import UseCase
from sqlalchemy import select
from app.enums import KindRule,ClassRule

class RuleUseCase(UseCase):
    async def create(self, cmd: CreateRule)->Rule:
        await self.auth.load_role()
        self.auth.check('rule:create')
        need_kind = self._get_kind(cmd)
        stmt = select(Department).where(Department.id == cmd.department_id)
        res = await self.session.execute(stmt)
        department = res.scalar_one_or_none()
        if department is None:
            raise IncorrectFieldsCmd('Cmd department_id not found')
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
        objects = frozenset([ClassRule.BAR_EQUIPMENT,
                             ClassRule.CLIMATE,
                             ClassRule.PLUMBING,
                             ClassRule.FURNITURE,
                             ClassRule.ELECTRICAL,
                             ClassRule.CONSUMABLE_EQUIPMENT,
                             ClassRule.REFRIGERATION])
        if cmd.class_rule in alerts:
            return KindRule.ALERT
        if cmd.class_rule in requests:
            return KindRule.REQUEST
        if cmd.class_rule in objects:
            return KindRule.OBJECT
        raise IncorrectFieldsCmd('From rule Class all is prohibit')

    async def deactivate(self, cmd: DeleteRule):
        await self.auth.load_role()
        self.auth.check('rule:delete')
        result = await self.session.execute(select(Rule).where(Rule.id == cmd.rule_id))
        rule = result.scalar_one_or_none()
        if rule is None:
            raise ResourceNotFound('Rule not found')
        rule.is_active = False
        await self.session.flush()

    async def receive(self)->list[Rule]:
        await self.auth.load_role()
        self.auth.check('rule:receive')
        result = await self.session.execute(select(Rule).where(Rule.is_active.is_(True)))
        rules = list(result.scalars().all())
        return rules
