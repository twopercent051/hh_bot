from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

from tgbot.misc.states import *
from tgbot.misc.hh_requester import main_request
from tgbot.keyboards.inline import *
from tgbot.keyboards.reply import *
from tgbot.models.db_connector import *
from create_bot import bot, admin_list


import json

async def user_start(message: Message):
    text = [
        '⚠️Прежде, чем мы начнем:',
        '\n',
        '\n',
        'Мы не храним и не используем Ваши данные без персонального согласия.',
        '\n',
        '\n',
        'Настраивать фильтр поиска и смотреть актуальные вакансии в вашем городе можно без указывания персональных',
        'данных. Если хотите откликнуться на вакансию или связаться с нами, то нужно будет указать Ваше имя и номер',
        'для связи. Но это сильно позже, а пока можно начать с поиска вакансии мечты😊.'
    ]
    keyboard = main_user_menu_kb()
    user_id = message.from_user.id
    username = message.from_user.username
    check_user = await is_user(user_id)
    if check_user == False:
        await create_user(user_id, username)
    await message.answer(' '.join(text), reply_markup=keyboard)


async def search_field(callback: CallbackQuery):
    text = [
        'Введите интересующую Вас специальность и город',
        'Вы можете не вводить город, тогда мы найдем вакансии со всей страны'
    ]
    keyboard = reset_kb()
    await FSMSearch.field.set()
    await bot.answer_callback_query(callback.id)
    await callback.message.answer('\n'.join(text))


async def searcher(message: Message):
    req_field = message.text
    vac_list = await main_request(req_field)
    for vac in vac_list:
        text = [
            f'<b>ВАКАНСИЯ</b>: {vac["title"]}',
            f'<b>ЗАРПЛАТА</b>: {vac["salary"]}',
            f'<b>ГОРОД</b>: {vac["city"]}',
            vac['description'],
            '<b>Требуемый опыт работы:</b>',
            vac['experience'],
            '<b>Занятость:</b>',
            vac['employment'],
            '<b>График:</b>',
            vac['schedule'],
        ]
        keyboard = send_request_kb(vac['vac_id'])
        await message.answer('\n'.join(text), reply_markup=keyboard)


async def get_user_contact(callback: CallbackQuery, state: FSMContext):
    text = 'Введите ваше имя и номер телефона, а так же возраст. HR-специалист свяжется с Вами ближайшее время'
    async with state.proxy() as data:
        data['user_id'] = callback.from_user.id
        if callback.from_user.username is not None:
            data['username'] = f'@{callback.from_user.username}'
        else:
            data['username'] = ''
        data['vac_id'] = str(callback.data).split(':')[1]
    keyboard = reset_kb()
    await FSMSearch.contacts.set()
    await bot.answer_callback_query(callback.id)
    await callback.message.answer(text)


async def send_request_to_admin(message: Message, state: FSMContext):
    user_text = 'Спасибом за отклик! Ожидайте звонка от HR-специалиста.'
    async with state.proxy() as data:
        user_id = data.as_dict()['user_id']
        username = data.as_dict()['username']
        vac_id = data.as_dict()['vac_id']
    vac_link = f'https://hh.ru/vacancy/{vac_id}'
    admin_text = [
        '⚠️⚠️НОВЫЙ ОТКЛИК НА ВАКАНСИЮ ⚠️⚠️',
        f'<b>Контакт для связи:</b> {message.text}',
        f'<b>Никнейм в Телеграм:</b> {username}',
        f'<b>Вакансия:</b> {vac_link}'
    ]
    user_keyboard = continue_searching()
    await create_request(user_id, username, message.text, vac_id)
    await message.answer(user_text, reply_markup=user_keyboard)
    for admin_id in admin_list:
        await bot.send_message(admin_id, '\n'.join(admin_text), disable_web_page_preview=True)





def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
    dp.register_message_handler(searcher, content_types='text', state=FSMSearch.field)
    dp.register_message_handler(send_request_to_admin, content_types='text', state=FSMSearch.contacts)

    dp.register_callback_query_handler(search_field, lambda x: x.data in ['main_search', 'home', 'continue_searching'],
                                       state='*')
    dp.register_callback_query_handler(get_user_contact, lambda x: x.data.split(':')[0] == 'send_request', state='*')

