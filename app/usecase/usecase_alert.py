from sqlalchemy import Select
from app.errors import ResourceNotFound, ProhibitNullBranch
from app.models import Alert, Rule
from app.schemas.schemas_alert import ReceiveAlerts, CreateAlert
from app.usecase.base_usecase import UseCase


class AlertUseCase(UseCase):
    async def create(self, cmd: CreateAlert)->Alert:
        await self.auth.load_role()
        self.auth.check('alert:create')
        self.auth.restrict_for_branch(cmd)
        stmt = Select(Rule).where(Rule.id == cmd.rule_id)
        result = await self.session.execute(stmt)
        rule = result.scalar_one_or_none()
        if rule is None:
            raise ResourceNotFound
        branch_id = self.auth.resolve_branch(cmd)
        new_alert = Alert(rule_id=cmd.rule_id,
                          branch_id=branch_id,
                          comment=cmd.comment)
        self.session.add(new_alert)
        await self.session.flush()
        return new_alert


    async def receive(self, cmd: ReceiveAlerts)->list[Alert]:
        await self.auth.load_role()
        self.auth.check('alert:receive')
        cmd = self.auth.check_restricts(cmd)
        stmt = Select(Alert)
        if cmd.alert_id is not None:
            stmt = stmt.where(Alert.id == cmd.alert_id)
        if cmd.branch_id is not None:
            stmt = stmt.where(Alert.branch_id == cmd.branch_id)
        if cmd.department_id is not None:
            stmt = stmt.join(Alert.rule)
            stmt = stmt.where(Rule.target_id == cmd.department_id)
        if cmd.class_rule is not None:
            stmt = stmt.join(Alert.rule)
            stmt = stmt.where(Rule.class_rule == cmd.class_rule)

        if cmd.limit is not None:
            stmt = stmt.limit(cmd.limit)
        if cmd.offset is not None:
            stmt = stmt.offset(cmd.offset)

        result = await self.session.execute(stmt)
        return list(result.scalars().all())
