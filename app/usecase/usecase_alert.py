from sqlalchemy import Select
from app.errors import ResourceNotFound, ProhibitNullBranch
from app.models import Alert, Rule
from app.schemas.schemas_alert import ReceiveAlerts, CreateAlert
from app.usecase.base_usecase import UseCase


class AlertUseCase(UseCase):
    async def create(self, cmd: CreateAlert)->Alert:
        stmt = Select(Rule).where(Rule.id == cmd.rule_id)
        result = await self.session.execute(stmt)
        rule = result.scalar_one_or_none()
        if rule is None:
            raise ResourceNotFound
        branch_id = self._presence_branch(cmd)
        new_alert = Alert(rule_id=cmd.rule_id,
                          branch_id=branch_id,
                          comment=cmd.comment)
        self.session.add(new_alert)
        await self.session.flush()
        return new_alert

    def _presence_branch(self, cmd:CreateAlert)->int:
        if self.actor.branch_id is not None:
            return self.actor.branch_id

        if cmd.branch_id is not None:
            return cmd.branch_id

        raise ProhibitNullBranch

    async def receive(self, cmd: ReceiveAlerts)->list[Alert]:
        stmt = Select(Alert)
        if cmd.alert_id is None:
            stmt = stmt.where(Alert.id == cmd.alert_id)
        if cmd.branch_id is None:
            stmt = stmt.where(Alert.branch_id == cmd.branch_id)
        if cmd.target_id is None:
            stmt = stmt.join(Alert.rule)
            stmt = stmt.where(Rule.target_id == cmd.target_id)

        if cmd.limit is None:
            stmt = stmt.limit(cmd.limit)
        if cmd.offset is None:
            stmt = stmt.offset(cmd.offset)

        result = await self.session.execute(stmt)
        return list(result.scalars().all())
