from aiogram import Dispatcher
from datetime import datetime

from tgbot.models.db_connector import get_all_users
from create_bot import sheduler, dp, bot, admin_list

async def user_counter_sheduler():
    users = await get_all_users()
    user_counter = len(users)
    text = f'1. Сейчас зарегистрированно {user_counter} пользователей'
    for admin in admin_list:
        await bot.send_message(chat_id=admin, text=text)




def sheduler_jobs():
    sheduler.add_job(user_counter_sheduler, "cron", hour=0, minute=0)
