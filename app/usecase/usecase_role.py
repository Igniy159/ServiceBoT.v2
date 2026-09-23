from app.models import Role
from app.schemas.schemas_role import CreateRole, RoleDTO
from app.usecase.base_usecase import UseCase


class RoleUseCase(UseCase):
    async def create(self, cmd:CreateRole)->RoleDTO:
        await self.auth.load_role()
        self.auth.check('role:create')
        new_role = Role(name=cmd.name,
                        need_branch=cmd.need_branch,
                        need_department=cmd.need_department,
                        responsibilities=cmd.responsibilities,
                        notifications=cmd.notifications,
                        permissions=cmd.permissions_ids)
        self.session.add(new_role)
        await self.session.flush()
        return RoleDTO(id=new_role.id,
                       name=new_role.name)
