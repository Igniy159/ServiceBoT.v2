from aiogram.types import InlineKeyboardMarkup,  InlineKeyboardButton as InB
from app.bot.keyboards.main_menu import button_main_menu
from app.models import User, Role


#ЧТО желаете сделать?
def users_menu()->InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InB(text='Мои сотрудники',callback_data='receive')],
            [InB(text='Добавить ',callback_data='create')],
            [InB(text='Переименовать', callback_data='rename')],
            [InB(text='Удалить', callback_data='delete')],
            button_main_menu()
        ]
    )
    return keyboard
