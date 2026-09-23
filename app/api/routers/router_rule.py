from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import Response
from app.models import User, Rule
from app.api.routers.depends import get_session, authenticate
from app.schemas.schemas_rule import CreateRule, DeleteRule, RuleDTO
from app.usecase.usecase_rule import RuleUseCase

rule_rout = APIRouter(prefix='/v1/rule')

def get_rule_use_case(session: AsyncSession = Depends(get_session),
    actor: User = Depends(authenticate)
    ) -> RuleUseCase:
    return RuleUseCase(session, actor)

@rule_rout.get(path='',tags=['Правила'],
               description='Показать все правила',response_model=list[RuleDTO])
async def get_rules(use_case: RuleUseCase = Depends(get_rule_use_case))->list[Rule]:
    rules =  await use_case.receive()
    if not rules:
        raise HTTPException(status_code=404,detail="Rules not found")
    return rules

@rule_rout.post(path='',tags=['Правила'],
                description='Создать новое правило',
                response_model=RuleDTO)
async def create_rule(cmd: CreateRule,
                      use_case: RuleUseCase = Depends(get_rule_use_case))->Rule:
    new_rule = await use_case.create(cmd)
    return new_rule

@rule_rout.delete(path='',tags=['Правила'],description='Удалить правило')
async def delete_rule(cmd: DeleteRule,
                      use_case: RuleUseCase = Depends(get_rule_use_case)):
    await use_case.delete(cmd)
    return Response(status_code=204)
