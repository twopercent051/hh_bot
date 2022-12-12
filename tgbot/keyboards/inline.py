from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_user_menu_kb():
    button_1 = InlineKeyboardButton(text='Понятно, меня устраивает', callback_data='main_search')
    keyboard = InlineKeyboardMarkup(row_width=1).add(button_1)
    return keyboard

def send_request_kb(id):
    button_1 = InlineKeyboardButton(text='📞 Откликнуться 📞', callback_data=f'send_request:{id}')
    keyboard = InlineKeyboardMarkup(row_width=1).add(button_1)
    return keyboard


def main_admin_menu_kb():
    button_1 = InlineKeyboardButton(text='🔍 Посмотреть заявки 🔎', callback_data='admin_requests')
    button_2 = InlineKeyboardButton(text='⚙️ Дамп базы ⚙️', callback_data='dump_db')
    keyboard = InlineKeyboardMarkup(row_width=1).add(button_1, button_2)
    return keyboard

def home_kb():
    button_1 = InlineKeyboardButton(text='🏠 Вернуться в начало 🏠', callback_data='home')
    keyboard = InlineKeyboardMarkup(row_width=1).add(button_1)
    return keyboard


def continue_searching():
    button_1 = InlineKeyboardButton(text='🔍Продолжить поиск вакансий', callback_data='continue_searching')
    keyboard = InlineKeyboardMarkup(row_width=1).add(button_1)
    return keyboard


def request_menu_kb():
    button_1 = InlineKeyboardButton(text='✅ Завершённые', callback_data='completed')
    button_2 = InlineKeyboardButton(text='❌ Незавершённые', callback_data='uncompleted')
    keyboard = InlineKeyboardMarkup(row_width=1).add(button_1, button_2)
    return keyboard

def req_list_kb(status, req_id):
    if status == 'completed':
        button_1 = InlineKeyboardButton(text='Возобновить', callback_data=f'to_restart:{req_id}')
    if status == 'waiting':
        button_1 = InlineKeyboardButton(text='Завершить', callback_data=f'to_finish:{req_id}')
    button_2 = InlineKeyboardButton(text='🏠 Вернуться в начало 🏠', callback_data='home')
    keyboard = InlineKeyboardMarkup(row_width=1).add(button_1, button_2)
    return keyboard

