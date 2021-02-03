"""Все для диалога: регистрация юзера как исполнителя."""
from aiogram import types
from aiogram.dispatcher import FSMContext

from functions import registration as funcs
from keyboards import markup
from loader import dp, users_db, bot
from questions.misc import HandleException
from questions.registration import RegistrationConv as States
from utils import telegraph_api as telegraph


@dp.message_handler(content_types='any', state=States.phone_number)
async def process_phone_number(msg: types.Message):
    if msg.text == 'Пропустить':
        phone_number = None
    elif msg.contact:
        phone_number = msg.contact.phone_number
    else:
        return HandleException('Ошибка, отправьте номер, нажав на кнопку')
    return {'phone_number': phone_number}


@dp.message_handler(state=States.email)
async def process_email(msg: types.Message):
    if msg.text == 'Пропустить':
        email = None
    elif '@' in msg.text:
        email = msg.text
    else:
        return HandleException('Похоже, вы ошиблись')
    return {'email': email}


@dp.message_handler(state=States.biography)
async def process_biography(msg: types.Message):
    if msg.text == 'Пропустить':
        biography = None
    elif len(msg.text) > 15:
        biography = msg.text
    else:
        return HandleException('Напишите не меньше 15 символов')
    return {'biography': biography}


@dp.message_handler(content_types='photo', state=States.works)
async def process_works(msg: types.Message):
    photo_id = msg.photo[-1].file_id
    return {'works': [photo_id]}, HandleException()


@dp.message_handler(text=['Готово', 'Начать заново'], state=States.works)
async def process_works_finish(msg: types.Message):
    if msg.text == 'Начать заново':
        return {'works': ()}, HandleException('Теперь отправляйте фото заново')
    return {'works': []}


@dp.message_handler(state=States.nickname)
async def process_nickname(msg: types.Message, state: FSMContext):
    user_id = msg.from_user.id
    username = msg.from_user.username
    all_nicknames = await funcs.get_all_nicknames()

    if msg.text == username:
        return HandleException('Пожалуйста, не используйте свой юзернейм')
    if msg.text in all_nicknames:
        return HandleException('Этот никнейм уже занят')

    udata = await state.get_data()
    udata['nickname'] = msg.text
    udata['deals_amount'] = 0

    await users_db.update_account_profile(user_id, udata)
    page_url = await funcs.create_author_page(user_id)
    await users_db.update_account_page_url(user_id, page_url)
    await msg.answer('Регистрация пройдена', reply_markup=markup.worker_kb)
