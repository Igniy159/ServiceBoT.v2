from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import Response

from app.models import Branch, User
from app.api.routers.depends import authenticate, get_session
from app.schemas.schemas_branch import CreateBranch, ReceiveBranch, DeactivateBranch, RenameBranch, BranchDTO
from app.usecase.usecase_branch import BranchUseCase

def get_branch_use_case(
    session: AsyncSession = Depends(get_session),
    actor: User = Depends(authenticate)
    ) -> BranchUseCase:
    return BranchUseCase(session, actor)


branch_rout = APIRouter(prefix='/v1/branch')

@branch_rout.post('',tags=['Филиалы'],description='Создать новый филиал', response_model=BranchDTO)
async def create_branch(cmd: CreateBranch,
                        use_case: BranchUseCase = Depends(get_branch_use_case))->Branch:
    new_branch = await use_case.create(cmd)
    return new_branch

@branch_rout.get('',tags=['Филиалы'],description='Получить нужные филиалы',response_model=BranchDTO)
async def get_branches(cmd: ReceiveBranch,
                           use_case: BranchUseCase = Depends(get_branch_use_case))->list[Branch]:
    branches = await use_case.receive(cmd)
    if not branches:
        raise HTTPException(status_code=404,detail='Branches not found')
    return branches

@branch_rout.delete('',tags=['Филиалы'],description='Деактивировать филиал')
async def deactivate_branch(cmd:DeactivateBranch,
                            use_case: BranchUseCase = Depends(get_branch_use_case)):
    await use_case.deactivate(cmd)
    return Response(status_code=204)

@branch_rout.patch('',tags=['Филиалы'], description="Переименовать филиал")
async def rename_branch(cmd:RenameBranch,
                        use_case: BranchUseCase= Depends(get_branch_use_case)):
    await use_case.rename(cmd)
    return Response(status_code=204)
