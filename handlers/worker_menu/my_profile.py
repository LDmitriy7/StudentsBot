"""Кнопка "Мой профиль": просмотр и изменение профиля, ссылка на личную страницу."""
from aiogram import types
from aiogram.contrib.middlewares.conversation import UpdateData
from aiogram.contrib.questions import QuestText

import functions as funcs
import keyboards as KB
from loader import dp, users_db
from questions import ChangeProfile as States
from texts import templates


@dp.message_handler(text=KB.for_worker.MY_PROFILE)
async def send_profile(user_id):
    account = await users_db.get_account_by_id(user_id)

    text = templates.form_profile_template(
        account.profile.nickname,
        account.profile.phone_number or 'Не указан',
        account.profile.email or 'Не указан',
        account.page_url,
    )
    return QuestText(text, KB.my_profile)


# Переход в состояния изменение

@dp.callback_query_handler(text=KB.my_profile.CHANGE_NICKNAME)
async def start_change_nickname():
    return UpdateData(new_state=States.nickname)


@dp.callback_query_handler(text=KB.my_profile.CHANGE_PHONE_NUMBER)
async def start_change_phone_number():
    return UpdateData(new_state=States.phone_number)


@dp.callback_query_handler(text=KB.my_profile.CHANGE_EMAIL)
async def start_change_email():
    return UpdateData(new_state=States.email)


@dp.callback_query_handler(text=KB.my_profile.CHANGE_BIOGRAPHY)
async def start_change_biography():
    return UpdateData(new_state=States.biography)


@dp.callback_query_handler(text=KB.my_profile.CHANGE_WORKS)
async def start_change_works(user_id):
    account = await users_db.get_account_by_id(user_id)
    return UpdateData({'works': account.profile.works}, new_state=States.works)


# Обработка ответов

@dp.message_handler(state=States.nickname)
async def process_nickname(user_id, text, username):
    all_nicknames = await funcs.get_all_nicknames()

    if username and username.lower == text.lower():
        return 'Пожалуйста, не используйте свой юзернейм'
    if text in all_nicknames:
        return 'Этот никнейм уже занят'

    await users_db.update_profile_nickname(user_id, text)
    return UpdateData(), QuestText('Никнейм обновлен', KB.for_worker)


@dp.message_handler(content_types=types.ContentType.CONTACT, state=States.phone_number)
async def process_phone_number(contact: types.Contact, user_id):
    await users_db.update_profile_phone_number(user_id, contact.phone_number)
    return UpdateData(), QuestText('Номер телефона обновлен', KB.for_worker)


@dp.message_handler(state=States.phone_number)
async def process_phone_number_manual(text: str, user_id: int):
    if text.isdigit() and len(text) == 12:
        await users_db.update_profile_phone_number(user_id, text)
        return UpdateData(), QuestText('Номер телефона обновлен', KB.for_worker)
    return 'Ошибка, введите только 12 цифр'


@dp.message_handler(state=States.email)
async def process_email(text, user_id):
    if '@' in text:
        email = text
    else:
        return 'Похоже, вы ошиблись'

    await users_db.update_profile_email(user_id, email)
    return UpdateData(), QuestText('Email изменен', KB.for_worker)


@dp.message_handler(state=States.biography)
async def process_biography(text, user_id):
    if len(text) < 15:
        return 'Напишите не меньше 15 символов'
    await users_db.update_profile_biography(user_id, text)
    return UpdateData(on_conv_exit=QuestText('Биография обновлена', KB.for_worker))


@dp.message_handler(content_types='photo', state=States.works)
async def process_works(photo: list[types.PhotoSize]):
    photo_id = photo[-1].file_id
    return UpdateData(extend_data={'works': photo_id}, new_state=None)


@dp.message_handler(text=[KB.ready.READY, KB.ready.START_OVER], state=States.works)
async def process_works_finish(text, user_id, sdata: dict):
    if text == KB.ready.START_OVER:
        return UpdateData(delete_keys='works', new_state=None), 'Осторожно, вы сбросили все работы'

    await users_db.update_profile_works(user_id, sdata.get('works', []))
    return UpdateData(), QuestText('Примеры работ обновлены', KB.for_worker)
