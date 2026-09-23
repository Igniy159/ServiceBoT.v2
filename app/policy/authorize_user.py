from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.enums import ClassRule
from app.errors import AuthorizeError, ProhibitNullBranch
from app.models import User, Role
from app.schemas.schemas_alert import ReceiveAlerts, CreateAlert
from app.schemas.schemas_ticket import ReceiveTickets, CreateTicket


class Authorize:
    def __init__(self, session: AsyncSession, actor: User):
        self.session = session
        self.actor = actor
        self.permissions: set[str] | None = None
        self.responsibilities: set[ClassRule] | None = None

    async def load_role(self):
        stmt = (select(Role)
            .options(selectinload(Role.permissions),
                selectinload(Role.responsibilities),
            )
            .where(Role.id == self.actor.role_id)
        )
        result = await self.session.execute(stmt)
        role = result.scalar_one()
        self.permissions = {p.name for p in role.permissions}
        self.responsibilities = {p for p in role.responsibilities}

    def check(self, permission: str):
        permissions = self.permissions
        if permissions is None:
            raise AuthorizeError("Permissions have not been loaded")
        if permissions == {'full_access',}:
            return
        if permission not in permissions:
            raise AuthorizeError(f'User can not use this action {permission}')

    def check_restricts(self,cmd):
        cmd = self.restrict_for_branch(cmd)
        cmd = self.restrict_for_depart(cmd)
        self.restrict_for_query(cmd)
        return cmd

    def restrict_for_branch(self, cmd):
        if self.actor.role.need_branch:
            if getattr(cmd,'branch_id') is None:
                setattr(cmd,'branch_id', self.actor.branch_id)
            if getattr(cmd,'branch_id') != self.actor.branch_id:
                raise AuthorizeError
        return cmd

    def restrict_for_depart(self, cmd):
        if self.actor.role.need_department:
            if getattr(cmd,'department_id') is None:
                setattr(cmd, 'department_id', self.actor.department_id)
            if getattr(cmd,'department_id') != self.actor.department_id:
                raise AuthorizeError
        return cmd

    def restrict_for_query(self,
                           cmd: ReceiveAlerts | ReceiveTickets):
        if self.responsibilities is None:
            raise AuthorizeError("Responsibilities have not been loaded")
        if getattr(cmd,'class_rule') is not None:
            if cmd.class_rule not in self.responsibilities:
                raise AuthorizeError

    def resolve_branch(self, cmd:CreateTicket | CreateAlert)->int:
        if self.actor.branch_id is not None:
            return self.actor.branch_id

        if cmd.branch_id is not None:
            return cmd.branch_id

        raise ProhibitNullBranch
