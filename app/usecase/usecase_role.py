from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.errors import IncorrectFieldsCmd, AlreadyExistsError
from app.models import Role, Responsibility, Subscribe, Permission
from app.schemas.schemas_role import CreateRole, RoleDTO
from app.usecase.base_usecase import UseCase


class RoleUseCase(UseCase):
    async def create(self, cmd:CreateRole)->RoleDTO:
        if cmd.need_branch and cmd.need_department:
            raise IncorrectFieldsCmd('Incorrect cmd. Branch and department is true')
        await self.auth.load_role()
        self.auth.check('role:create')

        resp = [Responsibility(class_rule=r) for r in cmd.responsibilities]
        sub = [Subscribe(class_rule=s) for s in cmd.subscriptions]

        stmt = select(Permission).where(
            Permission.name.in_(cmd.permissions)
        )
        result = await self.session.execute(stmt)
        permissions = list(result.scalars().all())
        if not permissions:
            raise IncorrectFieldsCmd('Role must have permissions')
        if len(permissions) != len(cmd.permissions):
            raise IncorrectFieldsCmd('Permissions have incorrect value')

        new_role = Role(name=cmd.name,
                            need_branch=cmd.need_branch,
                            need_department=cmd.need_department,
                            responsibilities=resp,
                            subscriptions=sub,
                            permissions=permissions)

        self.session.add(new_role)
        try:
            await self.session.flush()
        except IntegrityError as e:
            raise AlreadyExistsError('Role already exists') from e
        return RoleDTO(id=new_role.id,
                       name=new_role.name)
