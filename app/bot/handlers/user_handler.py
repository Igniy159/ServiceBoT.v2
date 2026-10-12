from aiogram import Router, F
from aiogram.types import CallbackQuery
from app.bot.midlleware import RequestContext

user_rout = Router()

@user_rout.callback_query(F.data == 'my_users')
def users_menu(callback: CallbackQuery,
               ctx: RequestContext):
    if ctx.auth.role.need_branch:
        ...
    elif ctx.auth.role.need_department:
        ...
    else:
        ...
