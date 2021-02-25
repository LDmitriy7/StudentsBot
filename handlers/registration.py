"""Все для диалога: регистрация юзера как исполнителя."""
from aiogram import types
from aiogram.contrib.middlewares.conversation import UpdateData
from aiogram.contrib.questions import QuestText

import functions as funcs
import keyboards as KB
from loader import dp
from questions import RegistrationConv as States


@dp.message_handler(text=KB.Miss.MISS, state=States.phone_number)
async def miss_phone_number():
    return UpdateData({'phone_number': None})


@dp.message_handler(content_types=types.ContentType.CONTACT, state=States.phone_number)
async def process_phone_number(contact: types.Contact):
    return UpdateData({'phone_number': contact.phone_number})


@dp.message_handler(state=States.email)
async def process_email(text: str):
    if text == KB.Miss.MISS:
        email = None
    elif '@' in text:
        email = text
    else:
        return "Похоже, вы ошиблись в email'е"
    return UpdateData({'email': email})


@dp.message_handler(state=States.biography)
async def process_biography(text: str):
    if len(text) > 15:
        return UpdateData({'biography': text})
    else:
        return 'Напишите не меньше 15 символов'


@dp.message_handler(content_types='photo', state=States.works)
async def process_works(photo: list[types.PhotoSize]):
    photo_id = photo[-1].file_id
    return UpdateData(extend_data={'works': photo_id}, new_state=None)


@dp.message_handler(text=[KB.Ready.READY, KB.Ready.START_OVER], state=States.works)
async def process_works_finish(text: str):
    if text == KB.Ready.START_OVER:
        return UpdateData(delete_keys='works', new_state=None), 'Теперь отправляйте фото заново'
    return UpdateData(extend_data={'works': []})


@dp.message_handler(state=States.nickname)
async def process_nickname(text: str, username: str):
    all_nicknames = await funcs.get_all_nicknames()

    if username and username.lower() == text.lower():
        return 'Пожалуйста, не используйте свой юзернейм'
    if text in all_nicknames:
        return 'Этот никнейм уже занят'

    await funcs.save_profile(nickname=text)
    await funcs.save_author_page()  # создание страницы автора
    return UpdateData(), QuestText('Регистрация пройдена', KB.ForWorker())
