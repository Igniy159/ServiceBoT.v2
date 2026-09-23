from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User
from app.api.routers.depends import get_session, authenticate
from app.schemas.schemas_role import CreateRole, RoleDTO
from app.usecase import RoleUseCase

role_rout = APIRouter(prefix='/v1/role')

def get_role_use_case(session: AsyncSession = Depends(get_session),
    actor: User = Depends(authenticate)
    ) -> RoleUseCase:
    return RoleUseCase(session, actor)

@role_rout.post(path='',
               tags=['Роли'], response_model=RoleDTO)
async def create_role(cmd: CreateRole,
                      use_case: RoleUseCase = Depends(get_role_use_case))->RoleDTO:
    return await use_case.create(cmd)
