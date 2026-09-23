from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.routers.depends import get_session
from app.usecase.usecase_registration import RegistrationUseCase
from app.schemas.schemas_user import Registry, UserDTO

public_rout = APIRouter()

def get_use_case(session: AsyncSession=Depends(get_session)):
    return RegistrationUseCase(session)

@public_rout.post(path='/register',
                  tags=['Регистрация'],
                  description="""Публичная регистрация.
Если в системе ещё нет пользователей, первый зарегистрированный
пользователь получает роль OWNER. Последующие пользователи
регистрируются без роли""")
async def registrate(cmd: Registry,
                     use_case:RegistrationUseCase = Depends(get_use_case))->UserDTO:
    new_user = await use_case.public_registry(cmd)
    return new_user


@public_rout.get('/health', description="Проверка работы приложения")
async def health():
    return {"status": "ok"}
