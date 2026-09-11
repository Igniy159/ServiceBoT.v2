from app.models import Role
from app.schemas.schemas_role import CreateRole
from app.usecase.base_usecase import UseCase


class RoleUseCase(UseCase):
    async def create(self, cmd:CreateRole):
        await self.auth.load_role()
        self.auth.check('role:create')
        new_role = Role(name=cmd.name,
                        need_branch=cmd.need_branch,
                        need_department=cmd.need_department,
                        responsibilities=cmd.responsibilities,
                        permissions=cmd.permissions)
        self.session.add(new_role)
        await self.session.flush()
