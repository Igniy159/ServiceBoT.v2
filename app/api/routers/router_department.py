from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import Response

from app.models import User, Department
from app.api.routers.depends import get_session, authenticate
from app.schemas.schemas_department import ReceiveDepartment, CreateDepartment, DeactivateDepartment, DepartmentDTO
from app.usecase.usecase_department import DepartmentUseCase

department_rout = APIRouter(prefix='/v1/department')

def get_depart_use_case(session: AsyncSession = Depends(get_session),
    actor: User = Depends(authenticate)
    ) -> DepartmentUseCase:
    return DepartmentUseCase(session, actor)

@department_rout.get(path='',tags=['Отделы'],
                     description='Показать все отделы',
                     response_model=list[DepartmentDTO])
async def receive_departments(
                        cmd: ReceiveDepartment,
                       use_case:DepartmentUseCase=Depends(get_depart_use_case)
                       )->list[Department]:
    departments = await use_case.receive(cmd)
    if not departments:
        raise HTTPException(status_code=404,detail='Department not found')
    return departments

@department_rout.post(path='',tags=['Отделы'],
                      description='Создать новый отдел',
                      response_model=DepartmentDTO)
async def create_department(
                            cmd: CreateDepartment,
                            use_case:DepartmentUseCase=Depends(get_depart_use_case)
                            )->Department:
    return await use_case.create(cmd)

@department_rout.delete(path='',tags=['Отделы'],description='Деактивировать отдел')
async def deactivate_department(cmd: DeactivateDepartment,
                                use_case:DepartmentUseCase=Depends(get_depart_use_case)):
    await use_case.deactivate(cmd)
    return Response(status_code=204)
