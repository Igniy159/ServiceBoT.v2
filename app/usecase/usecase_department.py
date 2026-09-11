from sqlalchemy import Select

from app.errors import ResourceNotFound
from app.models import Department
from app.schemas.schemas_department import (CreateDepartment,ReceiveDepartment,
                                            DeactivateDepartment)
from app.usecase.base_usecase import UseCase


class DepartmentUseCase(UseCase):

    async def create(self, cmd: CreateDepartment)-> Department:
        await self.auth.load_role()
        self.auth.check('department:create')
        new_depart = Department(name=cmd.name)
        self.session.add(new_depart)
        await self.session.flush()
        return new_depart


    async def receive(self, cmd: ReceiveDepartment)->list[Department]:
        await self.auth.load_role()
        self.auth.check('department:receive')
        if cmd.is_active is None:
            stmt = Select(Department)
        else:
            stmt = Select(Department).where(Department.is_active == cmd.is_active)

        result = await self.session.execute(stmt)
        return list(result.scalars().all())


    async def deactivate(self, cmd: DeactivateDepartment):
        await self.auth.load_role()
        self.auth.check('department:deactivate')
        result = await self.session.execute(
            Select(Department).where(Department.id == cmd.department_id)
        )
        department = result.scalar_one_or_none()
        if not department:
            raise ResourceNotFound
        department.is_active = False
        await self.session.flush()
