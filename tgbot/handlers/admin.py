import os
from datetime import datetime
import time

from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery

from tgbot.keyboards.inline import *
from tgbot.models.db_connector import *
from create_bot import bot



import json


async def admin_start_msg(message: Message):
    text = 'Вы авторизованы как администратор'
    keyboard = main_admin_menu_kb()
    await message.answer(text, reply_markup=keyboard)


async def admin_start_clb(callback: CallbackQuery):
    text = 'Вы авторизованы как администратор'
    keyboard = main_admin_menu_kb()
    await bot.answer_callback_query(callback.id)
    await callback.message.answer(text, reply_markup=keyboard)


async def request_menu(callback: CallbackQuery):
    text = 'Выберите тип заявок'
    keyboard = request_menu_kb()
    await bot.answer_callback_query(callback.id)
    await callback.message.answer(text, reply_markup=keyboard)

async def dump_db(callback: CallbackQuery):
    dumper()
    time.sleep(3)
    doc_path = f'{os.getcwd()}/backupdatabase.sql'
    chat_id = callback.from_user.id
    await bot.send_document(chat_id=chat_id, document=open(doc_path, 'rb'))
    await bot.answer_callback_query(callback.id)


async def schow_completed_requests(callback: CallbackQuery):
    req_list_prev = await get_requests('completed')
    req_list = []
    for req in req_list_prev:
        if time.time() - req[5] < 1209600:
            req_list.append(req)
    if len(req_list) == 0:
        text = 'У Вас нет обработанных заявок, поступивших за последние 14 дней'
        keyboard = home_kb()
        await callback.message.answer(text, reply_markup=keyboard)
    else:
        text = 'Завершённые отклики, поданные за последние 14 дней'
        await callback.message.answer(text)
        await bot.answer_callback_query(callback.id)
        for req in req_list:
            req_id = req[0]
            contact = req[3]
            nickname = req[2]
            vac_link = f'https://hh.ru/vacancy/{req[4]}'
            date = datetime.utcfromtimestamp(req[5]).strftime('%d-%m-%Y %H:%M')
            text = [
                '✅',
                f'<b>Контакт для связи:</b> {contact}',
                f'<b>Никнейм в Телеграм:</b> {nickname}',
                f'<b>Вакансия:</b> {vac_link}',
                f'<b>Дата подачи заявки:</b> {date}',
            ]
            keyboard = req_list_kb('completed', req_id)
            await callback.message.answer('\n'.join(text), reply_markup=keyboard, disable_web_page_preview=True)


async def schow_uncompleted_requests(callback: CallbackQuery):
    req_list = await get_requests('waiting')
    if len(req_list) == 0:
        text = 'У Вас нет необработанных заявок'
        keyboard = home_kb()
        await callback.message.answer(text, reply_markup=keyboard)
    else:
        text = 'Незавершённые отклики'
        await callback.message.answer(text)
        await bot.answer_callback_query(callback.id)
        for req in req_list:
            req_id = req[0]
            contact = req[3]
            nickname = req[2]
            vac_link = f'https://hh.ru/vacancy/{req[4]}'
            date = datetime.utcfromtimestamp(req[5]).strftime('%d-%m-%Y %H:%M')
            text = [
                f'<b>Контакт для связи:</b> {contact}',
                f'<b>Никнейм в Телеграм:</b> {nickname}',
                f'<b>Вакансия:</b> {vac_link}',
                f'<b>Дата подачи заявки:</b> {date}',
            ]
            keyboard = req_list_kb('waiting', req_id)
            await callback.message.answer('\n'.join(text), reply_markup=keyboard, disable_web_page_preview=True)


async def change_status(callback: CallbackQuery):
    change_to = callback.data.split(':')[0]
    if change_to == 'to_restart':
        new_status = 'waiting'
    if change_to == 'to_finish':
        new_status = 'completed'
    req_id = callback.data.split(':')[1]
    await update_status(new_status, req_id)
    await bot.answer_callback_query(callback.id)
    await callback.message.delete()

def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start_msg, commands=["start"], state="*", is_admin=True)

    dp.register_callback_query_handler(request_menu, lambda x: x.data == 'admin_requests', state='*', is_admin=True)
    dp.register_callback_query_handler(dump_db, lambda x: x.data == 'dump_db', state='*', is_admin=True)
    dp.register_callback_query_handler(admin_start_clb, lambda x: x.data == 'home', state='*', is_admin=True)
    dp.register_callback_query_handler(schow_completed_requests, lambda x: x.data == 'completed', state='*', is_admin=True)
    dp.register_callback_query_handler(schow_uncompleted_requests, lambda x: x.data == 'uncompleted', state='*', is_admin=True)
    dp.register_callback_query_handler(change_status, lambda x: x.data.split(':')[0] in ['to_restart', 'to_finish'],
                                       state='*', is_admin=True)


