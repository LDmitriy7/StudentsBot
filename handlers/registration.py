from loader import dp, users_db
from questions.registration import RegistrationConv as States
from aiogram import types
from questions.misc import HandleException
from functions import common as cfuncs
from functions import registration as funcs
from aiogram.dispatcher import FSMContext
from keyboards import markup


@dp.message_handler(text='Пропустить', state=States.phone_number)
async def miss_phone_number(msg: types.Message):
    return {'phone_number': None}


@dp.message_handler(content_types=types.ContentType.CONTACT, state=States.phone_number)
async def process_phone_number(msg: types.Message):
    phone_number = msg.contact.phone_number
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
    elif 15 < len(msg.text):
        biography = msg.text
    else:
        return HandleException('Напишите не меньше 15 символов')
    return {'biography': biography}


@dp.message_handler(content_types=['photo'], state=States.works)
async def process_works(msg: types.Message):
    photo_id = cfuncs.get_file_obj(msg)[1]
    return {'works': [photo_id]}, HandleException()


@dp.message_handler(text=['Готово', 'Сбросить выбор'], state=States.works)
async def process_works_finish(msg: types.Message):
    if msg.text == 'Сбросить выбор':
        return {'works': ()}, HandleException('Теперь выбирайте заново')
    return {'works': []}


@dp.message_handler(state=States.nickname)
async def process_nickname(msg: types.Message, state: FSMContext):
    username = msg.from_user.username
    all_nicknames = await funcs.get_all_nicknames()

    if msg.text == username:
        return HandleException('Пожалуйста, не используйте свой юзернейм')
    elif msg.text in all_nicknames:
        return HandleException('Этот никнейм уже занят')

    udata = await state.get_data()
    udata['nickname'] = msg.text
    await users_db.update_account_profile(msg.from_user.id, udata)
    await msg.answer('Регистрация пройдена', reply_markup=markup.worker_kb)
