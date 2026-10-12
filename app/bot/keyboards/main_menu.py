from aiogram.types import InlineKeyboardButton as InB, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def main_menu_builder(permissions: set[str],
                      url: str):
    keyboard = InlineKeyboardBuilder()
    has_full_access = bool('full_access' in permissions)
    view_dash = False
    if 'ticket:create' in permissions or has_full_access:
        keyboard.button(text='➕ Создать заявку',
                        callback_data='create_ticket').adjust(1)
    if 'alert:receive' in permissions or has_full_access:
        keyboard.button(text='🛎️ Мои уведомления',
                        callback_data='my_alerts').adjust(1)
    if 'ticket:receive' in permissions or has_full_access:
        keyboard.button(text='📖 Мои заявки',
                        callback_data='my_tickets').adjust(1)
    if 'branch:receive' in permissions or has_full_access:
        keyboard.button(text='☕ Филиалы',
                        callback_data='my_branches').adjust(1)
        view_dash = True
    if 'user:receive' in permissions or has_full_access:
        keyboard.button(text='👤 Пользователи',
                        callback_data='my_users').adjust(1)
        view_dash = True
    if 'department:receive' in permissions or has_full_access:
        keyboard.button(text="⚒️ Отделы",
                        callback_data='my_departments').adjust(1)
        view_dash = True
    if view_dash or has_full_access:
        keyboard.button(text='⏩ Открыть дашборд',
                        url=url).adjust(1)
    return keyboard.as_markup()


def button_main_menu()-> list[InB]:
    button = [InB(text='🏠Главное меню',callback_data='main_menu')]
    return button

def get_button_main():
    keyboard= InlineKeyboardMarkup(inline_keyboard=[button_main_menu()])
    return keyboard

def get_button_back()-> list[InB]:
    button = [InB(text='🔙Назад',callback_data='back')]
    return button


def entity_menu(objects: list, action: str, prefix:str):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InB(text=f"{prefix} {obj.name}",
                 callback_data=f'{action}:{obj.id}')]
            for obj in objects
        ]
    )
    keyboard.inline_keyboard.append(button_main_menu())
    return keyboard
