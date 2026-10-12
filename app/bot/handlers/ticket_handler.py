from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy import select

from app.bot.keyboards.main_menu import entity_menu
from app.bot.midlleware import RequestContext
from app.enums import KindRule
from app.models import Department, Rule

ticket_rout = Router()

@ticket_rout.callback_query(F.data == 'create_ticket')
async def create_ticket_start(callback: CallbackQuery,
                        ctx: RequestContext):
    result = await ctx.session.execute(select(Department))
    departments = list(result.scalars().all())
    menu = entity_menu(departments,'create_ticket', prefix='🚩')
    await callback.message.edit_text(text='Выберите отдел для заявки', reply_markup=menu)


@ticket_rout.callback_query(F.data.startswith('create_ticket'))
async def create_ticket_rules(callback: CallbackQuery,
                        ctx: RequestContext):
    depart_id = int(callback.data.split(':')[1])
    result = await ctx.session.execute(select(Rule).where(Rule.target_id == depart_id))
    rules = list(result.scalars().all())
    rule = rules[0]
    if rule.kind == KindRule.OBJECT:
        callback.data = 'ars_objects'
        return
    menu = entity_menu(rules,'rule_ticket',prefix='📨')
    await callback.message.edit_text('Выберите причину обращения', reply_markup=menu)


