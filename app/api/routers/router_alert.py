from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.api.routers.depends import authenticate, get_session
from app.schemas.schemas_alert import ReceiveAlerts, CreateAlert, AlertDTO
from app.usecase.usecase_alert import AlertUseCase

alert_rout = APIRouter(prefix='/v1/alert')

def get_alert_use_case(session: AsyncSession = Depends(get_session),
    actor: User = Depends(authenticate)
    ) -> AlertUseCase:
    return AlertUseCase(session, actor)

@alert_rout.get('', tags=['Срочные уведомления'],
               description='Показать все уведомления',response_model=AlertDTO)
async def receive_alerts(cmd: ReceiveAlerts,
                         use_case: AlertUseCase = Depends(get_alert_use_case)
                         )->list[AlertDTO]:
    alerts = await use_case.receive(cmd)
    if not alerts:
        raise HTTPException(status_code=404,detail='Alerts not found')
    return alerts

@alert_rout.post('', tags=['Срочные уведомления'],
               description='Создать уведомление')
async def create_alert(cmd: CreateAlert,
                         use_case: AlertUseCase = Depends(get_alert_use_case)
                         )->int:
    alert_id = await use_case.create(cmd)
    return alert_id
