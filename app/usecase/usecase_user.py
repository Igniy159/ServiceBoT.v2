from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.errors import ProhibitSelfModification, IncorrectFieldsCmd, ResourceNotFound
from app.policy.management_policy import ManagementPolicy
from app.usecase.base_usecase import UseCase
from app.schemas.schemas_user import (CreateTgUser, DeactivateUser, ChangeUser,
                                      RenameUser, ReceiveUser, ActivateUser, UserDTO)
from app.models import User, Role, Department, Branch


class UserUseCase(UseCase):

    async def create_from_tg(self,cmd: CreateTgUser)->User:
        await self.auth.load_role()
        self.auth.check('user:create')
        role_user = await self._role_requirement(cmd.role_id, cmd.branch_id, cmd.department_id)
        ManagementPolicy.check_management(self.auth.role, role_user)
        new_user = User(name= cmd.name,
                        tg_id=cmd.tg_id,
                        role_id=cmd.role_id,
                        department_id=cmd.department_id,
                        branch_id=cmd.branch_id)
        self.session.add(new_user)
        await self.session.flush()
        return new_user

    # async def change_tg_id(self, cmd:AddLinkTg):
    #     await self.auth.load_role()
    #     self.auth.check('user:tg_link')
    #     user = await self._get_user(cmd)
    #     user.tg_id = cmd.tg_id
    #     await self.session.flush()

    async def rename(self, cmd: RenameUser)->User:
        await self.auth.load_role()
        self.auth.check('user:rename')
        user = await self._get_user(cmd)
        ManagementPolicy.check_management(self.auth.role, user.role)
        user.name = cmd.new_name
        await self.session.flush()
        return user

    async def deactivate(self, cmd: DeactivateUser):
        await self.auth.load_role()
        self.auth.check('user:deactivate')
        self._prohibit_changing_oneself(cmd.user_id)
        user = await self._get_user(cmd)
        ManagementPolicy.check_management(self.auth.role, user.role)
        user.is_active = False
        await self.session.flush()

    async def activate(self, cmd: ActivateUser):
        await self.auth.load_role()
        self.auth.check('user:activate')
        self._prohibit_changing_oneself(cmd.user_id)
        user = await self._get_user(cmd)
        ManagementPolicy.check_management(self.auth.role, user.role)
        user.is_active = True
        await self.session.flush()


    async def change(self, cmd: ChangeUser)-> User:
        await self.auth.load_role()
        self.auth.check('user:change')
        cmd = self.auth.check_restricts(cmd)
        self._prohibit_changing_oneself(cmd.user_id)
        user = await self._get_user(cmd)
        ManagementPolicy.check_management(self.auth.role, user.role)
        await self._role_requirement(cmd.role_id,cmd.branch_id,cmd.department_id)
        user.role_id = cmd.role_id
        user.department_id = cmd.department_id
        user.branch_id = cmd.branch_id
        await self.session.flush()
        return user


    async def receive(self, cmd: ReceiveUser)->list[UserDTO]:
        await self.auth.load_role()
        self.auth.check('user:receive')
        cmd = self.auth.check_restricts(cmd)
        stmt = select(User.name,
                      Role.name,
                      Department.name,
                      Branch.name,
                      User.email,
                      User.tg_id
                      ).join(Role).join(Department).join(Branch)
        if cmd.user_id:
            stmt = stmt.where(User.id == cmd.user_id)
        if cmd.tg_id:
            stmt = stmt.where(User.tg_id == cmd.tg_id)
        if cmd.branch_id:
            stmt = stmt.where(User.branch_id == cmd.branch_id)
        if cmd.department_id:
            stmt = stmt.where(User.department_id == cmd.department_id)
        if cmd.role_id:
            stmt = stmt.where(User.role_id == cmd.role_id)
        if cmd.is_active is not None:
            stmt = stmt.where(User.is_active == cmd.is_active)
        stmt = stmt.limit(cmd.limit).offset(cmd.offset).order_by(User.name)

        result = await self.session.execute(stmt)
        return [UserDTO.model_validate(row.mappings()) for row in result]

    def _prohibit_changing_oneself(self, user_id):
        if self.actor.id == user_id:
            raise ProhibitSelfModification

    async def _role_requirement(self,
                          role_id: int,
                          branch_id: int | None,
                          department_id: int | None)->Role:
        role_res = await self.session.execute(select(Role).where(Role.id == role_id))
        role = role_res.scalar_one_or_none()
        if not role:
            raise ResourceNotFound
        if branch_id and department_id:
            raise IncorrectFieldsCmd
        if role.need_branch and not branch_id:
            raise IncorrectFieldsCmd
        if role.need_department and not department_id:
            raise IncorrectFieldsCmd
        return role

    async def _get_user(self, cmd)->User:
        stmt = (select(User)
                .where(User.id == cmd.user_id and User.is_active is True)
                .options(joinedload(User.role)))
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()
        if user is None:
            raise ResourceNotFound
        return user
