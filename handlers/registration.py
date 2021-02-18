"""Все для диалога: регистрация юзера как исполнителя."""
from aiogram import types
from aiogram.contrib.middlewares.conversation import HandleException, NewData

import functions as funcs
from keyboards import markup
from loader import dp
from questions import RegistrationConv as States


@dp.message_handler(text='Пропустить', state=States.phone_number)
async def miss_phone_number(msg: types.Message):
    return NewData({'phone_number': None})


@dp.message_handler(content_types=types.ContentType.CONTACT, state=States.phone_number)
async def process_phone_number(msg: types.Message):
    phone_number = msg.contact.phone_number
    return NewData({'phone_number': phone_number})


@dp.message_handler(state=States.email)
async def process_email(msg: types.Message):
    if msg.text == 'Пропустить':
        email = None
    elif '@' in msg.text:
        email = msg.text
    else:
        return HandleException("Похоже, вы ошиблись в email'е")
    return NewData({'email': email})


@dp.message_handler(state=States.biography)
async def process_biography(msg: types.Message):
    if len(msg.text) > 15:
        return NewData({'biography': msg.text})
    else:
        return HandleException('Напишите не меньше 15 символов')


@dp.message_handler(content_types='photo', state=States.works)
async def process_works(msg: types.Message):
    photo_id = msg.photo[-1].file_id
    return NewData(extend={'works': photo_id}), HandleException()


@dp.message_handler(text=['Готово', 'Начать заново'], state=States.works)
async def process_works_finish(msg: types.Message):
    if msg.text == 'Начать заново':
        return NewData(delete='works'), HandleException('Теперь отправляйте фото заново')
    return NewData(extend={'works': []})


@dp.message_handler(state=States.nickname)
async def process_nickname(msg: types.Message):
    username = msg.from_user.username
    all_nicknames = await funcs.get_all_nicknames()

    if msg.text.lower() == username.lower():
        return HandleException('Пожалуйста, не используйте свой юзернейм')
    if msg.text in all_nicknames:
        return HandleException('Этот никнейм уже занят')

    await funcs.save_profile(nickname=msg.text)
    await funcs.save_author_page()  # создание страницы автора
    await msg.answer('Регистрация пройдена', reply_markup=markup.worker_kb)
