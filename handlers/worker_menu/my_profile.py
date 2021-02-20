"""Кнопка "Мой профиль": просмотр и изменение профиля, ссылка на личную страницу."""
from aiogram import types
from aiogram.contrib.middlewares.conversation import UpdateData
from aiogram.contrib.questions import QuestText
from aiogram.dispatcher import FSMContext

import functions as funcs
from keyboards import markup
from keyboards.inline_plain import change_profile as change_profile_kb
from loader import dp, users_db
from questions import ChangeProfile as States
from texts import templates


@dp.message_handler(text='Мой профиль')
async def send_profile(msg: types.Message):
    account = await users_db.get_account_by_id(msg.from_user.id)

    text = templates.form_profile_template(
        account.profile.nickname,
        account.profile.phone_number or 'Не указан',
        account.profile.email or 'Не указан',
        account.page_url,
    )
    return QuestText(text, change_profile_kb)


# Переход в состояния изменение

@dp.callback_query_handler(text=change_profile_kb.CHANGE_NICKNAME)
async def start_change_nickname(query: types.CallbackQuery):
    return UpdateData(new_state=States.nickname)


@dp.callback_query_handler(text=change_profile_kb.CHANGE_PHONE_NUMBER)
async def start_change_phone_number(query: types.CallbackQuery):
    return UpdateData(new_state=States.phone_number)


@dp.callback_query_handler(text=change_profile_kb.CHANGE_EMAIL)
async def start_change_email(query: types.CallbackQuery):
    return UpdateData(new_state=States.email)


@dp.callback_query_handler(text=change_profile_kb.CHANGE_BIOGRAPHY)
async def start_change_biography(query: types.CallbackQuery):
    return UpdateData(new_state=States.biography)


@dp.callback_query_handler(text=change_profile_kb.CHANGE_WORKS)
async def start_change_works(query: types.CallbackQuery):
    account = await users_db.get_account_by_id(query.from_user.id)
    return UpdateData({'works': account.profile.works}, new_state=States.works)


# Обработка ответов

@dp.message_handler(state=States.nickname)
async def process_nickname(msg: types.Message):
    username = msg.from_user.username
    all_nicknames = await funcs.get_all_nicknames()

    if msg.text.lower() == username.lower():
        return 'Пожалуйста, не используйте свой юзернейм'
    if msg.text in all_nicknames:
        return 'Этот никнейм уже занят'

    await users_db.update_profile_nickname(msg.from_user.id, msg.text)
    return UpdateData(on_conv_exit=QuestText('Никнейм обновлен', markup.worker_kb))


@dp.message_handler(text='Пропустить', state=States.phone_number)
async def miss_phone_number(msg: types.Message):
    await users_db.update_profile_phone_number(msg.from_user.id, None)
    return UpdateData(on_conv_exit=QuestText('Номер телефона сброшен', markup.worker_kb))


@dp.message_handler(content_types=types.ContentType.CONTACT, state=States.phone_number)
async def process_phone_number(msg: types.Message):
    await users_db.update_profile_phone_number(msg.from_user.id, msg.contact.phone_number)
    return UpdateData(on_conv_exit=QuestText('Номер телефона обновлен', markup.worker_kb))


@dp.message_handler(state=States.email)
async def process_email(msg: types.Message):
    if msg.text == 'Пропустить':
        email = None
    elif '@' in msg.text:
        email = msg.text
    else:
        return 'Похоже, вы ошиблись'

    await users_db.update_profile_email(msg.from_user.id, email)
    return UpdateData(on_conv_exit=QuestText('Email изменен', markup.worker_kb))


@dp.message_handler(state=States.biography)
async def process_biography(msg: types.Message):
    if len(msg.text) < 15:
        return 'Напишите не меньше 15 символов'
    await users_db.update_profile_biography(msg.from_user.id, msg.text)
    return UpdateData(on_conv_exit=QuestText('Биография обновлена', markup.worker_kb))


@dp.message_handler(content_types='photo', state=States.works)
async def process_works(msg: types.Message):
    photo_id = msg.photo[-1].file_id
    return UpdateData(extend_data={'works': photo_id}, new_state=None)


@dp.message_handler(text=['Готово', 'Начать заново'], state=States.works)
async def process_works_finish(msg: types.Message, state: FSMContext):
    if msg.text == 'Начать заново':
        return UpdateData(delete_keys='works', new_state=None), 'Осторожно, вы сбросили все работы'

    udata = await state.get_data()
    await users_db.update_profile_works(msg.from_user.id, udata.get('works', []))
    return UpdateData(on_conv_exit=QuestText('Примеры работ обновлены', markup.worker_kb))
