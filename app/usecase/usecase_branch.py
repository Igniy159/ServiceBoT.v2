from sqlalchemy import Select

from app.errors import ResourceNotFound
from app.models import Branch
from app.schemas.schemas_branch import (CreateBranch,RenameBranch,
                                        ReceiveBranch, DeleteBranch)
from app.usecase.base_usecase import UseCase


class BranchUseCase(UseCase):

    async def create(self, cmd: CreateBranch)-> Branch:
        await self.auth.load_role()
        self.auth.check('branch:create')
        new_branch = Branch(name=cmd.name)
        self.session.add(new_branch)
        await self.session.flush()
        return new_branch


    async def rename(self, cmd: RenameBranch)->Branch:
        await self.auth.load_role()
        self.auth.check('branch:rename')
        result = await self.session.execute(
            Select(Branch).where(Branch.id == cmd.branch_id))
        branch = result.scalar_one_or_none()
        if not branch:
            raise ResourceNotFound
        branch.name = cmd.new_name
        await self.session.flush()
        return branch


    async def receive(self, cmd: ReceiveBranch)->list[Branch]:
        await self.auth.load_role()
        self.auth.check('branch:receive')
        if cmd.is_active is None:
            stmt = Select(Branch)
        else:
            stmt = Select(Branch).where(Branch.is_active == cmd.is_active)

        result = await self.session.execute(stmt)
        return list(result.scalars().all())


    async def deactivate(self, cmd: DeleteBranch):
        await self.auth.load_role()
        self.auth.check('branch:deactivate')
        result = await self.session.execute(
            Select(Branch).where(Branch.id == cmd.branch_id)
        )
        branch = result.scalar_one_or_none()
        if not branch:
            raise ResourceNotFound
        branch.is_active = False
        await self.session.flush()
