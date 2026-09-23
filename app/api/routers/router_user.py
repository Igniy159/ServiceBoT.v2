from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import Response

from app.api.routers.depends import get_session, authenticate
from fastapi import Depends, APIRouter, HTTPException
from app.schemas.schemas_user import (CreateTgUser, ReceiveUser,
                                      AddLinkTg, ChangeUser,
                                      ActivateUser, DeactivateUser, UserDTO)
from app.models import User
from app.usecase.usecase_user import UserUseCase

user_rout = APIRouter(prefix='/v1/user')

def get_user_use_case(session: AsyncSession = Depends(get_session),
    actor: User = Depends(authenticate))->UserUseCase:
    return UserUseCase(session,actor)

@user_rout.post(path='',
                tags=['Пользователи'],
                description='Добавить пользователя для TG интерфейса',
                response_model=UserDTO)
async def create_user(cmd: CreateTgUser,
                use_case: UserUseCase = Depends(get_user_use_case)
                )->UserDTO:
    new_user = await use_case.create_from_tg(cmd)
    return UserDTO(name=new_user.name,
                   tg_id=new_user.tg_id)

@user_rout.get(path='',
               tags=['Пользователи'],
               description='Получить пользователей',
               response_model=list[UserDTO])
async def receive_users(cmd: ReceiveUser,
                        use_case: UserUseCase = Depends(get_user_use_case)
                        )->list[UserDTO]:
    users = await use_case.receive(cmd)
    if not users:
        raise HTTPException(status_code=404,detail='Users not found')
    return users

@user_rout.patch(path='/change_tg',
                 tags=['Пользователи'],
                 description='Добавить или изменить TG Id для пользователя',
                 response_model=UserDTO)
async def change_tg_id(cmd: AddLinkTg,
                use_case: UserUseCase = Depends(get_user_use_case)
                )->UserDTO:
    new_user = await use_case.change_tg_id(cmd)
    return new_user

@user_rout.patch(path='/change',
                 tags=['Пользователи'],
                 description='Добавить или изменить роль и назначение для пользователя',
                 response_model=UserDTO)
async def change_user(cmd: ChangeUser,
                use_case: UserUseCase = Depends(get_user_use_case)
                )->User:
    new_user = await use_case.change(cmd)
    return new_user

@user_rout.patch(path='/activate',
                 tags=['Пользователи'],
                 description='Активировать уже удаленного пользователя')
async def activate_user(cmd: ActivateUser,
                use_case: UserUseCase = Depends(get_user_use_case)):
    await use_case.activate(cmd)
    return Response(status_code=204)

@user_rout.delete(path='',
                  tags=['Пользователи'],
                  description='Деактивировать пользователя')
async def deactivate_user(cmd: DeactivateUser,
                use_case: UserUseCase = Depends(get_user_use_case)):
    await use_case.deactivate(cmd)
    return Response(status_code=204)
