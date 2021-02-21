"""Все для диалога: регистрация юзера как исполнителя."""
from aiogram import types
from aiogram.contrib.middlewares.conversation import UpdateData
from aiogram.contrib.questions import QuestText

import functions as funcs
import keyboards as KB
from loader import dp
from questions import RegistrationConv as States


@dp.message_handler(text=KB.Miss.MISS, state=States.phone_number)
async def miss_phone_number(msg: types.Message):
    return UpdateData({'phone_number': None})


@dp.message_handler(content_types=types.ContentType.CONTACT, state=States.phone_number)
async def process_phone_number(msg: types.Message):
    phone_number = msg.contact.phone_number
    return UpdateData({'phone_number': phone_number})


@dp.message_handler(state=States.email)
async def process_email(msg: types.Message):
    if msg.text == KB.Miss.MISS:
        email = None
    elif '@' in msg.text:
        email = msg.text
    else:
        return "Похоже, вы ошиблись в email'е"
    return UpdateData({'email': email})


@dp.message_handler(state=States.biography)
async def process_biography(msg: types.Message):
    if len(msg.text) > 15:
        return UpdateData({'biography': msg.text})
    else:
        return 'Напишите не меньше 15 символов'


@dp.message_handler(content_types='photo', state=States.works)
async def process_works(msg: types.Message):
    photo_id = msg.photo[-1].file_id
    return UpdateData(extend_data={'works': photo_id}, new_state=None)


@dp.message_handler(text=[KB.Ready.READY, KB.Ready.START_OVER], state=States.works)
async def process_works_finish(msg: types.Message):
    if msg.text == KB.Ready.START_OVER:
        return UpdateData(delete_keys='works', new_state=None), 'Теперь отправляйте фото заново'
    return UpdateData(extend_data={'works': []})


@dp.message_handler(state=States.nickname)
async def process_nickname(msg: types.Message):
    username = msg.from_user.username
    all_nicknames = await funcs.get_all_nicknames()

    if msg.text.lower() == username.lower():
        return 'Пожалуйста, не используйте свой юзернейм'
    if msg.text in all_nicknames:
        return 'Этот никнейм уже занят'

    await funcs.save_profile(nickname=msg.text)
    await funcs.save_author_page()  # создание страницы автора
    return UpdateData(), QuestText('Регистрация пройдена', KB.ForWorker())
