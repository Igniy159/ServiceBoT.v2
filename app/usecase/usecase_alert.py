from sqlalchemy import select
from app.errors import ResourceNotFound
from app.models import Alert, Rule, Branch, Department,User
from app.schemas.schemas_alert import ReceiveAlerts, CreateAlert, AlertDTO
from app.usecase.base_usecase import UseCase


class AlertUseCase(UseCase):
    async def create(self, cmd: CreateAlert)->int:
        await self.auth.load_role()
        self.auth.check('alert:create')
        self.auth.restrict_for_branch(cmd)
        stmt = select(Rule).where(Rule.id == cmd.rule_id)
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
        return new_alert.id

    async def receive(self, cmd: ReceiveAlerts)->list[AlertDTO]:
        await self.auth.load_role()
        self.auth.check('alert:receive')
        cmd = self.auth.check_restricts(cmd)
        stmt = select(Alert.comment,
                      Alert.created_at,
                      Rule.name.label('rule_name'),
                      User.name.label('creator_name'),
                      Branch.name.label('branch_name'),
                      Department.name.label('department_name'),
            ).join(Rule).join(Branch).join(Department).join(User)
        if cmd.alert_id is not None:
            stmt = stmt.where(Alert.id == cmd.alert_id)
        if cmd.branch_id is not None:
            stmt = stmt.where(Alert.branch_id == cmd.branch_id)
        if cmd.department_id is not None:
            stmt = stmt.where(Rule.target_id == cmd.department_id)
        if cmd.class_rule is not None:
            stmt = stmt.where(Rule.class_rule == cmd.class_rule)
        if cmd.created_from is not None:
            stmt = stmt.where(Alert.created_at >= cmd.created_from)
        if cmd.created_to is not None:
            stmt = stmt.where(Alert.created_at < cmd.created_to)
        stmt = stmt.limit(cmd.limit)
        stmt = stmt.offset(cmd.offset)
        result = await self.session.execute(stmt)
        return [AlertDTO.model_validate(row.mappings()) for row in result]
