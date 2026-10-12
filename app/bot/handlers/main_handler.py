from os import getenv
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from app.bot.keyboards.main_menu import main_menu_builder
from app.bot.midlleware import RequestContext

main_rout = Router()
url_dash = getenv('URL_DASH')

@main_rout.message(Command('start'))
async def start(message: Message,
          ctx: RequestContext):
    await ctx.auth.load_role()
    menu = main_menu_builder(ctx.auth.permissions, url_dash)
    await message.answer(
        text=f'Добро пожаловать в систему, {ctx.actor.name}!\nВаша роль: {ctx.auth.role.name}',
    reply_markup=ReplyKeyboardRemove())
    await message.answer(
        text="Главное меню 🏠:",
        reply_markup=menu)

@main_rout.callback_query(F.data == 'main_menu')
async def main_menu(callback: CallbackQuery,
                    ctx: RequestContext,
                    state: FSMContext):
    await ctx.auth.load_role()
    menu = main_menu_builder(ctx.auth.permissions, url_dash)
    await state.clear()
    await callback.message.edit_text('🏠 Главное меню: ', reply_markup=menu)
