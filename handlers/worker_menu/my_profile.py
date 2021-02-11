"""Кнопка "Мой профиль": просмотр и изменение профиля, ссылка на личную страницу."""
from aiogram import types
from aiogram.dispatcher import FSMContext

from functions import common as cfuncs
from keyboards import markup
from keyboards.inline_plain import change_profile
from loader import dp, users_db
from questions import registration as questions
from questions.misc import HandleException
from states import ChangeProfile as States
from texts import templates


@dp.message_handler(text='Мой профиль')
async def send_profile(msg: types.Message):
    account = await users_db.get_account_by_id(msg.from_user.id)
    profile = account.profile
    nickname = profile.nickname
    phone_number = profile.phone_number or 'Не указан'
    email = profile.email or 'Не указан'
    page_url = account.page_url

    text = templates.form_profile_template(nickname, phone_number, email, page_url)
    await msg.answer(text, reply_markup=change_profile)


# Переход в состояния изменение

@dp.callback_query_handler(text=change_profile.CHANGE_NICKNAME)
async def start_change_nickname(query: types.CallbackQuery):
    question = questions.nickname
    await States.nickname.set()
    await query.message.answer(question.text, reply_markup=question.keyboard)


@dp.callback_query_handler(text=change_profile.CHANGE_PHONE_NUMBER)
async def start_change_phone_number(query: types.CallbackQuery):
    question = questions.phone_number
    await States.phone_number.set()
    await query.message.answer(question.text, reply_markup=question.keyboard)


@dp.callback_query_handler(text=change_profile.CHANGE_EMAIL)
async def start_change_email(query: types.CallbackQuery):
    question = questions.email
    await States.email.set()
    await query.message.answer(question.text, reply_markup=question.keyboard)


@dp.callback_query_handler(text=change_profile.CHANGE_BIOGRAPHY)
async def start_change_biography(query: types.CallbackQuery):
    question = questions.biography
    await States.biography.set()
    await query.message.answer(question.text, reply_markup=question.keyboard)


@dp.callback_query_handler(text=change_profile.CHANGE_WORKS)
async def start_change_works(query: types.CallbackQuery):
    account = await users_db.get_account_by_id(query.from_user.id)
    works = account['profile'].get('works', [])
    question = questions.works
    await States.works.set()
    await query.message.answer(question.text, reply_markup=question.keyboard)
    return {'works': works}


# Обработка ответов

@dp.message_handler(state=States.nickname)
async def process_nickname(msg: types.Message):
    username = msg.from_user.username
    all_nicknames = await cfuncs.get_all_nicknames()

    if msg.text.lower() == username.lower():
        return HandleException('Пожалуйста, не используйте свой юзернейм')
    if msg.text in all_nicknames:
        return HandleException('Этот никнейм уже занят')

    await users_db.update_profile_nickname(msg.from_user.id, msg.text)
    await msg.answer('Никнейм обновлен', reply_markup=markup.worker_kb)


@dp.message_handler(text='Пропустить', state=States.phone_number)
async def miss_phone_number(msg: types.Message):
    await users_db.update_profile_phone_number(msg.from_user.id, None)
    await msg.answer('Номер телефона сброшен', reply_markup=markup.worker_kb)


@dp.message_handler(content_types=types.ContentType.CONTACT, state=States.phone_number)
async def process_phone_number(msg: types.Message):
    phone_number = msg.contact.phone_number
    await users_db.update_profile_phone_number(msg.from_user.id, phone_number)
    await msg.answer('Номер телефона обновлен', reply_markup=markup.worker_kb)


@dp.message_handler(state=States.email)
async def process_email(msg: types.Message):
    if msg.text == 'Пропустить':
        email = None
        text = 'Email сброшен'
    elif '@' in msg.text:
        email = msg.text
        text = 'Email обновлен'
    else:
        return HandleException('Похоже, вы ошиблись')
    await users_db.update_profile_email(msg.from_user.id, email)
    await msg.answer(text, reply_markup=markup.worker_kb)


@dp.message_handler(state=States.biography)
async def process_biography(msg: types.Message):
    if len(msg.text) > 15:
        biography = msg.text
    else:
        return HandleException('Напишите не меньше 15 символов')
    await users_db.update_profile_biography(msg.from_user.id, biography)
    await msg.answer('Биография обновлена', reply_markup=markup.worker_kb)


@dp.message_handler(content_types='photo', state=States.works)
async def process_works(msg: types.Message):
    photo_id = msg.photo[-1].file_id
    return {'works': [photo_id]}, HandleException()


@dp.message_handler(text=['Готово', 'Начать заново'], state=States.works)
async def process_works_finish(msg: types.Message, state: FSMContext):
    if msg.text == 'Начать заново':
        return {'works': ()}, HandleException('Осторожно, вы сбросили все работы')

    udata = await state.get_data()
    works = udata.get('works', [])
    await users_db.update_profile_works(msg.from_user.id, works)
    await msg.answer('Примеры работ обновлены', reply_markup=markup.worker_kb)
