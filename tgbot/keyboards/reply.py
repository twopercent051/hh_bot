from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def reset_kb():
    button_1 = KeyboardButton('🏠 В начало 🏠')
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    return keyboard.row(button_1)

