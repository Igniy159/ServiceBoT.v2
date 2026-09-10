from typing import Optional
import bcrypt
from sqlalchemy import Select
from app.errors import ProhibitSelfModification, IncorrectRoleFields, ResourceNotFound
from app.usecase.base_usecase import UseCase
from app.schemas.schemas_user import (CreateTgUser, DeactivateUser, ChangeUser,
                    RenameUser, ReceiveUser, CreateWebUser,AddTgId)
from app.models import User, Role


class UserUseCase(UseCase):

    async def create_from_tg(self,cmd: CreateTgUser)->User:
        await self._role_requirement(cmd.role_id, cmd.branch_id, cmd.department_id)
        new_user = User(name= cmd.name,
                        tg_id=cmd.tg_id,
                        role_id=cmd.role_id,
                        department_id=cmd.department_id,
                        branch_id=cmd.branch_id)
        self.session.add(new_user)
        await self.session.flush()
        return new_user

    async def create_from_web(self,cmd:CreateWebUser):
        await self._role_requirement(cmd.role_id, cmd.branch_id, cmd.department_id)
        # NOT ASYNC FUNC !!!
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(cmd.password.encode(),salt).decode()
        new_user = User(name= cmd.name,
                        email=cmd.email,
                        password_hash=password_hash,
                        role_id=cmd.role_id,
                        department_id=cmd.department_id,
                        branch_id=cmd.branch_id)
        self.session.add(new_user)
        await self.session.flush()
        return new_user

    async def link_tg(self, cmd: AddTgId):
        result = await self.session.execute(Select(User).where(User.id == cmd.user_id))
        user = result.scalar_one_or_none()
        if not user:
            raise ResourceNotFound
        user.tg_id = cmd.tg_id
        await self.session.flush()


    async def rename(self, cmd: RenameUser)->User:
        result = await self.session.execute(Select(User).where(User.id == cmd.user_id))
        user = result.scalar_one_or_none()
        if not user:
            raise ResourceNotFound
        user.name = cmd.new_name
        await self.session.flush()
        return user

    async def deactivate(self, cmd: DeactivateUser):
        self._prohibit_changing_oneself(cmd.user_id)
        result = await self.session.execute(Select(User).where(User.id == cmd.user_id))
        user = result.scalar_one_or_none()
        if not user:
            raise ResourceNotFound
        user.is_active = False
        await self.session.flush()


    async def change(self, cmd: ChangeUser)-> User:
        self._prohibit_changing_oneself(cmd.user_id)
        result = await self.session.execute(Select(User).where(User.id == cmd.user_id))

        user = result.scalar_one_or_none()
        if not user:
            raise ResourceNotFound
        await self._role_requirement(cmd.role_id,cmd.branch_id,cmd.department_id)
        user.role_id = cmd.role_id
        user.department_id = cmd.department_id
        user.branch_id = cmd.branch_id
        await self.session.flush()
        return user


    async def receive(self, cmd: ReceiveUser)->list[User]:
        stmt = Select(User)
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
        result = await self.session.execute(stmt)
        users = result.scalars().all()
        return list(users)


    def _prohibit_changing_oneself(self, user_id):
        if self.actor.id == user_id:
            raise ProhibitSelfModification


    async def _role_requirement(self,
                          role_id: int,
                          branch_id: Optional[int],
                          department_id: Optional[int]):
        role_res = await self.session.execute(Select(Role).where(Role.id == role_id))
        role = role_res.scalar_one_or_none()
        if not role:
            raise ResourceNotFound
        if branch_id and department_id:
            raise IncorrectRoleFields
        if role.need_branch and not branch_id:
            raise IncorrectRoleFields
        if role.need_department and not department_id:
            raise IncorrectRoleFields
